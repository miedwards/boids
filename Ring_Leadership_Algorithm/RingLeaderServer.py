import logging
import SocketServer
from datetime import date

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    filename='adder-%(date)s.log' % {'date' : date.today()}
                    )

class LeaderRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('LeaderRequestHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')
        data = self.request.recv(1024)
        self.logger.debug('recv()->"%s"', data)
        try:
            received_value = int(data)
        except ValueError:
            self.logger.warn('Invalid Data->"%s"', data)
            self.request.send('ERROR')
            return
        if( received_value < self.server.server_id ):
            self.server.send_flag = False
        elif( received_value == self.server.server_id ):
            self.server.leader = True 
            self.server.send_flag = False
            self.logger.info("I am the leader!")
        elif(received_value > self.server.server_id):
            self.server.current_max = received_value
            self.server.leader = False
            self.server.send_flag = True
        self.server.send_to_neighbor()

    def finish(self):
        self.logger.debug('finish')
        self.request.close()
        return SocketServer.BaseRequestHandler.finish(self)

class LeaderServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=LeaderRequestHandler,
                 neighbor=(), server_id=None):
        self.logger = logging.getLogger('LeaderServer')
        self.logger.debug('__init__')
        self.neighbor_address = neighbor
        self.neighbor = None
        self.current_max = server_id
        self.server_id = server_id
        self.send_flag = True
        self.leader = False
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return
    
    def connect_to_neightbor(self):
        import socket
        self.neighbor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.neighbor.connect(self.neighbor_address)
        return
    
    def send_to_neighbor(self):
        if( not self.send_flag ):
            return
        if self.neighbor:
            self.neighbor.close()
        self.connect_to_neightbor()
        self.neighbor.send(str(self.current_max))
        return
        
    def server_activate(self):
        self.logger.debug('server_activate')
        self.send_to_neighbor()
        SocketServer.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('waiting for request')
        SocketServer.TCPServer.serve_forever(self)

    def handle_request(self):
        self.logger.debug('handle_request')
        return SocketServer.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return SocketServer.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return SocketServer.TCPServer.close_request(self, request_address)

if __name__ == '__main__':
    USAGE = '''python LeaderServer.py <ip-address> <port>'''
    from sys import argv, exit
    ADDRESS, PORT = '10.31.69.179', 9001
    if(len(argv) == 1):
        print("Using Default Server Address")
    elif(len(argv) == 5):
        try:
            PORT = int(argv[2])
        except ValueError:
            print "Bad Port Value"
            exit(USAGE)
    else:
        exit(USAGE)
        
        
    server = LeaderServer((ADDRESS, PORT),
                         handler_class=LeaderRequestHandler,
                         neighbor=('10.31.69.179',9001,),
                         server_id=66
                         )
    server.serve_forever()
    