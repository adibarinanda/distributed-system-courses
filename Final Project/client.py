import socket
import Pyro4

server = Pyro4.core.Proxy("PYRO:dispatcher@192.168.56.101:39501")

def main():
	print("Type file name to download:")
	filename = raw_input()
	# filename = "a.txt"
	download(filename)

def download(file_name):
    s = socket.socket()
    s.connect(('192.168.56.101', 56789))

    if file_name != 'q':
    	server.download(file_name)
        s.send(file_name)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                s.send("OK")
                f = open('new_'+file_name, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                print "Download Complete!"
                f.close()
        else:
            print "File Does Not Exist!"

    s.close()


if __name__ == '__main__':
	main()