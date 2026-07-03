'''
 Simple client that sends a "HI" message to the server and prints the response

 Code for CPSC 441 tutorials
 Janet Leahy 
 Sept. 17, 2023
'''

import socket as soc

# IP and port number of the SERVER
HOST = '127.0.0.1'  #localhost
PORT = 1024

with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.sendall(b"HELLO")
    
    response = s.recv(1000)
    
print(f"Received: {response.decode()}")