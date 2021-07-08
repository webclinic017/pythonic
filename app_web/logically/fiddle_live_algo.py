
# Socket Test with Image Update 
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

