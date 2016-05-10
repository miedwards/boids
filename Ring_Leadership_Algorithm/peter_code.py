# Peter Sylvester
import socket, thread, time, json, sys

PORT = 9001
HOST = ''
ID = 42 #42
FINISH = 10

# Check what IP this computer has on the network
def getIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8',80))
	return s.getsockname()[0]

# Handle incoming data	
def tcpReceive(socket, ip):
	global inNodes, lock
	try:
		if ip not in inNodes:
			inNodes.update({ip:[0,'unkown']})
		print 'Got connection from: %s, %s' % (ip, inNodes[ip][1])
		
		#parse data
		msg = ''
		data = socket.recv(1024 * 10)
		i = 0
		while data:
			msg += data
			data = socket.recv(1024)		
			i += 1
	
		print 'msg:', msg
		
		while lock:
			time.sleep(.01)
		lock = True
		
		try:
			inNodes[ip][0] = int(msg)
		except:
			pass
		finally:
			lock = False
	
		#socket.send('I got your message %s\n' % inNodes[ip][1])
	except Exception, e:
		print 'Receive failed...', e
		
	finally:
		socket.close()

# Listen for incoming data	
def tcpServer(ip):
	try:
		while True:
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print 'Hosting TCP on %s:%s' % (ip, PORT)
			server.bind((HOST, PORT))
			server.listen(1)
	
			try:
				#serve
				while True:
					client, addr = server.accept()
					thread.start_new_thread(tcpReceive, (client, addr[0])) #spin off
			except Exception, e:
				print 'TCP ERROR:', e
				time.sleep(1)
				server.close()
	except:
		server.close()

# Read data from a file		
def setupGraph(file):
	global outNodes, inNodes
	
	with open(file, 'r') as raw:
		data = raw.read().split('\n')
		try:
			inNodes = {d[1]:[0,d[0]] for d in [p.split(':') for p in data[0].split(' ')]}
		except:
			print 'No inNodes specified'
			inNodes = {}
		try:
			outNodes = {d[0]:[0,d[1],int(d[2])] for d in [p.split(':') for p in data[1].split(' ')]}
		except:
			print 'No outNodes specified'
			outNodes = {}

	raw.close()

# Send to neighbors 	
def tcpSender():
	global inNodes, outNodes, state, lock
	
	count = 0
	
	while True:
		#get current messages
		try:
			while lock:
				time.sleep(.01)
			lock = True
			
			print 'State:', state

			if state['send']:
				sent = True
				for n in outNodes:
					try:
						sender = socket.socket()
						sender.settimeout(2)
						sender.connect((outNodes[n][1], outNodes[n][2]))
						sender.send('%s\n'%state['max'])
						print 'sent to', n
					except Exception, e:
						print 'Could not send to', n, e
						sent = False
					finally:
						sender.close()
				if not sent:
					continue #do not check states, sending has not started
			
			#get all msgs
			msgs = [inNodes[n][0] for n in inNodes]
			if len(msgs) > 0:
				maxID = max(msgs)
			else:
				maxID = 0
			
			#check new state
			if sum(msgs) == 0 or maxID < state['id']:
				state['send'] = False
				count += 1
			elif maxID == state['id']:
				state['send'] = False
				state['leader'] = True
				count += 1
			elif maxID > state['max']:
				state['send'] = True
				state['max'] = maxID
				count = 0

			#clear messages
			for n in inNodes:
				inNodes[n][0] = 0
				
			if count >= FINISH:
				print 'System Stablized, final state:', state
				sys.exit()
			
		except Exception, e:
			print 'Error sending:', e
			
		finally:
			lock = False
			time.sleep(1)
			
if __name__ == '__main__':
	global outNodes, lock, state
	if len(sys.argv) < 2:
		print ('Need input file')
		sys.exit()
	
	#init state
	lock = False
	state = {'id':ID, 'packet':'', 'parent':None, 'send':False}
		
	setupGraph(sys.argv[1])

	#setup tcp server
	ip = getIP()
	id = ip.split(':')
	state.id = id[len(id)-1]
	
	print 'Starting TCP Server at %s:%s' % (ip, PORT)
	thread.start_new_thread(tcpServer, (ip,))
	
	#setup senders
	tcpSender();