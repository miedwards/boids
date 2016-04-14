'''
Created on Mar 10, 2016

@author: Mark Edwards
'''


if __name__ == '__main__':
#     import threading
    import multiprocessing
    import time
    from AdderServer import AdderRequestHandler, AdderServer
    import logging
    import socket
    

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ext_ip = s.getsockname()[0]
    s.close()
    logger = logging.getLogger('client')
    logger.info('My External IP is: %s', ext_ip)
    
    def start_server(server_args):
        address, o_list, server_id = server_args
        server = AdderServer(address, AdderRequestHandler, 
                            others_list= o_list, server_id=server_id,
                            my_value=1)
        server.serve_forever()
        
    
    portlist = range(7771,7775)
    server_arg_list = [None]*len(portlist)
    
    for port_ind in range(len(portlist)):
        port = portlist[port_ind]
        address = ('localhost', port)
        o_list = [('localhost', x) for x in portlist[:port_ind] + portlist[port_ind+1:]]
        server_id = port_ind
        server_arg_list[port_ind] = (address, o_list, server_id)
        
    worker_pool = multiprocessing.Pool(len(portlist))
    worker_pool.map_async(start_server, server_arg_list)
    time.sleep(2)    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('localhost', 7771)) 
    s.send('1')
    s.close()
    worker_pool.close()
    worker_pool.join()
    
    
    