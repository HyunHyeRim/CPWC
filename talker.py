# Talker (send data to tensorflow graph)
import socket
import sys
import collections

BUFFER_SIZE = 512

PORT = 9999
TF_PORT = 40000


buffers = collections.deque([])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tf_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.7', PORT))
tf_sock.connect(('127.0.0.1', TF_PORT))

while(True) :
    data = ""
    data = sock.recv(BUFFER_SIZE).decode()
    print("data : ", data)
    data_f = data.split('#')
    if(len(buffers) < 90):
        for i in range(3) :
            buffers.append(data_f[i])
    else :
        send_data = ""
        for i in range(90) :
            send_data += buffers[i] + "#"
        for i in range(3) :
            buffers.popleft()
            buffers.append(data_f[i])
        print(send_data)
        tf_sock.send(send_data.encode())
sock.close()