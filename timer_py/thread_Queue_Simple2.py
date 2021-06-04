"""
Implementation 3: Use Semaphores
https://melvinkoh.me/solving-producerconsumer-problem-of-concurrent-programming-in-python-ck3bqyj1j00i8o4s1cqu9mfi7
"""

import queue
import threading
import time

orders = queue.Queue()
has_order = threading.Semaphore(value=0)  # ADDED THIS


def order_line_or_producer():
    # Each staff in the serving line produces 200 orders
    for _ in range(10):
        orders.put("Order"+str(_))
        print (f"\t\tPlacing new order {_}")

        time.sleep(0.1)
        has_order.release() # ADDED THIS: Release the Semaphore, increment the internal counter by 1


def serving_line_or_consumer():
    while has_order.acquire():  # ADDED THIS: Acquire a Semaphore, or sleep until the counter of semaphore is larger than zero
        new_order = orders.get()
        print (f"Serving new order {new_order}")
        time.sleep(0.25)
        # prepare meals from `new_order`, assuming GIL is released while preparing meals
        orders.task_done()


# Let's put 4 staff into the order line
order_line = [threading.Thread(target=order_line_or_producer) for _ in range(4)]

# Let's assign 6 staff into the serving line
serving_line = [threading.Thread(target=serving_line_or_consumer) for _ in range(6)]

# Put all staff to work
[t.start() for t in order_line]
[t.start() for t in serving_line]

print ("P, C started")

# # "join" the order, block until all orders are cleared
# orders.join()

# # "join" the threads, ending all threads
# [t.join() for t in order_line]
# [t.join() for t in serving_line]