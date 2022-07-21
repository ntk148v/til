"""
Test shit - Make HTTP GET requests against the server.

$ pip intall locustio
# if file was named locustfile.py and located in the current working directory
$ locust --host=http://example.com
# If not
$ locust -f /path/to/locustfile_test.py --host=http://example.com
# Default port - 8089 we can change it with --port=<the-desire-port>
"""
from locust import HttpLocust, TaskSet, task


class TestTaskSet(TaskSet):
    @task(1)
    def index(self):
        self.client.get('/')


class TestLocust(HttpLocust):
    task_set = TestTaskSet
    # Each simulated request will wait between 0.5 and 1 seconds
    # between the requests.
    min_wait = 500
    max_wait = 1000
