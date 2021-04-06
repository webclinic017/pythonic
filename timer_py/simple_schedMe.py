# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds

import sched, time, datetime
s = sched.scheduler(time.time, time.sleep)

def do_something(sc): 
    print("Doing stuff...", datetime.datetime.now())
    # do your stuff
    s.enter(2, 1, do_something, (sc,))

s.enter(5, 1, do_something, (s,))
s.run()
