import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name. (you can specify any valid IP address.)
host = '127.0.0.1'


# Reserve a port for your service
port = 1024

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections with a maximum queue of 5
server_socket.listen(5)

while True:
    # Establish connection with the client
    # client_socket is the new socket object that you use to communicate with the client.
	# addr is a tuple containing the client's IP address and port number.
    client_socket, addr = server_socket.accept()
    
    print(f"Got a connection from {addr}")
    
    # Send a thank you message to the client
    message = "Thank you for connecting"
    # Data is transmitted over the network as a stream of bytes so we need to convert it.
    client_socket.send(message.encode('ascii'))
    
    # Close the connection
    client_socket.close()