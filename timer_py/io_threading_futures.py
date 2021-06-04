import concurrent.futures
import requests
import threading
import time

# https://realpython.com/python-concurrency/


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    print (f"{time.time()} start url {url}")
    with session.get(url) as response:
        duration = time.time() - start_time
        print(f"Read {len(response.content)} from {url} in {duration} secs")


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(download_site, sites)

start_time = None 

if __name__ == "__main__":
    # sites = [
    #     "https://www.jython.org",
    #     "http://olympus.realpython.org/dice",
    # ] * 80

    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
        'http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/'
    ]

    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
