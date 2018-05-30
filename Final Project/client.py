import socket
import threading
import hashlib
import os
import sys
import Pyro4

host1 = "192.168.56.101"

middleware = Pyro4.core.Proxy("PYRO:middleware@localhost:39501")
# server = Pyro4.core.Proxy("PYRO:dispatcher@" + host1 + ":39501")

def main():
	cmds = ['help', 'get', 'put', 'ls', 'quit']
	# print server
	# print middleware.get_node("a.txt")
	# a=middleware.get_node('a.txt')
	# print a
	print("Command: (type 'help' to get commands list)")
	commands = raw_input()

	command = commands.split()
	
	if command[0] == 'help':
		i = 1
		# print "\n"
		for cmd in cmds:
			print (str(i) + ". " + cmd)
			i+=1

	elif command[0] == 'quit':
		sys.exit()

	elif command[0] == 'get':
		print("Type file name to download:")
		filename = raw_input()
		a = middleware.get_node(filename)
		download(filename, a)

	elif command[0] == 'put':
		print("Type file name to upload:")
		filename = raw_input()
	# t = threading.Thread(target=upload, args=(filename, ))
	# t.start()
		a = middleware.get_node(filename)
		upload(filename, a)

	elif command[0] == 'ls':
		a = "PYRO:dispatcher@" + host1 + ":39501"
		if len(command)==1:
			path = "."
		else:
			path = command[1]
		listdir(path, a)

	else:
		print("Command " + command[0] + " not found. Please try again.")

def download(filename, conn):
	server = Pyro4.core.Proxy(conn)
	s = socket.socket()
	s.connect((host1, 56789))

	if filename != 'q':
		server.download(filename)
		s.send(filename)
		data = s.recv(1024)
		if data[:6] == 'EXISTS':
			filesize = long(data[6:])
			message = raw_input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
			if message == 'Y':
				s.send("OK")
				f = open('new_'+filename, 'wb')
				# data = s.recv(1024)
				# totalRecv = len(data)
				# f.write(data)
				totalRecv = 0
				while totalRecv < filesize:
					data = s.recv(1024)
					totalRecv += len(data)
					f.write(data)
					print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
				if totalRecv >= filesize:
					print "Download Complete!"
				f.close()
		else:
			print "File Does Not Exist!"

	s.close()

def upload(filename, conn):
	server = Pyro4.core.Proxy(conn)
	if os.path.isfile(filename):
		s = socket.socket()
		s.connect((host1, 56789))
		server.upload(filename)
		
		s.send( "EXISTS " + str(os.path.getsize(filename)) )
		userResponse = s.recv(1024)
		if userResponse[:2] == 'OK':
			with open(filename, 'rb') as f:
				print( "Sending file " + filename + " to " + str(s.getpeername()) )
				bytesToSend = f.read(1024)
				s.send(bytesToSend)
				while bytesToSend != "":
					bytesToSend = f.read(1024)
					s.send(bytesToSend)

	else:
		print("404")

	s.close()

def listdir(path, conn):
	server = Pyro4.core.Proxy(conn)
	a = server.listdir(path)
	for i in a:
		print i

if __name__ == '__main__':
	while True:
		main()