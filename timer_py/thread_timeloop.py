import time
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print ("2s job current time : {}".format(time.ctime()))

@tl.job(interval=timedelta(seconds=4))
def sample_job_every_2s():
    print ("4s job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(seconds=5))
def sample_job_every_5s():
    print ("5s job current time : {}".format(time.ctime()))

@tl.job(interval=timedelta(seconds=10))
def sample_job_every_10s():
    print ("10s job current time : {}".format(time.ctime()))

if __name__ == "__main__":
    tl.start(block=True)

#Output:
#2s job current time : Tue Oct 16 17:55:35 2018
#2s job current time : Tue Oct 16 17:55:37 2018
#5s job current time : Tue Oct 16 17:55:38 2018
#2s job current time : Tue Oct 16 17:55:39 2018
#2s job current time : Tue Oct 16 17:55:41 2018
#10s job current time : Tue Oct 16 17:55:43 2018


