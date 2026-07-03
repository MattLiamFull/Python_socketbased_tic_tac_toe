'''
 Simple server that responds with random greetings

 Code for CPSC 441 tutorials
 Janet Leahy 
 Sept. 17, 2023
'''

import socket as soc
import random

HOST = '127.0.0.1'  #localhost
PORT = 1024


greet = ["Hello there!", "Bonjour", "Yo sup", "Greetings strange being", "Who's there?", "Hello, it's me...", "Praise the sun"]

# use IPv4 and TCP
with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    
    s.listen()
    
    conn, addr = s.accept()
    
    # conn is the new socket used to communicate with the client
    with conn:
        print(f"Connected to {addr}")
        
        data = conn.recv(1024)
        print(f"Received: {data.decode()}")
            
        if (data.decode() == "HELLO"):
            i = random.randint(0, len(greet) - 1)
            conn.sendall(bytes(greet[i], 'utf-8'))
            
        else:
            conn.sendall(bytes(f"Incorrect! You sent {data.decode()} instead of HELLO", "utf-8"))