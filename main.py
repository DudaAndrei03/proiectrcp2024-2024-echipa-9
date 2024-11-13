import socket
import struct
import sys
import threading
import json
import os
from idlelib.run import handle_tk_events

""" Server : 

#socket.AF_INET -> specifica faptul ca socket-ul va folosi Internet Protocol V4(IPV4)
        #socket.SOCK_DGRAM -> specifica faptul ca socket-ul va folosi UDP(User Datagram Protocol)
        ________________________________________________________________________________________
        
        #socket.SO_REUSEADDR face posibila ascultarea mai multor socket-uri pe o adresa IP si port
        
        Daca mesajul primit are ca type CON->raspunsul va fi cu un ACK (adica raspuns cu type pus pe ACK)

"""


#Handling errors/exceptions for payload
class PayloadMarkerError(Exception):
    """Exception raised when there is an issue with the payload marker and payload content."""

class PayloadMarkerMissingError(PayloadMarkerError):
    """Raised when the payload marker is missing but the payload is not empty."""

class EmptyPayloadWithMarkerError(PayloadMarkerError):
    """Raised when the payload marker is present, but the payload is empty."""









class Message:
    def __init__(self):
        self.version = None
        self.message_type = None
        self.token_length = None
        self.code = None
        self.message_id = None # 16 bits -> 0 to 65535 values
        self.options = None
        self.payload = None
        self.payload_marker=None

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
        id = 0
        clients = []
        while True:
            # Așteaptă cereri
            data, client_address = self.server_socket.recvfrom(1024)
            #print(f"Request primit de la {client_address}: {data.decode('utf-8')}")->trebuie modficat astfel
            #incat sa parsez numai payload-ul nu intreg pachetul

            #target este UNICA zona de cod unde thread-ul are acces
            print(f"Thread-ul cu id-ul {id} ")
            id += 1#numarul de clienti (id thread client)
            clients.append( (id,client_address) )#lista de tuple
            client_thread = threading.Thread(target=self.handle_request2, args=(data, client_address))
            client_thread.start()

    def parse_header(self,content):

        message=Message()
        if len(content)<4:#len returneaza numarul de bytes din content
            print("Nu sunt destui octeti pentru un mesaj cu header") #header are dim fixa de 4 octeti
            return None

        #tratez header-ul ca un byte string (lucrez cu el cum il primesc) iar payload-ul va fi decodat->byte string rezulta din .pack(),iar din encode va rezulta tot un byte string
        header=struct.unpack("!BBH", content[:4])

        #Header e o tupla de 3 elemente ce contine 8 biti pt. primele 3 campuri, 8 biti pt. code si 16 pt. message id
        message.version=header[0]>>6 #iau primii doi biti din primul octet pentru versiune

        message.type=(header[0]>>4)&0x03 #urmatorii 2 biti pentru tip

        message.token_length=header[0] & 0x0F #ultimii 4 biti pentru lungime token

        message.code=header[1] #exact 8 biti

        message.message_id=header[2] #exact 16 biti

        #Aici pot trata si decodarea payload-ului sau sa pun in camp byte string-ul ce va fi decodat in handle_request
        #apoi decodat in acea functie

        token_end=4+message.token_length
        message.token=content[4:token_end]#token length reprezinta o valoare binara de 4 biti
                                                       #secventa de 0-8 bytes ce trebuie redata in raspuns

        #Momentan fara opituni,payload imediat dupa header

        message.payload_marker=content[token_end:token_end+1]#payload marker e un octet 0xFF

        payload_start=5+message.token_length

        message.payload=content[payload_start:]

        return message

    #data va fi aici message+header
    def handle_request2(self,data, client_address):
        try:
            message=self.parse_header(data)
            payload = message.payload

            if  message.payload_marker != b'\xFF' :
                if len(payload) != 0:
                    raise PayloadMarkerMissingError("Message payload marker is null, but the payload is not empty.")
                    #print("Message payload marker is null but the payload is not empty! ")

            else:
                if len(payload) == 0:
                    raise PayloadMarkerMissingError("Message payload marker is null, but the payload is not empty.")
                    #print("Message payload marker respects the format but the payload is empty!")



            print(payload)
            # Decodează datele JSON primite
            request = json.loads(payload.decode('utf-8'))
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




#un singur thread main
if __name__ == '__main__':
    server = CoAPServer()
    server.run()

