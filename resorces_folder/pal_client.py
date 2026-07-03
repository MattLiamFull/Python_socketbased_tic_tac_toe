'''
 Client sends a string to the palindrome server and prints the response

 Code for CPSC 441 tutorials
 Janet Leahy 
 Sept. 17, 2023
'''

import socket as soc

# IP and port number of the SERVER
HOST = '136.159.5.25'  #csx.cpsc.ucalgary.ca
PORT = 44144

with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.settimeout(3)
    
    message = b"ABBA"
    s.sendall(message)
    
    response = s.recv(1024)
    
    s.sendall(b"EXIT")

print(f"Sent: {message}")
print(f"Received: {response.decode()}")
