import logging
import SocketServer
import numpy as np
from time import time


logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s'
                    )


class TimeRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('FloodingRequestHandler')
        self.logger.debug('__init__')
        request.settimeout(3)
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        self.logger.debug('handle')
        data = self.request.recv(128)
        received_at = time()
        self.logger.debug('recv()->"%s"', data)
        value = None
        try:
            value = float(data)
        except ValueError:
            self.logger.debug('Bad value %s', data)
            return
        self.server.measurements.append([value, 1, (-1)**(len(self.server.measurements)+1)])
        self.server.send_to_others(data)
        return


class TimeServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=TimeRequestHandler,
                 others_list=[]):
        self.logger = logging.getLogger('FloodingServer')
        self.logger.debug('__init__')
        self.others_list = others_list
        self.measurements = []
        self.timeout = 2
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    @staticmethod
    def send_to_other(message, other_address):
        import socket
        import logging
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        l = logging.getLogger("send_to_other")
        s.settimeout(2.0)
        bts = 0.0
        try:
            s.connect(other_address)
            bts = s.send("%s\n" % str(message))
        except socket.timeout as e:
            l.debug("Connection to %s timed out." % str(other_address))
        l.debug("Sent %s bytes" % bts)
        s.close()
    
    def send_to_others(self, message="\n"):
        self.logger.debug('send_to_others')
        import threading
        for other_server_address in self.others_list:
            t = threading.Thread(target=self.send_to_other, args=(message, other_server_address,))
            t.setDaemon(True)
            t.start()
        from time import sleep
        sleep(0.2)

if __name__ == '__main__':
    USAGE = '''python FloodingServer.py <port> <recipients_file>'''
    PORT = 9003
    oth_list = [("192.168.1.71", 9001), ("192.168.1.95", 9001)]
    from sys import argv, exit
    if len(argv) == 1:
        print "Using Default Server Address/Recipients"
        print "Port: %s" % PORT
        for r in oth_list:
            print "Recipient: %s : %s" % (r[0], r[1])
    elif len(argv) == 2 or len(argv) == 3:
        try:
            PORT = int(argv[1])
        except ValueError:
            print "Bad Port Value"
            exit(USAGE)
        if len(argv) == 3:
            try:
                recipients_file = open(argv[2], "r")
            except IOError:
                exit("Error opening file %s." % argv[2])
            recipients_entries = map(lambda x: x.split(), recipients_file.readlines())
            oth_list = [0] * len(recipients_entries)
            for ind in range(len(recipients_entries)):
                try:
                    oth_list[ind] = (recipients_entries[ind][0], int(recipients_entries[ind][1]))
                except (ValueError, IndexError):
                    exit("Error reading file %s" % argv[2])

    else:
        exit(USAGE)

    import socket
    ADDRESS = socket.gethostbyname(socket.gethostname())
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # result = sock.connect_ex((ADDRESS, PORT))
    # if result != 0:
    #     exit("Port %s is not free" % PORT)
    server = TimeServer((ADDRESS, PORT),
                        handler_class=TimeRequestHandler,
                        others_list=oth_list
                        )
    server.serve_forever()
