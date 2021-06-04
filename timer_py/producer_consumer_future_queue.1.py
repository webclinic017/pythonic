## Reading material behind this 
# https://towardsdatascience.com/dive-into-queue-module-in-python-its-more-than-fifo-ce86c40944ef
# https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html
# https://alexwlchan.net/2019/10/adventures-with-concurrent-futures/
# https://melvinkoh.me/solving-producerconsumer-problem-of-concurrent-programming-in-python-ck3bqyj1j00i8o4s1cqu9mfi7

import concurrent.futures
import queue
import random
import time
from threading import Semaphore, Thread

q = queue.Queue()
has_q = Semaphore(value=0)  # Allow consumers to sleep while waiting for an event (pause infinite loop)
SENTINEL = "END"

def compute (i) : # simulate a high compute or low latency IO process 
    duration = random.randint(0,7)
    print (f"Compute {i} started with {duration} secs")
    time.sleep(duration)

def load_url(url, timeout): 
    duration = random.randint(0,7)
    print (f"Compute {url} started with {duration} secs")
    time.sleep(duration)

def producer(queue):
    for i in range(15):
        # time.sleep(0.01) # Do you think the result will be changed if I uncomment this line? 
        print(f"Insert element {i}")
        queue.put(i)
        has_q.release()
    # queue.put(SENTINEL)
    print(f"Insert sentinel")

def consumer2(queue):
    while has_q.acquire(): # wait for q to fill and some thread to release it 
        item = queue.get()
        if item != SENTINEL:
            print(f"\t\tRetrieve element {item}.")
            queue.task_done()
        else:
            print("\t\tReceive SENTINEL, the consumer will be closed.")
            queue.task_done()
            break


def consumer (queue): 
    
    # We can use a with statement to ensure threads are cleaned up promptly        
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        # start a future for a thread which sends work in through the queue
        future_to_url = {executor.submit(lambda x: print ("started"), 0): "FEEDER DONE"}

        while has_q.acquire() : # will pause thread for release 
            has_q.release()  # increment to compensate above 
            while not queue.empty() and has_q.acquire():
                    # fetch a url from the queue
                    url = queue.get()
                    # Start the load operation and mark the future with its URL
                    future_to_url[executor.submit(load_url, url, 60)] = url
            
            while future_to_url:
                # check for status of the futures which are currently working
                done, not_done = concurrent.futures.wait(
                    future_to_url, timeout=1.0, return_when=concurrent.futures.FIRST_COMPLETED
                )

                print (f"Running {len(not_done)} | Completed {len(done)}")

                # if there is incoming work, start a new future
                while not queue.empty() and has_q.acquire():

                    # fetch a url from the queue
                    url = queue.get()

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
                            print("Execution is successful",url)

                    # remove the now completed future
                    del future_to_url[future]
            print ("Waiting for Queue ......")


## initialize and start producer, consumer threads 
threads = [Thread(target=producer, args=(q,)),Thread(target=consumer, args=(q,)),]
for thread in threads:
    thread.start()

# Simulate late jobs 
time.sleep(20)
for i in range (22, 25):  
    print(f"Insert element {i}")
    q.put(i)
    has_q.release() # increment semaphore counter by each count of put job 


# Simulate late jobs 2
time.sleep(10)
for i in range (101, 103):  
    print(f"Insert element {i}")
    q.put(i)
    has_q.release() # increment semaphore counter by each count of put job 



# # q.join()
