import Pyro4


class FileTransfer(object):
    """docstring for FileTransfer"""
    """ def __init__(self, arg):
        super(FileTransfer, self).__init__()
        self.arg = arg """
    def __init__(self):
        return "Success"
        

if __name__ == "__main__":
    print("Spinning up 5 wordcounters, and 1 dispatcher.")
    custom_daemon = Pyro4.Daemon(host="192.168.56.101")  # some additional custom configuration
    Pyro4.config.SERVERTYPE = "thread"
    Pyro4.Daemon.serveSimple(
        {
            FileTransfer: "dispatcher"
        }, ns = False
        ,
    daemon = custom_daemon)