import struct
import socket
import sys
import fcntl
import getopt

class Arp():
    def __init__(self, interface, server):
        self.interface = interface
        self.server = server
        (self.mac, self.ip) = self.__addr__()
        
    def __addr__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', self.interface[:15]))
        mac = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
        ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', self.interface[:15]))[20:24])

        return (mac, ip)

    def bld_packet(self):
        eth_hdr = struct.pack("!6s6s2s", '\xff\xff\xff\xff\xff\xff', self.mac.replace(':','').decode('hex'), '\x08\x06')
        arp_hdr = struct.pack("!2s2s1s1s2s", '\x00\x01', '\x08\x00', '\x06', '\x04', '\x00\x01')
        sender = struct.pack("!6s4s", self.mac.replace(':','').decode('hex'), socket.inet_aton(self.ip))
        target = struct.pack("!6s4s", '\x00\x00\x00\x00\x00\x00', socket.inet_aton(self.server))

        return(eth_hdr, arp_hdr, sender, target)
    
    def inject(self, packet):
        try:
            if type(packet) is not tuple:
                raise TypeError("argument must be a tuple")
            
            if len(packet) != 4:
                raise IndexError("packet must be length of 4")
            
            s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))
            s.bind((self.interface, socket.htons(0x806)))
            s.send(''.join(['%s' %p for p in packet]))
        except TypeError, e:
            print >> sys.stderr, e
        except IndexError, e:
            print >> sys.stderr, e
    
def process_args(argv):
    interface = None
    server_ip = None
    
    try:
        opts, args = getopt.getopt(argv, 'hi:s:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-i':
                interface = arg
            elif opt == '-s':
                server_ip = arg
    except getopt.GetoptError:
        print >> sys.stderr, "invalid argument"
        usage()
        sys.exit(1)
        
    return(interface, server_ip)

def usage():
    print >> sys.stderr, """
{0} - ARP packet injector
usage is: {0} -i network_interface -s server_ip [-h]
    """.format(sys.argv[0])

if __name__ == "__main__":
    try:
        (interface, server) = process_args(sys.argv[1:])
        if interface is None or server is None:
            raise TypeError("missing arguments")
        arp = Arp(interface, server)
        arp.inject(arp.bld_packet())
    except TypeError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)
    