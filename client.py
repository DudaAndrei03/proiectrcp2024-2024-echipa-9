import socket
import json
import struct



class CoAPClient:
    def __init__(self,server_host = 'localhost', server_port = 5683):
        self.server_host = server_host
        self.server_port = server_port

        #socket UDP
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


    def send_request(self,filename,content):

        version = 1#la << voi shifta 00000001
        message_type = 1
        token_length = 4
        #-
        code = 1  # GET request in CoAP
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
        data = json.dumps({'filename' : filename, 'content' : content}).encode('utf-8')
        #data->payload
        #converteste string-ul cu format standardizat de tip JSON catre bytes pentru a putea fi transmis la server

        self.client_socket.sendto(message,(self.server_host,self.server_port))

        try:
            response,server_address = self.client_socket.recvfrom(4096)
            print(f"Raspuns primit de la server: {response.decode('utf-8')}")

        except socket.timeout:
            print("Nu s-a primit niciun raspuns de la server.")

if __name__ == '__main__':
    client = CoAPClient()
    client.send_request("test.txt", "Acest mesaj este trimis de la client.")
