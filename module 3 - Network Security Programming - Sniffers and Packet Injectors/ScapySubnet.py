import math
import scapy.route
import sys

class ScapySubnet():
    MASK = 0xFFFFFFFF
    
    def __init__(self):
        self.__routes__ = []
        for route in scapy.config.conf.route.routes:
            (network, mask, interface) = (route[0], route[1], route[3])
            if not self.__filter__(network, interface):
                self.__routes__.append({'net'   : scapy.utils.ltoa(network), \
                                        'iface' : interface, \
                                        'mask'  : 32 - int(round(math.log(self.MASK - mask, 2)))}\
                                       )
        
    def __filter__(self, n, i):
        rv = False
        if n == 0 or i == 'lo' or i != scapy.config.conf.iface:
            rv = True
        
        return rv
    
    def get_routes(self):
        return self.__routes__
    
    def dump(self):
        for r in self.get_routes():            
            print "Interface {0}: submask {1}/{2}".format(r['iface'], r['net'], r['mask'])
            
if __name__ == "__main__":
    ScapySubnet().dump()
    sys.exit(0)
