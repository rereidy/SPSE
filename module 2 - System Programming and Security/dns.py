from __future__ import with_statement, print_function
import sys
import re

if __name__ == "__main__":
    with open("/var/log/syslog", "r") as f:
        for line in f:
            l = line.strip()
            if re.search(r"DNS", l, re.IGNORECASE):
                print("DNS line: {0}".format(l), file=sys.stdout)