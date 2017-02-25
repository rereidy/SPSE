import sys
import fcntl
import socket
import struct
import netifaces

class PromiscuousToggle():
    IFF_PROMISC = 0x100
    SIOCGIFFLAGS = 0x8913
    SIOCSIFFLAGS = 0x8914
    
    FLAGS_LEN = 18
    INTERFACE_NAME_OFFSET = 16
    
    def __init__(self, interface, verbose=False):
        self.__ifconfig__ = {}

        for i in netifaces.interfaces():
            if i == interface:
                self.__ifconfig__ = { i : netifaces.ifaddresses(i) }
        
        try:
            if interface not in self.__ifconfig__:
                raise AttributeError("no such network interface: {0}".format(interface))
            else:
                self.__interface_name__ = interface
                self.__interface__ = self.__ifconfig__[self.__interface_name__]
                (self.__rsock__, self.__ifreq__) = self.__get_raw__()
                self.__verbose__ = verbose
        except AttributeError:
            raise

    def toggle(self):
        (flags,) = struct.unpack('16xH', self.__ifreq__[:self.FLAGS_LEN])
        if flags & self.IFF_PROMISC:
            flags = flags | self.IFF_PROMISC
            if self.__verbose__:
                print "toggle: {0} into promiscuous mode".format(self.__interface_name__)
        else:
            flags = flags & ~self.IFF_PROMISC
            if self.__verbose__:
                print "toggle: {0} out of promiscuous mode".format(self.__interface_name__)

        try:
            self.__ifreq__ = struct.pack('%ss%sxH' %(len(self.__interface_name__),self.INTERFACE_NAME_OFFSET - len(self.__interface_name__)), self.__interface__, flags)
            fcntl.ioctl(self.__rsock__.fileno(), self.SIOCSIFFLAGS, self.__ifreq__)
        except struct.error:
            #print >> sys.stderr, e
            raise

    def __get_raw__(self):
        iface_len = len(self.__interface_name__)
        ifreq = 0x00
        rsock = None
        
        try:
            rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ifreq = struct.pack('%ss%sxH'%(iface_len, self.INTERFACE_NAME_OFFSET - iface_len),interface,0)
            ifreq = fcntl.ioctl(rsock.fileno(), self.SIOCGIFFLAGS, ifreq)
        except socket.error:
            #print >> sys.stderr, e
            raise
                
        return (rsock, ifreq)

def usage():
    print >> sys.stderr, """
{0} - toggle network interface to/from promiscuous mode
usage is: {0} -i interface [-v] [-h]
    """.format(sys.argv[0])

def process_args(args):
    import getopt

    interface = None
    verbose = False
    
    try:
        opts, args = getopt.getopt(args, 'hi:v')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-i':
                interface = arg
            elif opt == '-v':
                verbose = True
    except TypeError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)
    except getopt.GetoptError:
        print >> sys.stderr, "invalid argument"
        usage()
        sys.exit(1)

    return (interface, verbose)

if __name__ == "__main__":
    try:
        (interface, verbose) = process_args(sys.argv[1:])
        PromiscuousToggle(interface, verbose).toggle()
    except AttributeError, e:
        print >> sys.stderr, e