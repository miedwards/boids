import socket
import sys

USAGE = '''Usage: python client.py <host> <port> <data>'''

if(len(sys.argv) < 3):
    print USAGE
    sys.exit('''Not Enough Arguments''')

HOST = sys.argv[1]
PORT = -1 
try:
    PORT = int(sys.argv[2])
except ValueError:
    print USAGE
    sys.exit( "Port must be an integer." )
    
data = " ".join(sys.argv[3:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    #received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
#print "Received: {}".format(received)
