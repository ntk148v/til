import concurrent.futures
import requests
import threading
import time


thread_local = threading.local()


# Each thread needs to create its own requests.Session() object.
# Because the OS is in control of when your tasks gets interrupted
# and another task starts, any data that is shared between threads
# needs to be protected, or thread-safe. Unfortunately, requests.Session()
# is not thread-safe.
# Solution
# threading.local() creates an object that looks like a global
# but is specific to each thread.
def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    # ThreadPoolExecutor = Thread + Pool + Executor
    # Thread
    # Pool: create a pool of threads, each of which can run concurrency.
    # Executor: the part that's going to control how and when each of the
    #           threads in the pool will run.
    # Use as context manager to mange creating and freeing the pool of Threads.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
