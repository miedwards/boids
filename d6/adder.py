import logging
import sys
import SocketServer
from datetime import date

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    filename='%(date)s.log' % {'date' : date.today()}
                    )

class EchoRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        # Echo the back to the client
        data = self.request.recv(1024)
        self.logger.debug('recv()->"%s"', data)
        if( data == '100' ):
            print "We're done."
            self.server.socket.close()
            return
        if( data == 'DONE' ):
            self.server.socket.close()
            return
        received_value = -1
        try:
            received_value = int( data )
        except ValueError:
            logger.warn('Invalid Data->"%s"', data)
            return
        if( received_value < 0 || received_value > 100 ):
            logger.warn('Invalid Data->"%s"', data)
            return
        if( received_value < self.server.my_value ):
            logger.debug('Out of date Data->"%s"', data)
            return
        if( self.server.my_value == received_value ):
            self.server.my_value += 1
            for other_server_address in self.server.others_list:
                other_server_address

        self.server.my_value = received_value
        logger.info('Value updated to %s', received_value)
        return

    def finish(self):
        self.logger.debug('finish')
        return SocketServer.BaseRequestHandler.finish(self)

class EchoServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=EchoRequestHandler, others_list=[],
            my_value=0):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        self.others_list = others_list
        self.my_value = my_value
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        SocketServer.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

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
    import socket
    import threading

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ext_ip = s.getsockname()[0]
    s.close()
    logger = logging.getLogger('client')
    logger.info('My External IP is: %s', ext_ip)

    portlist = range(7771,7775)
    for port_ind in range(portlist)
        port = portlist[port_ind]
        address = ('localhost', port)
        o_list = portlist[:port_ind] + portlist[port_ind+1:]
        server = EchoServer(address, EchoRequestHandler,
                others_list= o_list)
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()


    # Connect to a server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ext_ip, portlist[0]))


    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ext_ip, portlist[0])

    # Send the data
    message = 1
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # # Receive a response
    # logger.debug('waiting for response')
    # response = s.recv(len_sent)
    # logger.debug('response from server: "%s"', response)

    # Clean up
    #logger.debug('closing socket')
    #s.close()
    #logger.debug('done')
    #server.socket.close()
