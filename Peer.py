import socket
import pickle

class Peer(object):
	"""The peer object, represents a peer on the network, and has fields:
	stringIP--the IP address of the peer
	intPort--the port of the peer to connect to
	Socket--defaults to None, but can (and should) be overridden for the socket of the peer
	fields:
	IP--stringIP
	port--intPort
	hasSock--boolean if the peer currently has a socket object, but may also be reverted to None
	to shut down a malfunctioning peer
	"""
	
	def __init__(self, stringIP, intPort = None, Socket = None, isBlocking = None):
		self.IP = stringIP
		self.port = intPort
		self.isBlocking = True
			
		# If a socket is provided, use it. Otherwise, document that.
		#TODO Do we really need the bool hasSocket? Can't we just test for `self.socket is None`? 
		if Socket is not None:
			self.Sock = Socket
			self.hasSock = True 
			
		else:
			self.hasSock = False
		self.name = None
	
	def __str__(self):
		"""
		Returns a string representation of this peer including IPv4 address, port and whether a socket exists.
		
		Example with a socket:  Peer@192.168.1.4 12345(S)
		Example without socket: Peer@192.168.1.4 12345
		"""
		
		text = "Peer@" + self.IP + " " + str(self.port)
		if self.hasSock:
			text += "(S)"
		return text
	
	
	
	def __eq__(self, other):
	  """ Compares this peer to another peer for equality. (for == operator) """
	  
	  return self.IP == other.IP and self.port == other.port
	
	
	def __neq__(self, other):
	  """ Compares the peer to another peer for inequality. (for != operator) """
	  
	  return not self == other
	
	
	
	
	def sendable(self):
		""" Returns an instance of peer that is this peer, but a sendable version ie no socket"""
		return peer(self.IP,self.port)
	
	
	def send(self,message):
		""" Send a message to this peer. """
		if self.hasSock == True:
			try:
				self.Sock.send(pickle.dumps(message))
			except socket.error:
				print("error sending message " + message + " to peer " + str((self.IP,self.port)))
				self.hasSock = None
				print("peer removed")
		
	def receive(self):
		""" Receive a message from this peer and print it. """
		if self.hasSock==True:
			try:
				print("hasSockTrue")
				
				message = pickle.loads(self.Sock.recv(1024))
				print(message)
			except socket.error:
				print("error receiving message from " + str((self.IP,self.port)))
				#self.hasSock = None
				print("peer not removed")

	def addSock(self,Socket):
		""" Add a socket to the peer. """
		self.Sock = Socket 
		self.hasSock = True
		# Aware this looks suspiciously like a setter, I just didn't feel like not doing it...	
	
