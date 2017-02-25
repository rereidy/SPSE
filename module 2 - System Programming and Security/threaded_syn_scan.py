from __future__ import print_function
import sys
import getopt
import thread
from scapy.all import *

class SynScan(object):
    def __init__(self, host='127.0.1.0', s, e):
        self.__host = host
        self.__starting_ip = s
        self.__ending_ip = e
        
        self.__port_list = self.__create_port_lists__()
        
    def __create_port_lists(self):
        lists = []
        
        return lists     
        
    def syn(self):
        pass

def usage():
    print("""
{0}: scapy SYN scanner
usage is: {0} -s server -b starting_ip -e ending_ip [h]
NOTE: 's' defaults to localhost
    """.format(sys.argv[0], sys.argv[0]))

def parse_args(args):
    host = None
    start_ip = None
    end_ip = None

    try:
        opts, args = getopt.getopt(args, 'hs:b:e:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-s':
                host = arg
            elif opt == '-b':
                start_ip = arg
            elif opt == '-e':
                end_ip = arg
    except TypeError as e:
        print(e, file=sys.stderr)
        usage()
        sys.exit(3)
    except getopt.GetoptError:
        print("invlaid argument", file=sys.stderr)
        usage()
        sys.exit(1)

    return host, start_ip, end_ip

if __name__ == "__main__":
    try:
        (server, start_ip, end_ip) = parse_args(sys.argv[1:])
        
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    finally:
        sys.exit(0)