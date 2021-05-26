serv = None 

import socket
# def create_localSocket() : 

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 12345))
serv.listen(5)
print ('Socket Server Listening......')
while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += data.decode("utf-8") # decode bytes to string 
        print (from_client)
        conn.send(b"I am SERVER<br>")  # response message to be sent in bytes over TCP
    conn.close()
    print ('client disconnected')

    
    
    # return serv


## The following is a client example 
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 12345))
client.send(b"I am CLIENT<br>") # this is the message to be sent in bytes over TCP
from_server = client.recv(4096)
client.close()
print (from_server)
