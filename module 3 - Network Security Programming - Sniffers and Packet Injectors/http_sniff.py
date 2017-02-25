#!/usr/bin/env python

import socket
import struct
import binascii
import fcntl
import sys

SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914
IFF_PROMISC = 0x100

current_flags = 0

def set_promiscuous(packet, yes_no=False):
    # return the current flags present on the interface
    ifreq = fcntl.ioctl(packet, SIOCGIFFLAGS, "eth0" + "\0" * 256)
    # extract current flags field from struct returned
    (current_flags,) = struct.unpack("16xH", ifreq[:18])
    # add the PROMISC flag
    if yes_no is True:
        current_flags |= IFF_PROMISC
    else:
        current_flags ^= IFF_PROMISC
    
    ifreq = struct.pack("4s12xH", "eth0", current_flags)
    fcntl.ioctl(packet, SIOCSIFFLAGS, ifreq)

def dump_packet(packet, port):
    data = 'null'
    while len(data):
        data = packet.recvfrom(2048)
        eth_header = data[0][0:14]
        eth_hdr = struct.unpack("!6s6s2s", eth_header)
        iph = data[0][14:34]
        ip_hdr = struct.unpack("!1s1sH2s2s1s1s2s4s4s", iph)
        tcph = data[0][34:54]
        tcp_hdr = struct.unpack("!HHLL1s1sHHH", tcph)
        http_data = data[0][54:]
        
        if tcp_hdr[0] == port:
            print "\n\n\n***** Eth Header Information *****"
            print eth_hdr
            
            print "Dest MAC address: %s" % binascii.hexlify(eth_hdr[0])
            print "Source MAC address: %s" % binascii.hexlify(eth_hdr[1])
            print "Protocol: %s" % binascii.hexlify(eth_hdr[2])
            
            print "\n***** IP Header Information *****"
            print ip_hdr
            print "Junk: %s" % binascii.hexlify(ip_hdr[0])
            print "Service: %s" % binascii.hexlify(ip_hdr[1])
            print "Total Length: %s" % str(ip_hdr[2])
            print "Identification: %s" % binascii.hexlify(ip_hdr[3])
            print "Junk: %s" % str(ip_hdr[4])
            print "TTL: %s" % binascii.hexlify(ip_hdr[5]) #str(ip_hdr[5])
            print "Protocol: %s" % binascii.hexlify(ip_hdr[6])
            print "Header Checksum: %s" % int(binascii.hexlify(ip_hdr[7]),16)
            print "Source IP address: %s" % socket.inet_ntoa(ip_hdr[8])
            print "Dest IP address: %s" % socket.inet_ntoa(ip_hdr[9])
            
            print "\n***** TCP Header Information *****"
            print tcp_hdr
            print "Source port: %s" % str(tcp_hdr[0])
            print "Dest port:  %s" % str(tcp_hdr[1])
            print "Seq Number: %s" % str(tcp_hdr[2])
            print "Acq Number: %s" % str(tcp_hdr[3])
            print "Junk: %s" % binascii.hexlify(tcp_hdr[4])
            print "TCP Flags: %s" % binascii.hexlify(tcp_hdr[5]) #str(tcp_hdr[5])
            print "Window: %s" % str(tcp_hdr[6])
            print "Checksum: %s" % str(tcp_hdr[7])
            print "Urgent Pointer: %s" % str(tcp_hdr[8])
            print "Packet Data:\n"
            print http_data
            
            print "\n***** HTTP Information *****"
            print "Src: %s:%s   Dst: %s:%s" % (socket.inet_ntoa(ip_hdr[8]), str(tcp_hdr[0]), socket.inet_ntoa(ip_hdr[9]), str(tcp_hdr[1]))
            print "Packet Data:"
            print http_data
            
            data = ''

if __name__ == "__main__":
    sniff_port = int(sys.argv[1])
    rs = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
    set_promiscuous(rs, True)
    dump_packet(rs, sniff_port)
    set_promiscuous(rs, False)