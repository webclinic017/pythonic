import concurrent.futures
import queue
import time
from threading import Semaphore, Thread

max_workers = 10  # global max_worker count 

processQ = queue.Queue()
has_q = Semaphore(value=0)  # Allow consumers to sleep while waiting for an event (pause infinite loop)
SENTINEL = "END"

def putQ ( job ) : 
    processQ.put (job)  # format: (func, (*args), jobName)
    has_q.release()

def endQ () : 
    processQ.put (SENTINEL)  # format: (func, (*args), jobName)
    has_q.release()

def setMaxWorker(maxWorkers) :
    global max_workers
    max_workers = maxWorkers 

def genericConsumer (queue): ## create a live consumer thread with has_q semaphore 
    
    print (f'Staring IO bound tasks with {max_workers} thread workers.')
    # We can use a with statement to ensure threads are cleaned up promptly        
    # with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:

        # start a future for a thread which sends work in through the queue            
        future_to_func = { } # init empty dict for executors 
            # {executor.submit(lambda x: print ("Started. Waiting for Queue ......"), 0): "FEEDER DONE"}
        exception_count = 0 
        successfull_count = 0 
            
        while has_q.acquire() : # will pause thread for release 
            has_q.release()  # increment to compensate above 

            tic = time.perf_counter()

            while not queue.empty() and has_q.acquire():
                # fetch a url from the queue
                job = queue.get()
                if job == SENTINEL:
                    print(f"\t\tThread Quit Triggered. Job ID: {job}.")
                    print(f"\t\tQuitting Consumer thread....")
                    queue.task_done()
                    processQ.join()
                    return
                # Start the load operation and mark the future with its URL
                # this is a dictionary for future_to_func = { `executorobject` : `job ID`}
                
                myfunc, args, name = job 
                
                future_to_func[executor.submit(myfunc, *args)] = name
        
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
                
                ### Live Thread Updates from the dict of futures
                runningfutures = [v for (k,v) in future_to_func.items() if 'state=running' in str(k)]
                # print('running fut: ', str(runningfutures))
                # print ('all fut:', str(future_to_func))
                # runningfutures = []
                # for future in not_done: ## find 'state=running', 'state=pending' in workers 
                #     if 'state=running' in str(future): runningfutures.append(future_to_func[future])
                # print (f"")

                # print (f"\t\t\tWorkerCount = {len(runningfutures)} | Pending {len(not_done)-len(runningfutures)} | Completed {len(done)}  | queue {len(future_to_func)} | qsize {queue.qsize()} | qUnfinished: {q.unfinished_tasks} | {runningfutures} is running ")
                ## Live End...

                # if there is incoming work, start a new future
                while not queue.empty() and has_q.acquire():

                    # fetch a url from the queue
                    job = queue.get()
                    myfunc, args, name = job 

                    # Start the load operation and mark the future with its URL
                    future_to_func[executor.submit(myfunc, *args)] = name

                # process any completed futures
                for future in done:
                    job = future_to_func[future]
                    try:
                        data = future.result()             
                        queue.task_done() # update task counter in queue if result true
                    except Exception as exc:
                        print("%r generated an exception: %s" % (job, exc))                        
                    else:
                        if job == "FEEDER DONE":
                            # print(data)
                            print ('Job set ended')
                        else:
                            # print("Execution is successful | Job ID:",job) # has name
                            pass
                            
                    # remove the now completed future
                    del future_to_func[future]

            toc = time.perf_counter()
            print (f"Finished in  {toc - tic:0.4f} seconds")
            print ("Waiting for Queue ......")

def initialize(maxWorkers=max_workers) : 
    global max_workers
    max_workers = maxWorkers  # init # of workers    
    print (max_workers)
    ## initialize and start producer, consumer threads 
    threads = [Thread(target=genericConsumer, args=(processQ,))]
    print ('Generic consumer: Threads started ......')
    for thread in threads:
        thread.start()

# ## initialize and start producer, consumer threads 
# threads = [Thread(target=genericConsumer, args=(processQ,))]
# print ('Generic consumer: Threads started ......')
# for thread in threads:
#     thread.start()
