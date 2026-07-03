import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name
host = '127.0.0.1'

# Reserve a port for your service
port = 1024

# Connection to the server
client_socket.connect((host, port))

# Receive data from the server
# Buffer size is 1024
message = client_socket.recv(1024)

# Print the received message
print(message.decode('ascii'))

# Close the socket
client_socket.close()