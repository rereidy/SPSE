from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

server_address = '127.0.0.1'
server_port = 8000

h = None

try:   
    h = HTTPServer((server_address, server_port), CGIHTTPRequestHandler)
    h.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass
except RuntimeError, e:
    if e.error[0] == 104:
        pass
    else:
        raise
finally:
    if h is not None:
        h.shutdown()