import socket
import struct
import sys
import threading
import json
import os
from idlelib.run import handle_tk_events
from turtledemo.penrose import start

from functions import read_file, rename_file, create_file, create_dir, generate_code

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

    def send_response(self, client_address,message,response):
        # Pregătește răspunsul
        response_data = json.dumps(response).encode('utf-8')

        message+=response_data
        # Trimite răspunsul clientulu
        self.server_socket.sendto(message, client_address)

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

            #Deocodez JSON
            request = json.loads(payload.decode('utf-8'))
            category = request.get('CATEGORY') #2 val-FILE sau DIR
            op = request.get('OP')
            param1=request.get('PARAM1')
            param2=request.get('PARAM2')

            method=message.code
            if method==1: #GET
                if category=='FILE': #pe get,fle singura operatie e download, nu mai verific
                    content=read_file(self.base_dir,param1)
                    status_code=generate_code(method,content)
                    response={'CATEGORY':category, 'OP':op,'PARAM1':'Continut fisier','PARAM2':content}

                elif category=='DIRECTORY':
                    content_dir=os.listdir(self.base_dir) #lista de string-uri ce reprezinta fisierele
                    response={'CATEGORY':category, 'OP':op,'PARAM1':'Continut director','PARAM2':content_dir}

            elif method==2: #POST->urmeaza restul de implementari
                if category=='FILE':
                    if op=='RENAME':
                        status=rename_file(param1,param2)
                        status_code=generate_code(method,status)
                        response = {'CATEGORY': category, 'OP': op, 'PARAM1': 'Redenumire',
                                    'PARAM2': None}

            elif method==3:
                if category=='FILE': #o singura operatie, nu mai verific op
                    content=create_file(self.base_dir,param1,param2)#param1 e nume,param2 e content
                    status_code=generate_code(method,content)
                    response = {'CATEGORY': category, 'OP': op, 'PARAM1': 'Creare fisier', 'PARAM2': None}

                elif category=='DIRECTORY':
                    content=create_dir(param1)
                    status_code=generate_code(method,content)

                    response = {'CATEGORY': category, 'OP': op, 'PARAM1': 'Creare director', 'PARAM2': None}
                    #decodificarea payload-ului


            data=self.create_response(message,status_code)

        except json.JSONDecodeError:
           response_error = {'error': 'Invalid JSON format'}

        self.send_response(client_address,data,response)



    def create_response(self,request_message,request_code):

        version=1
        message_type=1
        token_length=request_message.token_length
        #piggybacked->momentan nu exista mesaj gol
        if request_message.message_type==0: #request confirmabil
            message_type=2 #tipul acknowledgment
        elif request_message.message_type==1: # request non-confirmable
            message_type=1

        code=request_code
        message_id=request_message.message_id
        token=request_message.token
        payload_marker = b'\xFF'


        first_byte = (version << 6) | (message_type << 4) | token_length


        print(code)
        header = struct.pack("!BBH",
                             first_byte,
                             code,
                             message_id)

        if message_type==0:
            message=header
        else:
            message=header+token+payload_marker

        return message



#un singur thread main
if __name__ == '__main__':
    server = CoAPServer()
    server.run()

