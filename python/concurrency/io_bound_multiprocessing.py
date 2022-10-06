import requests
import multiprocessing
import time

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site(url):
    if session is None:
        return
    with session.get(url, verify=False) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")


def download_all_sites(sites):
    # Pool creates a number of separate Python interpreter processes and
    # has each one run the specified function on some of the items
    # in the iterable - a list of sites.
    # initializer=set_global_session: Each process in Pool has its own memory
    # space, so we create one session for each process. Initialize a global
    # session variable to hold the single session for each process.
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
