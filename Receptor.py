import socket
import threading

class Receiver:
    def __init__(self):
        self.received_data = None
        self.data_ready = threading.Event()

    def TCPServer(self, host='127.0.0.1', port=12345):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"Servidor aguardando conexão em {host}:{port}...")
            conn, addr = s.accept()
            with conn:
                print(f"Conexão estabelecida com {addr}")
                self.received_data = conn.recv(1024)
                print(f"Dados recebidos: {self.received_data}")
                self.data_ready.set()  # Sinaliza que os dados estão prontos