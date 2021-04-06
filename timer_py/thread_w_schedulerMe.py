# How to execute jobs in parallel with python schedule library
# https://schedule.readthedocs.io/en/stable/faq.html

# Notes:
# By default, schedule executes all jobs serially. The reasoning behind this is that it would be difficult to find a model for parallel execution that makes everyone happy.
# You can work around this restriction by running each of the jobs in its own thread


import threading
import time
import schedule
import datetime


def job():  # 1st job that needs execution
	print("[JOB1] I'm running on thread %s" % threading.current_thread())
	time.sleep( 5 )
	print ("[JOB1] Exiting thread %s" % threading.current_thread())

def job2(): # 2nd job that needs execution
	print (">>>>>> [JOB2] I am just another job unction on thread %s" % threading.current_thread())
	time.sleep( 7 )
	print (">>>>>> [JOB2] Exiting thread %s" % threading.current_thread())


# each job above needs its own thread to ensure parallel execution
def run_threaded(job_func): # the thread for the job
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


# Even scheduler configs.
schedule.every(2).seconds.do(run_threaded, job)
schedule.every(5).seconds.do(run_threaded, job2)
schedule.every(7).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job2)


while 1:
    schedule.run_pending()
    time.sleep(1)
