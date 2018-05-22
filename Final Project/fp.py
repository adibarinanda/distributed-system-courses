import hashlib
import Pyro4

def get_node(namafile):
    petalokasi = []
    petalokasi[1]='PYRO:example.warehouse@localhost:51280'
    petalokasi[2]='PYRO:example.warehouse@localhost:51281'
    petalokasi[3]='PYRO:example.warehouse@localhost:51282'
    petalokasi[4]='PYRO:example.warehouse@localhost:51283'
    namafile_encoded = namafile.encode('utf-8')
    h = hashlib.md5(namafile_encoded).hexdigest()[-1]
    if h=='a' or h=='b' or h=='c' or h=='d' or h=='6' or h=='7' or h=='8' or h=='9':
        return petalokasi[1]
    
    elif h=='e' or h=='f' or h=='0' or h=='1' or h=='2' or h=='3' or h=='4' or h=='5':
        return petalokasi[2]

    elif h=='2' or h=='3' or h=='4' or h=='5' or h=='e' or h=='f' or h=='0' or h=='1':
        return petalokasi[3]

    elif h=='6' or h=='7' or h=='8' or h=='9' or h=='a' or h=='b' or h=='c' or h=='d':
        return petalokasi[4]

def storefile(namafile, isifile):
    lokasi = get_node(namafile)
    storage = Pyro4.Proxy(lokasi)
    storage.storefile(namafile)

def getfile(namafile):
    lokasi = get_node(namafile)
    storage = Pyro4.Proxy(lokasi)
    content = storage.getfile(namafile)
    return content