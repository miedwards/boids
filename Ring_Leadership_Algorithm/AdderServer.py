import logging
import SocketServer
from datetime import date

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    filename='adder-%(date)s.log' % {'date' : date.today()}
                    )

class AdderRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('AdderRequestHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')
        
        self.server.add_other_address(self.request.getpeername())
        
        data = self.request.recv(1024)
        self.logger.debug('recv()->"%s"', data)
        data_lst = data.split()
        if(len(data_lst)==2):
            new_address = data_lst[0]
            try:
                new_port = int(data_lst[1])
            except ValueError:
                self.logger.warn('New Port is not an integer')
                return
            data_tup = (new_address, new_port,)
            self.logger.debug('Contains an address')
            self.server.meet_other(data_tup)
            return
        try:
            received_value = int(data)
        except ValueError:
            self.logger.warn('Invalid Data->"%s"', data)
            self.request.send('ERROR')
            return
        
        if(received_value < 0 or received_value > 100):
            self.logger.warn('Invalid value->"%s"', received_value)
            self.request.send('ERROR')
            return
        
        if(received_value == 100):
            print "We're done."
            self.request.send('DONE')
            
            self.server.socket.close()
            self.server.shutdown() 
            self.server.server_close()
            return
        my_value = self.server.my_value
        if(received_value < my_value):
            self.logger.debug('Out of date value->"%s"', received_value)
            self.request.send(str(my_value))
            return
        if(my_value >= received_value):
            my_value = received_value + 1
            self.server.my_value = my_value
            self.logger.info('Value updated to %s', my_value)
            self.server.send_to_others()
        return
    


    def finish(self):
        self.logger.debug('finish')
        self.request.close()
        return SocketServer.BaseRequestHandler.finish(self)

class AdderServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=AdderRequestHandler,
                 others_list=[], server_id=None, my_value=0):
        self.logger = logging.getLogger('AdderServer')
        self.logger.debug('__init__')
        self.others_list = others_list
        self.my_value = my_value
        self.server_id = server_id
        self.timeout = 2
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return
    
    def add_other_address(self, new_address):
        self.logger.debug('add_other_address(%s)', new_address)
        if(type(new_address) != 'tuple' or 
           len(new_address) != 2 or 
           type(new_address[0]) != 'str' or
           type(new_address[1]) != 'int'):
            self.logger.warn('New address %s is not properly formatted', new_address)
            return None
        other_addresses = self.others_list
        if new_address in other_addresses:
            return None
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(new_address)
        except socket.error:
            s.close()
            return None
        other_addresses.append(new_address)
        self.others_list = other_addresses
        return new_address
    
    def send_to_others(self):
        self.logger.debug('send_to_others')
        import threading, socket
        def send_to_other(other_address):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(str(self.my_value), other_address)                
                s.close()
        for other_server_address in self.others_list:
            t = threading.Thread(target=send_to_other, args=(other_server_address,))
            t.setDaemon(True)
            t.start()
        from time import sleep
        sleep(1)
            
    def meet_other(self, new_address):
        self.logger.debug('meet_other(%s)', new_address)
        if(self.add_other_address(new_address)):
            self.send_to_others()
        return

    def server_activate(self):
        self.logger.debug('server_activate')
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
    USAGE = '''python AdderServer.py <ip-address> <port>'''
    from sys import argv, exit
    ADDRESS, PORT = 'localhost', 7770
    if(len(argv) == 1):
        print("Using Default Server Address")
    elif(len(argv) == 3):
        try:
            PORT = int(argv[2])
        except ValueError:
            print "Bad Port Value"
            exit(USAGE)
    else:
        exit(USAGE)
        
        
    server = AdderServer((ADDRESS, PORT),
                         handler_class=AdderRequestHandler,
                         others_list=[],
                         server_id=1,
                         my_value=1
                         )
    server.serve_forever()
    