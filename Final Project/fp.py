import hashlib
import Pyro4

def get_node(namafile):
    petalokasi[1]='PYRO:example.warehouse@localhost:51280'
    petalokasi[2]='PYRO:example.warehouse@localhost:51281'
    petalokasi[3]='PYRO:example.warehouse@localhost:51282'
    petalokasi[4]='PYRO:example.warehouse@localhost:51283'
    namafile_encoded = namafile.encode('utf-8')
    h = hashlib.md5(namafile_encoded).hexdigest()[-1]
    if(h == 'a' OR h == 'b' OR h == 'c' OR h == 'd'):
        return petalokasi[1]
    
    elif(h == 'e' OR h == 'f' OR h == '0' OR h == '1'):
        return petalokasi[2]

def storefile(namafile, isifile):
    lokasi = get_node(namafile)
    storage = Pyro4.Proxy(lokasi)
    storage.storefile(namafile,content)

def getfile(namafile):
    lokasi = get_node(namafile)
    storage = Pyro4.Proxy(lokasi)
    content = storage.getfile(namafile)
    return content