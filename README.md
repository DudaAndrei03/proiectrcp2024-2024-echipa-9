
# Server CoAP

The Constrained Application Protocol (CoAP) is a specialized web
   transfer protocol for use with constrained nodes and constrained
   (e.g., low-power, lossy) networks.

   CoAP provides a request/response interaction model between
   application endpoints, supports built-in discovery of services and
   resources, and includes key concepts of the Web such as URIs and
   Internet media types.  CoAP is designed to easily interface with HTTP
   for integration with the Web while meeting specialized requirements
   such as multicast support, very low overhead, and simplicity for
   constrained environments.


## Features

- Web protocol fulfilling M2M (Machine to Machine) requirements in constrained environments

- UDP binding with optional reliability supporting unicast and multicast requests.

- Asynchronous message exchanges.

- Low header overhead and parsing complexity.

- URI and Content-type support.

- Simple proxy and caching capabilities.

## CoAP Message Types

CoAP defines four types of messages:

- Confirmable (CON)
- Non-confirmable (NON)
- Acknowledgement (ACK)
- Reset (RST)
## Request/Response Model
- Message Format: CoAP is based on the exchange of compact messages that, by default, are transported over UDP.

- __CoAP messages carry requests and responses__ in a binary format, including method codes like __GET__, __PUT__, __POST__, __DELETE__ , and a specialized method.


```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver| T |  TKL  |      Code     |          Message ID           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Token (if any, TKL bytes)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Options (if any)                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|1 1 1 1 1 1 1 1|      Payload (if any)                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## Field Definitions
- 1.Version (Ver): 2-bit integer indicating the CoAP version.

- 2.Type (T): 2-bit integer for message type: CON (0), NON (1), ACK (2), or RST (3).

- 3.Token Length (TKL): 4-bit integer, indicates the Token length (0-8 bytes).
  

- 4.Code: 8-bit integer, representing the method or response. This holds the type of method/the type of response for the message sent by the client, respectively the server.
  
- 5.Message ID: 16-bit integer to identify messages.
- 6.Token:

   This header structure is followed by the Token value, which may be 0 or 8 bytes (given by the Token Length Field) and which is used to correlate requests and responses. Every message carries a token (even if it is of zero length) and every request carries a token generated by the client that must be replicated by the server in it's response.
    
   The client should generate unique tokens (that are not in use in a source/destination communication) which should be randomized to guard against spoofing of responses (the reason why the length is permitted to be 32 bytes long is to increase the range of possible random values ).

- 7.Payload:

  Following the header, token, and options, if any, comes the optional payload (the actual message sent). If present and of a not null length, it is prefixed by a fixed, one-byte Payload Marker, which indicates the end of options and the start of the payload (it's absence denotes an empty payload).

  Depending on the type of message sent and on the type of the response, the payload can be carried togheter with the acknowledgement or separately. This means that, if the message sent was a confirmable one, the acknowledgement message that acknowledges the request carries the actual data as well. If the message is non-confirmable, no acknowledgement message is sent.

  Depending on the implementation, actions such as a request for a file, for example, could be implemented either with the help of a binary codification (encoding/decoding strings with the help of Python functions) or by usin a file format such as JSON.

- 8.Options: 

  CoAp defines a number of options that can be included in a message, with each option instance being determined by the Option Number of the specific CoAp option,the length of the Option Value, and the actual Option Value (a sequence of exactly Option Length bytes with the length and format of the Option Value depending on the respective option).

   Instead of specifying the Option Number directly, the instances must appear in order of their Option Numbers and a delta encoding is used between them: the Option Number for each instance is calculated as the sum of its delta and the Option Number of the preceding instance in the message.


   ```
   0   1   2   3   4   5   6   7
   +---------------+---------------+
   |               |               |
   |  Option Delta | Option Length |   1 byte
   |               |               |
   +---------------+---------------+
   \                               \
   /         Option Delta          /   0-2 bytes
   \          (extended)           \
   +-------------------------------+
   \                               \
   /         Option Length         /   0-2 bytes
   \          (extended)           \
   +-------------------------------+
   \                               \
   /                               /
   \                               \
   /         Option Value          /   0 or more bytes
   \                               \
   /                               /
   \                               \
   +-------------------------------+
   ```

## Request/Response semantics

CoAp operates similarly to HTTP, where an endpoint playing the role of a client sends a request to a server, which in return provides a service. Unlike HTTP, requests and responses are exchanged asynchronously over CoAP messages.

### Responses:
   
   After receiving a request, a server responds with a message matched to the request with the help of a client-generated token. This is different from the Message ID matching process, where an ACK message is related to a CON message by means of the Message ID (generated by the sender of a CON message), which must be echoed by the recipient in the ACK message. This process is called Message Correlation.
   
   A response is identified by the Code field in the CoAP header being set to a Response Code which indicates the result of the server's attempt to deal with the request.

   The response code is composed of 8 bits, with the upper three representing the class of the response and the lower 5 bits providing details about the overall class (if the message is a request sent by the client this field hold the specific method's codification). 

   The three classes of response codes are:

   2 - Success: The request was successfully received, understood, and accepted.

   4 - Client Error: The request contains bad syntax or cannot be fulfilled.

   5 - Server Error: The server failed to fulfill an apparently valid request.

   CoAP code numbers including the Response Code are documented in the format "c.dd", where "c" is the class in decimal, and "dd" is the detail as a two-digit decimal. For example, some important response codes are:

   - Succes 2.xx: 
      
       -2.01 Created: used in response to POST and PUT
     requests. Serves as an upload function.
      
      -2.02 Deleted: only used in 
      response to requests that cause the resource to cease being
      available, such as DELETE.

      -2.04 Changed: in response to POST functions. Serves as a rename/update function.
      
      -2.05 Content: in response to GET functions. Serves as a download function.
   
   - Client Error 4.xx:
      
      -4.00: The format was not understood.

      -4.04: The data could not be found
   
   - Server Error 5.xx:
      
      -This series of Response Codes suggest the server's inabilty to perform a specific request due to a series of different reasons such as bad gateways or unimplemented functions.


### Types of responses:

- Piggybacked:
  
  In the basic scenario, the response is carried with the Acknowledgement Message that acknowledges a request for a Confirmable Message. The request is sent as one, with the response piggybacked on the Acknowledgement message, even if the response indicates a failure.

   This type of response is often used due to it's ability to save network resources as it avoids sending two messages for confirmation and fulfilling the actual request.

-  Separate:
   
   It may not be possible to return a piggybacked response in all cases, as a server might, for example, take longer to obtain the resource requested and send back the acknowledgement message than the client can wait until it resends the request message. This means that the the request was of the CON type, as the response to a request carried in a Non-confirmable message is always sent separately.

   One way to implement this in a server is to initiate the attempt to obtain the resource representation and, while that is in progress, configure an acknowledgement timer (to track and regulate the delay between the ACK and the eventual response). A server may also immediately send an acknowledgement if it knows in advance that there will be no piggybacked response. In both cases, the acknowledgement effectively is a promise that the request will be acted upon later.

   When the server chooses to use a separate response, it sends the Acknowledgement to the Confirmable request as an Empty message. Once this is sent, another Acknowledgement message must not be sent, even if the client retransmits another identical request. If this happens, another Empty Acknowledgement is sent, and any response must be sent as a separate response (ensuring that the client doesn't receive a duplicate response).

   The protocol leaves the decision whether to piggyback a response or not to the server. The client must be prepared to receive either.

## Methods:
 
- #### GET:

   The GET method retrieves a representation for the information that currently corresponds to the command contained in the request's payload. This can be identified by the first 3 bits of the Code field in a message sent by the client, and should be upon succes answered with a 2.05 Content code. The payload could hold a binary codification of a file's name (that the client wishes to get/download) or the codification of a specific word that details the client's request. Another possibility would be to hold a standard file format (such as a JSON) that will be interpreted by the server which will search for the file requested and send it to the client.

   
- #### POST:

   The POST method requests that the representation enclosed in the request be processed. The actual function performed by the POST method is determined by the server's implementation and by the target resource. Usually, this means that the server's data is updated or a new file (resource) is created. For example, the request's payload could hold the codification of a specific word combined with a file name, which will prompt the server to create that specific file.


## Sequence Example


```
 0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   | 1 | 0 |   0   |     GET=1     |          MID=0x7d34           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  11   |  11   |      "temperature" (11 B) ...
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   | 1 | 2 |   0   |    2.05=69    |          MID=0x7d34           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |1 1 1 1 1 1 1 1|      "22.3 C" (6 B) ...
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

```

![image](https://github.com/user-attachments/assets/7c06e634-9b08-4b5b-b512-49a367118c08)


This is an example of a CoAp interaction with a Confirmable Message and a Piggybacked Response, where the client requests a resource (the temperature) and the server replies in the same Acknowledgement Message with a succes code and the actual resource requested.

## Application Structure

![image](https://github.com/user-attachments/assets/ac3670ba-b52b-4220-b66a-eb40ca16a451)

### Description of the Application Structure
- The Main Thread which holds the main server's process is dedicated to receiving requests from clients. The thread is constantly waiting for clients to connect and uses the accept() function to establish said connection. This means that, after the thread is started (the application is launched), a new thread instance is created for every client/request sent by an already connected client. A multithreading approach is essential for a performant application that can manage multiple requests at once, as it allows for a concurrent processing of all the requests received, thus improving performance and eliminating the need for a single, serial communication on a single thread.
- The Client Thread is present in multiple instances, one for every connection the server receives, connection for which it launches a new thread. From this point, they will act independently, treating each request in parallel. As a result, every thread will perform it's specific action, following the main pattern of checking for bad/invalid requests and generating specific responses for every different request sent by the client.
- The Request Queue is used to provide stability to the server, by queueing every request found on every thread to make sure that each one is safely treated. Every request will be put in the queue, and every thread will extract a request and resolve it depending on it's necesities.
- The main element used is the Thread class from the Python "threading" module, which gives access to functions used for thread creation and management. Each thread will receive a target (an already defined function) that will be launched in execution using the start() function. Moreover, it will also receive the client's specific connection generated by the accept() function, as this gives access to the socket specific functions that will be used to interact with the client.








__Bibliografie__: https://datatracker.ietf.org/doc/html/rfc7252
                  https://sequencediagram.org/
                  https://www.geeksforgeeks.org/constrained-application-protocol-coap/
