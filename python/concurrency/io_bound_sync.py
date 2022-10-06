import requests
import time


def download_site(url, session):
    with session.get(url, verify=False) as response:
        print(f"Read {len(response.content)} from {url}")


# download_all_sites() walks through a list of sites,
# downloading each one in turn
def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
