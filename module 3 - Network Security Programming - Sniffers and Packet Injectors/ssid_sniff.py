from scapy.all import *
import scapy
import sys
import getopt

class SID():
    def __init__(self, interface):
        self.interface = interface
        
    def discover(self, cnt=10):
        pkts = sniff(iface=self.interface, count=cnt)
        self.__sid__(pkts)
        
    def __sid__(self, p):
        found_beacons = []
        
        for i in p:
            if i.haslayer(Dot11Beacon):
                if found_beacons(i.payload.payload.info) == 0:
                    found_beacons.append(i.payload.payload.info)
                    print i.sprintf('%Dot11Elt.info%, %Dot11.addr2% , %Dot11Beacon.cap%')       

def process_args(argv):
    interface = None
    packet_count = -1
    
    try:
        opts, args = getopt.getopt(argv, 'hi:c:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-i':
                interface = arg
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
        
    return (interface, packet_count)

def usage():
    print >> sys.stderr, """
{0} - scapy SSID sniffer
usage is: {0} -i network_interface -c count[-h]
    """.format(sys.argv[0])
            
if __name__ == "__main__":
    try:
        (interface, count) = process_args(sys.argv[1:])
        
        if interface is not None or count < 0:
            raise TypeError('missing or invalid arguments')
        
        s = SID(interface).discover(count)
    except TypeError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)
        