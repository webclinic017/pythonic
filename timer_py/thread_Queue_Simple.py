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
    for _ in range(4):
        orders.put("Order"+str(_))
        print ("placing order", "Order"+str(_))
        # time.sleep(1)
        has_order.release() # ADDED THIS: Release the Semaphore, increment the internal counter by 1

    time.sleep(3)
    
    for _ in range(5,9):
        orders.put("Order"+str(_))
        print ("placing order", "Order"+str(_))
        has_order.release() # ADDED THIS: Release the Semaphore, increment the internal counter by 1


def serving_line_or_consumer():
    while has_order.acquire():  # ADDED THIS: Acquire a Semaphore, or sleep until the counter of semaphore is larger than zero
        new_order = orders.get()
        # prepare meals from `new_order`, assuming GIL is released while preparing meals
        print ('Preparing order', new_order)
        # time.sleep(1)
        # if (new_order == 'Order1') : time.sleep (10)
        # else: time.sleep(2)
        print ('DONE order', new_order)
        orders.task_done()


# Let's put 4 staff into the order line
order_line = threading.Thread(target=order_line_or_producer)

# Let's assign 6 staff into the serving line
serving_line = threading.Thread(target=serving_line_or_consumer)

# # Put all staff to work
# [t.start() for t in order_line]
# [t.start() for t in serving_line]

order_line.start()
serving_line.start()

# "join" the order, block until all orders are cleared
# orders.join()

# "join" the threads, ending all threads
# [t.join() for t in order_line]
# [t.join() for t in serving_line]

# order_line.join()
# serving_line.join()
print ('all orders completed')

time.sleep(15) ## test reactivation
orders.put("Order"+str(15))
print ("placing order", "Order"+str(15))
has_order.release() 


time.sleep(5) ## test reactivation
orders.put("Order"+str(5))
print ("placing order", "Order"+str(5))
has_order.release() 

# Exit all threads 
# orders.join()
# order_line.join()
# serving_line.join()
print ("Exiting all producers and consumers")