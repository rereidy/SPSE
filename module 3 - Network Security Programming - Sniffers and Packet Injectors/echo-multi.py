from multiprocessing import Process
import SocketServer
import socket
import os
import sys
import getopt
import re 

class EchoServerHandler (SocketServer.BaseRequestHandler):
    MAX_BUF_LEN = 2048
    def handle(self):
        self.ct = os.getpid()
        print "connection from client : ", self.client_address
        data = "test data"
        while len(data):
            data = self.request.recv(self.MAX_BUF_LEN)
            print self.ct , " client sent: " , data
            self.request.send("message from server to client %d: \"%s\" to you\n" %(self.ct, data.strip()))
        print "client connection closed : ", self.client_address
        
    def close(self):
        self.finish()

class EchoServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

def usage():
    print >> sys.stderr, """
%s - multi-threaded echo server
usage: %s -p port_num
    """ %(sys.argv[0], sys.argv[0])
    
def process_args(argv):
    seconds = 0
    port = -1
    try:
        opts, args = getopt.getopt(argv, 'hp:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-p':
                if re.match("^[0-9]*$", arg):
                    port = int(arg)
                else:
                    raise TypeError("invalid type: port must be an integer")
    except TypeError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)
    except getopt.GetoptError:
        print >> sys.stderr, "invalid argument"
        usage()
        sys.exit(1)

    return (port)

if __name__ == '__main__':
    p = process_args(sys.argv[1:])
    if p <= 1024:
        print >> sys.stderr, "port must be >= 1024"
        sys.exit(1)

    try:
        server = EchoServer(('localhost', p), EchoServerHandler)
        server.allow_reuse_address = True
        server_thread = Process(targer = server.serve_forever())
        server_thread.daemon = True
        server_thread.start()
    except KeyboardInterrupt:
        pass
    finally:
        print "shutting down server ..."
        server.server_close()
        sys.exit(0)