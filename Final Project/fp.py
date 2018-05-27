import hashlib
import Pyro4

def get_node(namafile, status):
    petalokasi = []
    petalokasi[1]='PYRO:example.warehouse@localhost:51280'
    petalokasi[2]='PYRO:example.warehouse@localhost:51281'
    petalokasi[3]='PYRO:example.warehouse@localhost:51282'
    petalokasi[4]='PYRO:example.warehouse@localhost:51283'

    namafile_encoded = namafile.encode('utf-8')
    h = hashlib.md5(namafile_encoded).hexdigest()[-1]

    if(status)
        storages = []
        if h=='a' or h=='b' or h=='c' or h=='d'
            storages.extend([petalokasi[1], petalokasi[4]])
        elif h=='e' or h=='f' or h=='0' or h=='1'
            storages.extend([petalokasi[2], petalokasi[3]])
        elif h=='2' or h=='3' or h=='4' or h=='5'
            storages.extend([petalokasi[3], petalokasi[2]])
        elif h=='6' or h=='7' or h=='8' or h=='9'
            storages.extend([petalokasi[4], petalokasi[1]])
        return storages
    else
        


    if h=='a' or h=='b' or h=='c' or h=='d' or h=='6' or h=='7' or h=='8' or h=='9':
        return petalokasi[1]
    
    elif h=='e' or h=='f' or h=='0' or h=='1' or h=='2' or h=='3' or h=='4' or h=='5':
        return petalokasi[2]

    elif h=='2' or h=='3' or h=='4' or h=='5' or h=='e' or h=='f' or h=='0' or h=='1':
        return petalokasi[3]

    elif h=='6' or h=='7' or h=='8' or h=='9' or h=='a' or h=='b' or h=='c' or h=='d':
        return petalokasi[4]

def storefile(namafile, isifile):
    lokasi = get_node(namafile, 1)
    storage = Pyro4.Proxy(lokasi)
    storage.storefile(namafile, isifile)

def getfile(namafile):
    lokasi = get_node(namafile, 0)
    storage = Pyro4.Proxy(lokasi)
    isifile = storage.getfile(namafile)
    return isifile

def main():
    print('nama file:')


if __name__ == "__main__":
    main()