import time
from datetime import datetime
from psutil import cpu_percent
from flask_socketio import emit, SocketIO
import random

DATE_FMT = "%Y-%m-%d %H:%M:%S"
base64_img = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAA' \
            'LEwEAmpwYAAAB1klEQVQ4jY2TTUhUURTHf+fy/HrjhNEX2KRGiyIXg8xgSURuokX' \
            'LxFW0qDTaSQupkHirthK0qF0WQQQR0UCbwCQyw8KCiDbShEYLJQdmpsk3895p4aS' \
            'v92ass7pcfv/zP+fcc4U6kXKe2pTY3tjSUHjtnFgB0VqchC/SY8/293S23f+6VEj' \
            '9KKwCoPDNIJdmr598GOZNJKNWTic7tqb27WwNuuwGvVWrAit84fsmMzE1P1+1TiK' \
            'MVKvYUjdBvzPZXCwXzyhyWNBgVYkgrIow09VJMznpyebWE+Tdn9cEroBSc1JVPS+' \
            '6moh5Xyjj65vEgBxafGzWetTh+rr1eE/c/TMYg8hlAOvI6JP4KmwLgJ4qD0TIbli' \
            'TB+sunjkbeLekKsZ6Zc8V027aBRoBRHVoduDiSypmGFG7CrcBEyDHA0ZNfNphC0D' \
            '6amYa6ANw3YbWD4Pn3oIc+EdL36V3od0A+MaMAXmA8x2Zyn+IQeQeBDfRcUw3B+2' \
            'PxwZ/EdtTDpCPQLMh9TKx0k3pXipEVlknsf5KoNzGyOe1sz8nvYtTQT6yyvTjIax' \
            'smHGB9pFx4n3jIEfDePQvCIrnn0J4B/gA5J4XcRfu4JZuRAw3C51OtOjM3l2bMb8' \
            'Br5eXCsT/w/EAAAAASUVORK5CYII='

def bootstrap_on_connect():
    # emit('bootstrap', {'x': [datetime.now().strftime(DATE_FMT)], 'y': [0]})
    emit('bootstrap', {'chart':"data:image/png;base64,"+ base64_img, 'tick': "HELLO WORLD"})


# def update_plot():
#     socketio = SocketIO(message_queue='redis://localhost:6379/')
#     while True:
#         datetime_now = datetime.now().strftime(DATE_FMT)
#         cpu_percent_second = cpu_percent(interval=1)
#         # cpu_percent_second = random.randint(1,101)
#         socketio.emit('update', {'x': [datetime_now], 'y': [cpu_percent_second]})
#         time.sleep(5)
#         # time.sleep(0.25)

# if __name__ == '__main__':
#     update_plot()