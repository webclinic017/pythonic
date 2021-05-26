# this is the modified version of the plotlyredis app. 

# run application server 
python app.py 

# simulate redis update 
<!-- python streaming.py  -->

## update image and tick over socket 
python test.py 

# OR 

# Example 2 : add a base64 image in to var `base64_img2`

from flask_socketio import emit, SocketIO
socketio.emit('chartupdate', {'chart':"data:image/png;base64,"+ base64_img2, 'tick': "New Image"})

