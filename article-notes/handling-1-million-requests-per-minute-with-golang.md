# Handle 1 million requests per minute with Go

Source: <http://marcio.io/2015/07/handling-1-million-requests-per-minute-with-golang/>:

> While working on a piece of our anonymous telemetry and analytics system, our goal was to be able to handle a large amount of POST requests from millions of endpoints. The web handler would receive a JSON document that may contain a collection of many payloads that needed to be written to Amazon S3, in order for our map-reduce systems to later operate on this data.

First version:

```go
type PayloadCollection struct {
	WindowsVersion  string    `json:"version"`
	Token           string    `json:"token"`
	Payloads        []Payload `json:"data"`
}

type Payload struct {
    // [redacted]
}

func (p *Payload) UploadToS3() error {
    // the storageFolder method ensures that there are no name collision in
    // case we get same timestamp in the key name
    storage_path := fmt.Sprintf("%v/%v", p.storageFolder, time.Now().UnixNano())

	bucket := S3Bucket

	b := new(bytes.Buffer)
	encodeErr := json.NewEncoder(b).Encode(payload)
if encodeErr != nil {
		return encodeErr
	}

    // Everything we post to the S3 bucket should be marked 'private'
    var acl = s3.Private
	var contentType = "application/octet-stream"

	return bucket.PutReader(storage_path, b, int64(b.Len()), contentType, acl, s3.Options{})
}
```

Try to parallelize the job processing into a simple goroutine:

```go
func payloadHandler(w http.ResponseWriter, r *http.Request) {

    if r.Method != "POST" {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

    // Read the body into a string for json decoding
	var content = &PayloadCollection{}
	err := json.NewDecoder(io.LimitReader(r.Body, MaxLength)).Decode(&content)
    if err != nil {
		w.Header().Set("Content-Type", "application/json; charset=UTF-8")
		w.WriteHeader(http.StatusBadRequest)
		return
	}

    // Go through each payload and queue items individually to be posted to S3
    for _, payload := range content.Payloads {
        go payload.UploadToS3()   // <----- DON'T DO THIS
    }

    w.WriteHeader(http.StatusOK)
}
```

- There is no way to control how many go routines we are spawning.
- The iteration variables (`payload`) will be reused across each iteration. Depending on the method receiver type you might upload the same payload multiple times (which will happen if the UploadToS3() method has a pointer receiver). Checkout 50 shades of Golang - Iteration variables and Closures in "for" statements --> actually it was fixed (tested on Go 1.24).

Keep the lifetime of the request handler very short and spawning processing in the background. So the 2nd iteration was to create a buffered channel where we could queue up some jobs and upload them to S3 (control the maximum number of items and had plenty of RAM to queue up jobs in memory).

```go
var Queue chan Payload

func init() {
    Queue = make(chan Payload, MAX_QUEUE)
}

func payloadHandler(w http.ResponseWriter, r *http.Request) {
    ...
    // Go through each payload and queue items individually to be posted to S3
    for _, payload := range content.Payloads {
        Queue <- payload
    }
    ...
}

// dequeue jobs and process them
func StartProcessor() {
    for {
        select {
        case job := <-Queue:
            job.payload.UploadToS3()  // <-- STILL NOT GOOD
        }
    }
}
```

We have traded flawed concurrency with a buffered queue that was simple postponing the problem. Our synchronous processor was only uploading one payload at a time to S3, and since the rate of incoming requests were much larger than the ability of the single processor to upload to S3, our buffered channel was quickly reaching its limit and blocking the request handler ability to queue more items.

In order to create a 2-tier channel system, one for queuing jobs and another to control how many workers operate on the JobQueue concurrently. The idea was to parallelize the uploads to S3 to a somewhat sustainable rate, one that would not cripple the machine nor start generating connections errors from S3 -> Job/Worker pattern.

```go
var (
	MaxWorker = os.Getenv("MAX_WORKERS")
	MaxQueue  = os.Getenv("MAX_QUEUE")
)

// Job represents the job to be run
type Job struct {
	Payload Payload
}

// A buffered channel that we can send work requests on.
var JobQueue chan Job

// Worker represents the worker that executes the job
type Worker struct {
	WorkerPool  chan chan Job
	JobChannel  chan Job
	quit    	chan bool
}

func NewWorker(workerPool chan chan Job) Worker {
	return Worker{
		WorkerPool: workerPool,
		JobChannel: make(chan Job),
		quit:       make(chan bool)}
}

// Start method starts the run loop for the worker, listening for a quit channel in
// case we need to stop it
func (w Worker) Start() {
	go func() {
		for {
			// register the current worker into the worker queue.
			w.WorkerPool <- w.JobChannel

			select {
			case job := <-w.JobChannel:
				// we have received a work request.
				if err := job.Payload.UploadToS3(); err != nil {
					log.Errorf("Error uploading to S3: %s", err.Error())
				}

			case <-w.quit:
				// we have received a signal to stop
				return
			}
		}
	}()
}

// Stop signals the worker to stop listening for work requests.
func (w Worker) Stop() {
	go func() {
		w.quit <- true
	}()
}
```

Create an instance of `Job` struct with payload and send into the `JobQueue` channe for the worker to pickup.

```go
func payloadHandler(w http.ResponseWriter, r *http.Request) {

    if r.Method != "POST" {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

    // Read the body into a string for json decoding
	var content = &PayloadCollection{}
	err := json.NewDecoder(io.LimitReader(r.Body, MaxLength)).Decode(&content)
    if err != nil {
		w.Header().Set("Content-Type", "application/json; charset=UTF-8")
		w.WriteHeader(http.StatusBadRequest)
		return
	}

    // Go through each payload and queue items individually to be posted to S3
    for _, payload := range content.Payloads {

        // let's create a job with the payload
        work := Job{Payload: payload}

        // Push the work onto the queue.
        JobQueue <- work
    }

    w.WriteHeader(http.StatusOK)
}
```

During our web server initialization we create a `Dispatcher` and call `Run()` to create the pool of workers and to start listening for jobs that would appear in the `JobQueue`.

```go
dispatcher := NewDispatcher(MaxWorker)
dispatcher.Run()

// ...

type Dispatcher struct {
	// A pool of workers channels that are registered with the dispatcher
	WorkerPool chan chan Job
}

func NewDispatcher(maxWorkers int) *Dispatcher {
	pool := make(chan chan Job, maxWorkers)
	return &Dispatcher{WorkerPool: pool}
}

func (d *Dispatcher) Run() {
    // starting n number of workers
	for i := 0; i < d.maxWorkers; i++ {
		worker := NewWorker(d.pool)
		worker.Start()
	}

	go d.dispatch()
}

func (d *Dispatcher) dispatch() {
	for {
		select {
		case job := <-JobQueue:
			// a job request has been received
			go func(job Job) {
				// try to obtain a worker job channel that is available.
				// this will block until a worker is idle
				jobChannel := <-d.WorkerPool

				// dispatch the job to the worker job channel
				jobChannel <- job
			}(job)
		}
	}
}
```
