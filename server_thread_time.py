from socket import *
import socket
import threading
import logging
import time
import sys

def ShowTheTime():
	from datetime import datetime
	now = datetime.now()
	waktu = now.strftime("%H:%M:%S")
	balas = f"JAM {waktu}\r\n"
	return balas

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)
	def run(self):
		try:
			while True:
				data = b''
				while not data.endswith(b'\r\n'):
					inputUser = self.connection.recv(1)
					if not inputUser:
						break
					data += inputUser
				if not data:
					break
				cleanData = data.decode('utf-8').strip()
				logging.warning(f"Received from {self.address}: {cleanData}")
				if cleanData == 'TIME':
					response = ShowTheTime()
					self.connection.sendall(response.encode('utf-8'))
				elif cleanData == 'QUIT':
					logging.warning(f"Connection closed by client: {self.address}")
					break
				else:
					self.connection.sendall(b"Invalid command\r\n")
		except Exception as e:
			logging.error(f"Error: {e}")
		finally:
			self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0', 45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()