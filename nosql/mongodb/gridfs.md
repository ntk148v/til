# GridFS

Source: <https://www.mongodb.com/docs/manual/core/gridfs/>

- GridFS is a specification for storing and retrieveing files that exceed the BSON-document size limit of 16MB.
- GridFS divides the file into parts, or chunks, and stores each chunk as a separate document. Default chunk size: 255kB.
- For any file being stored with GridFS, the file is chopped into 255KB chunks.
  - Those chunks are saved in a bucket, called fs, and a collection in that bucket, `fs.chunks`.
  - Metadata about the files is stored in another collection in the same bucket, `fs.files`, though you can have more buckets with different bucket names in the same database.
  - An index makes retrieving the chunks quick.
  - All this chunking and metadata management is not done by the MongoDB database though. It is a task performed by the client's driver which is then wrapperd in a GridFS's API for that driver.
    - For Golang, check [here](https://github.com/mongodb/mongo-go-driver/blob/886d852b768f98f06d976609ef5fdc00351ca405/mongo/gridfs/upload_stream.go#L222) for example.

![](https://www.mongodb.com/docs/drivers/node/current/includes/figures/GridFS-upload.png)

- All this chunking and metadata management is not done by the MongoDB database though. It is a task performed by the client's driver which is then wrapperd in a GridFS's API for that driver.
  - For Golang, check [here](https://github.com/mongodb/mongo-go-driver/blob/886d852b768f98f06d976609ef5fdc00351ca405/mongo/gridfs/upload_stream.go#L222) for example.
- The chunking with GridFS and the fact that it is done by the driver also mean that large operations like replacing an entire file within GridFS are not atomic and there's no built in versioning to fall back on.
- Should have another MongoDB server dedicated to GridFS storage and optimized towards your file storage use pattern.
- When to use GridFS
  - Store files larger than 16MB.
  - If your filesystem limits the number of files in a directory, you can use GridFS to store as many files as needed.
  - When you want to access information from portions of large files without having to load whole files into memory, you can use GridFS to recall sections of files without reading the entire file into memory.
  - When you want to keep your files and metadata automatically synced and deployed across a number of systems of facilities, you can use GridFS.
- When not to use GridFS
  - If you need to update the content of the entire file atomically -> Store multiple versions of each file and specify the current version of the file in the metadata.
  - If your files are all smaller than the 16MB BSON Document Size limit -> store each file in a single document instead of using  GridFS.
