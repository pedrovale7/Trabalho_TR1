import socket
import time
from bitarray import bitarray

def startServer(message, host='127.0.0.1', port=12345, max_retries=3):

    bit_data = bitarray()
    bit_data.extend(message)
    byte_array = bit_data.tobytes()
    
    for attempt in range(max_retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(byte_array)
                print("Dados enviados com sucesso!")
                return True
        except ConnectionRefusedError:
            print(f"Tentativa {attempt + 1}/{max_retries} - Servidor não disponível. Tentando novamente...")
            time.sleep(1)
    print("Falha ao conectar ao servidor após várias tentativas.")
    return False