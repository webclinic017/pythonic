# https://towardsdatascience.com/dive-into-queue-module-in-python-its-more-than-fifo-ce86c40944ef

from threading import Thread
import time
import queue

q = queue.Queue()
SENTINEL = "END"

def producer(queue):
    for i in range(15):
        # time.sleep(0.01) # Do you think the result will be changed if I uncomment this line? 
        print(f"Insert element {i}")
        queue.put(i)
    queue.put(SENTINEL)
    print(f"Insert sentinel")

def consumer(queue):
    while True:
        item = queue.get()
        if item != SENTINEL:
            print(f"Retrieve element {item}.")
            queue.task_done()
        else:
            print("Receive SENTINEL, the consumer will be closed.")
            queue.task_done()
            break

threads = [Thread(target=producer, args=(q,)),Thread(target=consumer, args=(q,)),]

for thread in threads:
    thread.start()

q.join()