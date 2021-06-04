import concurrent.futures
import queue
import random
import time
import urllib.request

q = queue.Queue()

URLS = [
    "http://www.foxnews.com/",
    "http://www.cnn.com/",
    "http://europe.wsj.com/",
    "http://www.bbc.co.uk/",
    "http://some-made-up-domain.com/",
]


def feed_the_workers(spacing):  ## Producer
    """ Simulate outside actors sending in work to do, request each url twice """
    for url in URLS + URLS:
        time.sleep(spacing)
        q.put(url)
    return "DONE FEEDING"



def load_url(url, timeout):  ## Consumer
    """ Retrieve a single page and report the URL and contents """
    print (f"\t\tFetching {url}. wait.....")
    time.sleep(3)
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()
    # print(url, random.randint(0, 9)) 
    # time.sleep(0.25)


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:

    # start a future for a thread which sends work in through the queue
    future_to_url = {executor.submit(feed_the_workers, 0): "FEEDER DONE"}

    while future_to_url:
        # check for status of the futures which are currently working
        done, not_done = concurrent.futures.wait(
            future_to_url, timeout=0.25, return_when=concurrent.futures.FIRST_COMPLETED
        )

        # if there is incoming work, start a new future
        while not q.empty():

            # fetch a url from the queue
            url = q.get()

            # Start the load operation and mark the future with its URL
            future_to_url[executor.submit(load_url, url, 60)] = url

        # process any completed futures
        for future in done:
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print("%r generated an exception: %s" % (url, exc))
            else:
                if url == "FEEDER DONE":
                    print(data)
                else:
                    print("%r page is %d bytes" % (url, len(data)))

            # remove the now completed future
            del future_to_url[future]
