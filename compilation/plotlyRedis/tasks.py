import time
from datetime import datetime, timedelta, date
from flask_socketio import SocketIO
import random


def update_plot():
    # x = (date(2018, 1, 1)+timedelta(days=299))
    x = (datetime.now()+timedelta(seconds=20))
    socketio = SocketIO(message_queue='redis://localhost:6379/')
    while True:
        # x = x + timedelta(days=1)
        x = x + timedelta(seconds=5)
        cpuUT = random.randint(1,101)
        # print ({'x': x.strftime("%Y-%m-%d"), 'y': cpuUT})
        print ({'x': x.timestamp(), 'y': cpuUT})
        socketio.send({'x': x.timestamp(), 'y': cpuUT})
        time.sleep(1)


update_plot()