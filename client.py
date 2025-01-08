import socket
import json
import struct

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



class CoAPClient:
    def __init__(self,server_host = 'localhost', server_port = 5683):
        self.server_host = server_host
        self.server_port = server_port

        #socket UDP
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


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



    def send_request(self,filename,content):

        version = 1#la << voi shifta 00000001
        message_type = 1
        token_length = 4
        #-
        code = 2
        message_id = 16
        token = b'\xA1\xB2\xC3\xD4'
        payload_marker=b'\xFF'

        first_byte = (version << 6) | (message_type << 4) | token_length

        #Primii 4 bytes impachetati (header)
        header = struct.pack("!BBH",
                             first_byte,
                             code,
                             message_id)


        message=header+token+payload_marker

        file_content='Test create file'
        file_content_bytes=file_content.encode('utf-8')
        data = json.dumps({'CATEGORY' : 'DIRECTORY',
                           'OP' : 'RENAME',
                            'PARAM1':'DIR_TEST_MAKEDIR/DIR_TEST_PENTRU_RENAME',
                           'PARAM2':'banane'
                           }).encode('utf-8')
        #data->payload
        #converteste string-ul cu format standardizat de tip JSON catre bytes pentru a putea fi transmis la server

        self.client_socket.sendto(message+data,(self.server_host,self.server_port))


        try:
            response,server_address = self.client_socket.recvfrom(4096)
            parsed_response=self.parse_header(response)

            print(parsed_response.code)
            print(f"Raspuns primit de la server: {parsed_response.payload.decode('utf-8')},")

        except socket.timeout:
            print("Nu s-a primit niciun raspuns de la server.")

if __name__ == '__main__':
    client = CoAPClient()
    client.send_request("test.txt", "Acest mesaj este trimis de la client.")

