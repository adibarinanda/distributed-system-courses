import socket
import threading
import hashlib
import os
import sys
import Pyro4

host1 = "10.151.36.33"
host2 = "10.151.36.51"
host3 = "192.168.56.101"

middleware = Pyro4.core.Proxy("PYRO:middleware@localhost:39501")
# server = Pyro4.core.Proxy("PYRO:dispatcher@" + host1 + ":39501")

def main():
	cmds = ['help', 'get', 'put', 'rename', 'cp', 'ls', 'rm', 'quit']
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
		if len(filename)==1:
			download(filename, a)
		else:
			files = filename.split()
			for f in files:
				a = middleware.get_node(f)
				# if f == 'get':
				# 	continue
				download(f, a)

	elif command[0] == 'put':
		print("Type file name to upload:")
		filename = raw_input()
	# t = threading.Thread(target=upload, args=(filename, ))
	# t.start()
		if len(filename)==1:
			upload(filename, a)
		else:
			files = filename.split()
			print files
			for f in files:
				a = middleware.get_node(f)
				# if f == 'put':
				# 	continue
				upload(f, a)

	elif command[0] == 'rename':
		print("Type file name to rename:")
		filename = raw_input()
		print("Type NEW file name:")
		filename2 = raw_input()
	# t = threading.Thread(target=upload, args=(filename, ))
	# t.start()
		a = middleware.get_node(filename)
		rename(filename, filename2, a)

	elif command[0] == 'cp':
		print("Type file name to copy:")
		filename = raw_input()
		print("Type NEW file name:")
		filename2 = raw_input()
	# t = threading.Thread(target=upload, args=(filename, ))
	# t.start()
		a = middleware.get_node(filename)
		copy(filename, filename2, a)

	elif command[0] == 'rm':
		print("Type file name to delete:")
		filename = raw_input()
		a = middleware.get_node(filename)
		delete(filename, a)

	elif command[0] == 'ls':
		a = "PYRO:dispatcher@" + host1 + ":39501"
		b = "PYRO:dispatcher@" + host2 + ":39501"
		c = "PYRO:dispatcher@" + host3 + ":39501"
		if len(command)==1:
			path = "."
			conn = a
		elif len(command)==3:
			path = command[1]
			if command[2]=='1':
				conn = a
			elif command[2]=='2':
				conn = b
			elif command[2]=='3':
				conn = c
		else:
			path = command[1]
			conn = a
		listdir(path, conn)

	elif command[0] == 'mkdir':
		a = "PYRO:dispatcher@" + host1 + ":39501"
		b = "PYRO:dispatcher@" + host2 + ":39501"
		c = "PYRO:dispatcher@" + host3 + ":39501"
		if len(command)==1:
			print "Parameter is not complete"
		elif len(command)==3:
			path = command[1]
			if command[2]=='1':
				conn = a
			elif command[2]=='2':
				conn = b
			elif command[2]=='3':
				conn = c
		# else:
		# 	path = command[1]
		# 	conn = a
		makedir(path, conn)

	elif command[0] == 'chdir':
		a = "PYRO:dispatcher@" + host1 + ":39501"
		b = "PYRO:dispatcher@" + host2 + ":39501"
		c = "PYRO:dispatcher@" + host3 + ":39501"
		path = "."
		if len(command)==1:
			print "Parameter is not complete"
		elif len(command)==3:
			path = command[1]
			if command[2]=='1':
				conn = a
			elif command[2]=='2':
				conn = b
			elif command[2]=='3':
				conn = c
		else:
			path = command[1]
			conn = a
		chdir(path, conn)

	else:
		print("Command " + command[0] + " not found. Please try again.")

def download(filename, conn):
	server = Pyro4.core.Proxy(conn)
	s = socket.socket()

	hosts = str(conn.split(':')[1].split('@')[1])

	s.connect((hosts, 56789))

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
		
		hosts = str(conn.split(':')[1].split('@')[1])

		s.connect((hosts, 56789))
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

def rename(file_from, file_to, conn):
	server = Pyro4.core.Proxy(conn)
	response = server.rename(file_from, file_to)
	if(response == True):
		print(file_from + ' renamed to ' + file_to)
	else:
		print('rename failed')

def copy(file_from, file_to, conn):
	server = Pyro4.core.Proxy(conn)
	response = server.copy(file_from, file_to)
	if(response == True):
		print(file_from + ' copied to ' + file_to)
	else:
		print('copy failed')

def delete(filename, conn):
	server = Pyro4.core.Proxy(conn)
	response = server.delete(filename)
	print filename + " deleted."

def listdir(path, conn):
	server = Pyro4.core.Proxy(conn)
	a = server.listdir(path)
	for i in a:
		print i

def makedir(path, conn):
	server = Pyro4.core.Proxy(conn)
	a = server.makedir(path)

def chdir(path, conn):
	server = Pyro4.core.Proxy(conn)
	a = server.chdir(path)
	# for i in a:
		# print i

if __name__ == '__main__':
	while True:
		main()