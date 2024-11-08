import socket
import struct
import sys
import threading
import json
import os

""" Server : 

#socket.AF_INET -> specifica faptul ca socket-ul va folosi Internet Protocol V4(IPV4)
        #socket.SOCK_DGRAM -> specifica faptul ca socket-ul va folosi UDP(User Datagram Protocol)
        ________________________________________________________________________________________
        
        #socket.SO_REUSEADDR face posibila ascultarea mai multor socket-uri pe o adresa IP si port
        

"""

class Message:
    def __init__(self):
        self.version = None
        self.message_type = None
        self.token_length = None
        self.code = None
        self.message_id = None # 16 bits -> 0 to 65535 values
        self.options = None
        self.payload = None

class CoAPServer:
    def __init__(self, host='localhost', port=5683, base_dir='./uploads'):
        self.host = host
        self.port = port
        self.base_dir = base_dir

        # Crează directorul de upload dacă nu există
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        # Crează socket UDP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        print(f"Serverul CoAP asculta pe {self.host}:{self.port}")

    def handle_request(self, data, client_address):
        try:
            # Decodează datele JSON primite
            request = json.loads(data.decode('utf-8'))
            filename = request.get('filename')
            content = request.get('content')

            # Verifică dacă fișierul și conținutul sunt specificate
            if not filename or not content:
                response = {'error': 'Invalid request'}
                self.send_response(client_address, 400, response)
                return

            file_path = os.path.join(self.base_dir, filename)

            # Verifică dacă fișierul există deja
            if os.path.exists(file_path):
                response = {'error': 'File already exists'}
                self.send_response(client_address, 409, response)
                return

            # Creează fișierul și scrie conținutul
            with open(file_path, 'w') as f:
                f.write(content)

            response = {'message': 'File created successfully'}
            self.send_response(client_address, 201, response)

        except json.JSONDecodeError:
            response = {'error': 'Invalid JSON format'}
            self.send_response(client_address, 400, response)

    def send_response(self, client_address, status_code, response):
        # Pregătește răspunsul
        response_data = json.dumps(response).encode('utf-8')
        # Trimite răspunsul clientului
        self.server_socket.sendto(response_data, client_address)

    def run(self):
        print("Serverul este acum activ.")
        while True:
            # Așteaptă cereri
            data, client_address = self.server_socket.recvfrom(1024)
            print(f"Request primit de la {client_address}: {data.decode('utf-8')}")
            self.handle_request(data, client_address)

if __name__ == '__main__':
    server = CoAPServer()
    server.run()

