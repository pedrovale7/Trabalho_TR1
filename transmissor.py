import socket

def startServer(message, host = '127.0.0.1', port = 12345):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((host, port))
    
    status = tcp_client.send(message)
    if status>0:
        data = tcp_client.recv(1024)
    tcp_client.close()