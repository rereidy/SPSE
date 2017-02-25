from __future__ import print_function
import os
import sys

INDENT = 2
    
def traverse(directory, level):
    for i in os.listdir(directory):
        ap = os.path.join(directory, i)
        if os.path.isdir(os.path.join(ap)):
            print("{0}listing of sub-directory: {1}".format(level*'--', ap), file=sys.stdout)
            traverse(ap, level+INDENT)
        else:
            print("{0}{1}".format(level*'-', i), file=sys.stdout)

if __name__ == "__main__":
    starting_dir = "/home/rereidy/workspace/spse/mod04"
    #starting_dir = raw_input("Enter start: ")
    print("listing of directory: {0}".format(starting_dir), file=sys.stdout)
    traverse(starting_dir, INDENT)