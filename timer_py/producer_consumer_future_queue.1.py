## Reading material behind this 
# https://towardsdatascience.com/dive-into-queue-module-in-python-its-more-than-fifo-ce86c40944ef
# https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html
# https://alexwlchan.net/2019/10/adventures-with-concurrent-futures/
# https://melvinkoh.me/solving-producerconsumer-problem-of-concurrent-programming-in-python-ck3bqyj1j00i8o4s1cqu9mfi7
# https://stackoverflow.com/questions/41648103/how-would-i-go-about-using-concurrent-futures-and-queues-for-a-real-time-scenari

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

def myfunc(job, timeout): 
    duration = random.randint(0,7)
    print (f"Compute {job} started with {duration} secs")
    time.sleep(duration)

def producer(queue):
    for i in range(15):
        # time.sleep(0.01) # Do you think the result will be changed if I uncomment this line? 
        print(f"Insert element {i}")
        queue.put(i)
        has_q.release()
    # queue.put(SENTINEL)
    print(f"Insert sentinel. Exiting Producer.")

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


def consumer (queue): ## create a live consumer thread with has_q semaphore 
    
    # We can use a with statement to ensure threads are cleaned up promptly        
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        # start a future for a thread which sends work in through the queue            
        future_to_func = {
            executor.submit(lambda x: print ("Started. Waiting for Queue ......"), 0): "FEEDER DONE"}

        while has_q.acquire() : # will pause thread for release 
            has_q.release()  # increment to compensate above 
            while not queue.empty() and has_q.acquire():
                # fetch a url from the queue
                job = queue.get()
                # Start the load operation and mark the future with its URL
                future_to_func[executor.submit(myfunc, job, 60 )] = job
        
                # https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html#submitfn-args-kwargs
                # sample executor with function and args 
                # args = ((a, b) for b in c)
                # for result in executor.map(f, args):
                #     pass
                    
            while future_to_func:
                # check for status of the futures which are currently working
                done, not_done = concurrent.futures.wait(
                    future_to_func, timeout=1.0, return_when=concurrent.futures.FIRST_COMPLETED
                )

                print (f"\t\t\tRunning {len(not_done)} | Completed {len(done)}  | queue {len(future_to_func)} | qsize {queue.qsize()}")
                # if there is incoming work, start a new future
                while not queue.empty() and has_q.acquire():

                    # fetch a url from the queue
                    job = queue.get()

                    # Start the load operation and mark the future with its URL
                    future_to_func[executor.submit(myfunc, job, 60)] = job

                # process any completed futures
                for future in done:
                    job = future_to_func[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print("%r generated an exception: %s" % (job, exc))
                    else:
                        if job == "FEEDER DONE":
                            print(data)
                        else:
                            print("Execution is successful",job)

                    # remove the now completed future
                    del future_to_func[future]
            print ("Waiting for Queue ......")


## initialize and start producer, consumer threads 
threads = [Thread(target=producer, args=(q,)),Thread(target=consumer, args=(q,)),]
for thread in threads:
    thread.start()
# threads[1].start()  # testing if only consumer is started # ! Works ! 

# Simulate late jobs 
time.sleep(5)
for i in range (22, 25):  
    print(f"Insert element {i}")
    q.put(i)
    has_q.release() # increment semaphore counter by each count of put job 


# Simulate late jobs 2
time.sleep(10)
for i in range (101, 103):  
    print(f"Insert element {i}")
    has_q.release() # increment semaphore counter by each count of put job 
    q.put(i)



# # q.join()
