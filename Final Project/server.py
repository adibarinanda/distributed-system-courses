import socket
import threading
import os
import Pyro4

s = socket.socket()
s.bind(("192.168.56.101",56789))
s.listen(10)

def RetrFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")

    sock.close()


@Pyro4.expose
class FileTransfer(object):
    def init(self):
        print("Success")

    def download(self, file_name):
	c, addr = s.accept()
	print "client connedted ip:<" + str(addr) + ">"
	t = threading.Thread(target=RetrFile, args=("RetrThread", c))
	t.start()

if __name__ == "__main__":
    custom_daemon = Pyro4.Daemon(host="192.168.56.101", port=39501)  # some additional custom configuration

    # Pyro4.config.SERVERTYPE = "thread"
    Pyro4.Daemon.serveSimple(
        {
            FileTransfer: "dispatcher"
        }, ns = False
        ,
    daemon = custom_daemon)
    s.close()
