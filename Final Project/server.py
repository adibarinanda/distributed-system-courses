import socket
import threading
import os
import time
import Pyro4
from shutil import copyfile

host1 = "10.151.36.33"
host2 = "10.151.36.51"
host3 = "192.168.56.101"

s = socket.socket()
s.bind((host2,56789))
s.listen(10)

def SendFile(name, sock):
	filename = sock.recv(1024)
	if os.path.isfile(filename):
		sock.send("EXISTS " + str(os.path.getsize(filename)))
		userResponse = sock.recv(1024)
		if userResponse[:2] == 'OK':
			print( "Sending file " + filename + " to " + str(sock.getpeername()) )
			with open(filename, 'rb') as f:
				bytesToSend = f.read(1024)
				sock.send(bytesToSend)
				while bytesToSend != "":
					bytesToSend = f.read(1024)
					sock.send(bytesToSend)
			print( filename + " sent to " + str(sock.getpeername()) )

	else:
		sock.send("ERR ")

	sock.close()

def RecvFile(name, sock, filename):
	data = sock.recv(1024)
	filesize = long(data[6:])
	sock.send("OK")
	f = open(filename, 'wb')
	totalRecv = 0
	while totalRecv < filesize:
#		time.sleep(5)
		data = sock.recv(1024)
		totalRecv += len(data)
		f.write(data)
		print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
	if totalRecv >= filesize:
		print "Upload Complete!"
	f.close()

@Pyro4.expose
class FileTransfer(object):
	#def __init__(self):
		#c = None
		#addr = None
		#print("Success")
		#return None

	def download(self, file_name):
		c, addr = s.accept()
		print "Download file to:<" + str(addr) + ">"
		t = threading.Thread(target=SendFile, args=("SendThread", c))
		t.start()

	def upload(self, file_name):
		c, addr = s.accept()
		print "Upload file from:<" + str(addr) + ">"
		t = threading.Thread(target=RecvFile, args=("RecvThread", c, file_name))
		t.start()

	def listdir(self, dir_path):
		return os.listdir(dir_path)

	def makedir(self, dir_path):
		os.mkdir(dir_path)

	def chdir(self, dir_path):
		os.chdir(dir_path)

	def rename(self, s_path, d_path):
		os.rename(s_path, d_path)

	def delete(self,filename):
		os.remove(filename)

	def copy(self, file1, file2):
		copyfile(file1, file2)

if __name__ == "__main__":
	custom_daemon = Pyro4.Daemon(host=host2, port=39501)  # some additional custom configuration

	# Pyro4.config.SERVERTYPE = "thread"
	Pyro4.Daemon.serveSimple(
		{
			FileTransfer: "dispatcher"
		}, ns = False
		,
		daemon = custom_daemon)
	s.close()
