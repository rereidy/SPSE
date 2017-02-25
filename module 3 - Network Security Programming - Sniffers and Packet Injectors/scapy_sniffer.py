import scapy
from scapy.all import *
import sys
import getopt

class SSniff():
    def __init__(self, interface, f='tcp port 80', cnt=10):
        self.interface = interface
        self.BF = f
        self.count = cnt
        
    def scapy_sniff(self):
        sniff(iface=self.interface, store=0, count=self.count, filter=self.BF, \
              lfilter=lambda z: z if z.haslayer(TCP) and z.haslayer(Raw) else False, \
              prn=lambda x: x.getlayer(Raw) \
             )

def process_args(argv):
    interface = None
    BF_filter = None
    packet_count = -1
    
    try:
        opts, args = getopt.getopt(argv, 'hi:f:c:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-i':
                interface = arg
            elif opt== '-f':
                BF_filter = arg
            elif opt == '-c':
                if re.match("^[0-9]*$", arg):
                    packet_count = int(arg)
                else:
                    raise TypeError("invalid type: port must be an integer")
    except getopt.GetoptError:
        print >> sys.stderr, "invalid argument"
        usage()
        sys.exit(1)
    except TypeError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)
        
    return (interface, BF_filter, packet_count)

def usage():
    print >> sys.stderr, """
{0} - scapy Sniffer
usage is: {0} -i network_interface -f filter -c count[-h]
    """.format(sys.argv[0])

if __name__ == "__main__":
    try:
        (interface, BF_filter, packet_count) = process_args(sys.argv[1:])

        if interface is None or BF_filter is None or packet_count < 0:
            raise TypeError("missing argument(s)")

        s = SSniff(interface, BF_filter)
        s.scapy_sniff()
    except TypeError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)