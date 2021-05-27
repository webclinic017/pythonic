import base64
import requests, io
from flask_socketio import emit, SocketIO

socketio = SocketIO(message_queue='redis://localhost:6379/')

myurl = "https://image.shutterstock.com/image-vector/picture-icon-image-photo-260nw-1672289161.jpg"

myurl = "https://s0.2mdn.net/9684689/cs2203r0001_005_548363_us_bb_cm_cm_fy22q2_sit_precision-fixed-family_300x250_ccf.jpg"


response = requests.get(myurl)
image_bytes = io.BytesIO(response.content)

base64_img = base64.b64encode(image_bytes.getbuffer()).decode("ascii")

# Exmaple 1 
socketio.emit('chartupdate', {'chart':"data:image/png;base64,"+ base64_img, 'tick': "New Image"})



# Example 2
base64_img2 = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB1klEQVQ4jY2TTUhUURTHf+fy/HrjhNEX2KRGiyIXg8xgSURuokXLxFW0qDTaSQupkHirthK0qF0WQQQR0UCbwCQyw8KCiDbShEYLJQdmpsk3895p4aSv92ass7pcfv/zP+fcc4U6kXKe2pTY3tjSUHjtnFgB0VqchC/SY8/293S23f+6VEj9KKwCoPDNIJdmr598GOZNJKNWTic7tqb27WwNuuwGvVWrAit84fsmMzE1P1+1TiKMVKvYUjdBvzPZXCwXzyhyWNBgVYkgrIow09VJMznpyebWE+Tdn9cEroBSc1JVPS+6moh5Xyjj65vEgBxafGzWetTh+rr1eE/c/TMYg8hlAOvI6JP4KmwLgJ4qD0TIbliTB+sunjkbeLekKsZ6Zc8V027aBRoBRHVoduDiSypmGFG7CrcBEyDHA0ZNfNphC0D6amYa6ANw3YbWD4Pn3oIc+EdL36V3od0A+MaMAXmA8x2Zyn+IQeQeBDfRcUw3B+2PxwZ/EdtTDpCPQLMh9TKx0k3pXipEVlknsf5KoNzGyOe1sz8nvYtTQT6yyvTjIaxsmHGB9pFx4n3jIEfDePQvCIrnn0J4B/gA5J4XcRfu4JZuRAw3C51OtOjM3l2bMb8Br5eXCsT/w/EAAAAASUVORK5CYII='


# Example 2
socketio.emit('chartupdate', {'chart':"data:image/png;base64,"+ base64_img2, 'tick': "New Image"})