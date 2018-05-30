import hashlib
import string
import Pyro4

petalokasi = {}
host = "localhost"
host1 = "10.151.36.33"
host2 = "10.151.36.51"
host3 = "192.168.56.101"
host4 = "192.168.56.101"

@Pyro4.expose
class Middleware(object):
    def __init__(self):
        for i in string.ascii_lowercase:
            if i == 'f':
                petalokasi[i] = 'PYRO:dispatcher@' + host2 + ':39501'
                break
            elif i == 'e':
                petalokasi[i] = 'PYRO:dispatcher@' + host2 + ':39501'
            else:
                petalokasi[i] = 'PYRO:dispatcher@' + host1 + ':39501'
        
        for x in range(2):
            petalokasi[str(x)] = 'PYRO:dispatcher@' + host2 + ':39501'

        for x in range(2, 6):
            petalokasi[str(x)] = 'PYRO:dispatcher@' + host3 + ':39501'

        for x in range(6, 10):
            petalokasi[str(x)] = 'PYRO:dispatcher@' + host4 + ':39501'

        # for k, v in petalokasi.items():
        #     print v

    def get_node(self, namafile):
    # def a():
        # petalokasi = {}
        # petalokasi['1']='PYRO:dispatcher@' + host1 + ':39501'
        # petalokasi['2']='PYRO:dispatcher@' + host1 + ':39501'
        # petalokasi['3']='PYRO:dispatcher@' + host1 + ':39501'
        # petalokasi['4']='PYRO:dispatcher@' + host1 + ':39501'

        # print petalokasi
        # return petalokasi

        # namafile_encoded = namafile.encode('utf-8')
        h = hashlib.md5(namafile).hexdigest()[-1]
        print petalokasi[h]

        cek = cekkoneksi(petalokasi[h])
        if(cek):
            return petalokasi[h]
        else:
            for k, v in petalokasi.items():
                # print v
                cek = cekkoneksi(v)
                # print cek
                # print i
                if (cek):
                    # print i
                    return v

        return False


        # h2 = hashlib.md5(namafile).hexdigest()[-2]
        # cek   = cekkoneksi(h2)
        # if (cek):
        #     return petalokasi[h2]
        
        return False

        # if(status)
        #     storages = []
        #     if h=='a' or h=='b' or h=='c' or h=='d'
        #         storages.extend([petalokasi[1], petalokasi[4]])
        #     elif h=='e' or h=='f' or h=='0' or h=='1'
        #         storages.extend([petalokasi[2], petalokasi[3]])
            #     elif h=='2' or h=='3' or h=='4' or h=='5'
        #         storages.extend([petalokasi[3], petalokasi[2]])
        #     elif h=='6' or h=='7' or h=='8' or h=='9'
        #         storages.extend([petalokasi[4], petalokasi[1]])
        #     return storages
        # else
            


        # if h=='a' or h=='b' or h=='c' or h=='d' or h=='6' or h=='7' or h=='8' or h=='9':
        #     return petalokasi[1]
        
        # elif h=='e' or h=='f' or h=='0' or h=='1' or h=='2' or h=='3' or h=='4' or h=='5':
        #     return petalokasi[2]

        # elif h=='2' or h=='3' or h=='4' or h=='5' or h=='e' or h=='f' or h=='0' or h=='1':
        #     return petalokasi[3]

        # elif h=='6' or h=='7' or h=='8' or h=='9' or h=='a' or h=='b' or h=='c' or h=='d':
        #     return petalokasi[4]


    def storefile(namafile, isifile):
        lokasi = get_node(namafile, 1)
        storage = Pyro4.Proxy(lokasi)
        storage.storefile(namafile, isifile)

    def getfile(namafile):
        lokasi = get_node(namafile, 0)
        storage = Pyro4.Proxy(lokasi)
        isifile = storage.getfile(namafile)
        return isifile

def cekkoneksi(hashed):
    with Pyro4.Proxy(hashed) as h:
        try:
            h._pyroBind()
            return True
        except Pyro4.errors.CommunicationError:
            return False

def init():
    petalokasi = {}
    for i in string.ascii_lowercase:

        petalokasi[i] = ""
        # print i
        if i == 'f':
            break
    for x in range (10):
        petalokasi[str(x)] = ""

    # for i in petalokasi:
        # print i
    print petalokasi

def main():
    # print('nama file:')
    custom_daemon = Pyro4.Daemon(host=host, port=39501)  # some additional custom configuration
    Pyro4.Daemon.serveSimple(
        {
            Middleware: "middleware"
        }, ns = False
        ,
        daemon = custom_daemon)
    s.close()


if __name__ == "__main__":
    # init()
    main()
    # a()
