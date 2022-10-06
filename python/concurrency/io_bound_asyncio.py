import asyncio
import time

import aiohttp


async def download_site(session, url):
    async with session.get(url, verify=False) as response:
        print("Read {0} from {1}".format(response.content_length, url))


async def download_all_sites(sites):
    # Tasks can share a session because they are all running on the same thread
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        # Keep the session context alive until all of tasks have completed.
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    # Python >=3.7
    asyncio.run(download_all_sites(sites))
    # Legacy
    # asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")
