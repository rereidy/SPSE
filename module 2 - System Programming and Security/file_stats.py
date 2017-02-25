from __future__ import print_function
import os
import sys
import time
import stat
import getopt
import os.path

from pwd import getpwuid
from grp import getgrgid

def permissions_to_unix_name(st):
    is_dir = 'd' if stat.S_ISDIR(st.st_mode) else '-'
    dic = {'7':'rwx', '6' :'rw-', '5' : 'r-x', '4':'r--', '0': '---'}
    perm = str(oct(st.st_mode)[-3:])
    return is_dir + ''.join(dic.get(x,x) for x in perm)

def usage():
    print("""
{0}: print file stats
usage is: {0} -f file_name [h]
    """.format(sys.argv[0], sys.argv[0]))

def parse_args(args):
    fname = None

    try:
        opts, args = getopt.getopt(args, 'hf:')

        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit(2)
            elif opt == '-f':
                fname = arg
    except TypeError as e:
        print(e, file=sys.stderr)
        usage()
        sys.exit(3)
    except getopt.GetoptError:
        print("invlaid argument", file=sys.stderr)
        usage()
        sys.exit(1)

    return fname

if __name__ == "__main__":
    try:
        fname = parse_args(sys.argv[1:])
        
        if fname is None:
            raise ValueError("no file name given")
        elif not os.path.exists(fname):
            raise ValueError("file {0}: does not exist".format(fname))
        
        st = os.stat(fname)
        
        print("file stats: {0}".format(fname), file=sys.stdout)
        perms = permissions_to_unix_name(st)
        print("""
mode:              {0}
inode:             {1}
device:            {2}
hard links:        {3}
uid:               {4}
gid:               {5}
size (bytes):      {6}
last access time:  {7}
modification time: {8}
change time:       {9}
        """.format(perms, st[1], st[2], st[3], getpwuid(st.st_uid)[0], getgrgid(st.st_gid)[0], st[6], time.ctime(st.st_atime), time.ctime(st.st_mtime), time.ctime(st.st_ctime)), file=sys.stdout)
        
        
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    finally:
        sys.exit(0)