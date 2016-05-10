import logging
import SocketServer

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s'
                    )


class FloodingRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('FloodingRequestHandler')
        self.logger.debug('__init__')
        request.settimeout(3)
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        self.logger.debug('handle')
        data = self.request.recv(128)
        self.logger.debug('recv()->"%s"', data)
        try:
            value = float(data)
        except ValueError:
            self.logger.debug("Error handling value: %s", data)
            return
        addr = self.request.getpeername()
        sender = str(addr[0])
        self.server.check_status(value, sender)
        return


class FloodingServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=FloodingRequestHandler,
                 others_list=[], senders_list=[], weights=[], my_value=[]):
        self.logger = logging.getLogger('FloodingServer')
        self.logger.debug('__init__')
        self.others_list = others_list
        print self.others_list
        self.senders_list = senders_list
        self.weights = weights
        self.timeout = 2
        self.received_values = {}
        self.my_value = my_value
        self.step_size = 0.1
        for i in senders_list:
            self.received_values[i] = None

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

    def check_status(self, value, sender):
        self.logger.debug("check_status")
        from numpy import array, multiply

        self.received_values[sender] = value
        for s in self.senders_list:
            if self.received_values[s] is None:
                return False
        self.my_value += self.step_size*sum(multiply(array(self.weights),array(self.received_values.values())))
        self.received_values = {}
        for s in self.senders_list:
            self.received_values[s] = None
        self.send_to_others(str(self.my_value))
        return True


if __name__ == '__main__':

    def __read_file(filename):
        try:
            recipients_file = open(filename, "r")
        except IOError:
            exit("Error opening file %s." % argv[2])
        entries = map(lambda x: x.split(), recipients_file.readlines())
        return entries


    def __read_ip_file(filename):
        entries = __read_file(filename)
        ip_list = [0] * len(entries)
        for ind in range(len(entries)):
            try:
                ip_list[ind] = tuple([entries[ind][0], int(entries[ind][1])])
                print ip_list[ind]
            except (ValueError, IndexError):
                exit("Error reading file %s" % argv[2])
        print entries
        return entries


    USAGE = '''python LeastSquaresServer.py <port> <recipients_file> <senders_file> <weight_file>'''
    oth_list = []
    from sys import argv, exit
    import socket
    import numpy as np
    value = 1

    if len(argv) == 5:
        try:
            PORT = int(argv[1])
        except ValueError:
            print "Bad Port Value"
            exit(USAGE)
        send_to = __read_ip_file(argv[2])
        receive_from = map(lambda x: x[0], __read_file(argv[3]))
        weights = np.array(map(lambda x: map(lambda y: float(y), x), __read_file(argv[4])))
    else:
        exit(USAGE)

    ADDRESS = socket.gethostbyname(socket.gethostname())
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # result = sock.connect_ex((ADDRESS, PORT))
    # if result != 0:
    #     exit("Port %s is not free" % PORT)
    server = FloodingServer((ADDRESS, PORT),
                            handler_class=FloodingRequestHandler,
                            others_list=send_to,
                            senders_list=receive_from,
                            weights=weights,
                            my_value=value
                            )
    server.serve_forever()
