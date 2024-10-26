
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

Web protocol fulfilling M2M (Machine to Machine) requirements in constrained environments

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

- __CoAP messages carry requests and responses__ in a binary format, including method codes like __GET__, __PUT__, __POST__, __DELETE__ , and a specialized method, **JOMAG4**.


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

- 4.Code: 8-bit integer, representing the method or response.

- 5.Message ID: 16-bit integer to identify messages.



