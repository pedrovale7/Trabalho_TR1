import socket
import decode_CamadaEnlace as dce
import decode_CamadaFisica as dcf
import random

host,port = ('127.0.0.1', 12345)

def TCPServer(host,port):
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((host,port))
    tcp_server.listen()
    conn,addr = tcp_server.accept()

    while 1:
        data = conn.recv(1024)
        if not data: break
    conn.close()
    
    return data

