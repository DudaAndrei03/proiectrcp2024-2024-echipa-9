import socket
import json



class CoAPClient:
    def __init__(self,server_host = 'localhost', server_port = 5683):
        self.server_host = server_host
        self.server_port = server_port

        #socket UDP
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


    def send_request(self,filename,content):
        data = json.dumps({'filename' : filename, 'content' : content}).encode('utf-8')
        #converteste string-ul cu format standardizat de tip JSON catre bytes pentru a putea fi transmis la server

        self.client_socket.sendto(data,(self.server_host,self.server_port))

        try:
            response,server_address = self.client_socket.recvfrom(4096)
            print(f"Raspuns primit de la server: {response.decode('utf-8')}")

        except socket.timeout:
            print("Nu s-a primit niciun raspuns de la server.")

if __name__ == '__main__':
    client = CoAPClient()
    client.send_request("test.txt", "Acest mesaj este trimis de la client.")
