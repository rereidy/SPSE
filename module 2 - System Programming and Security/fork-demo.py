#!/usr/bin/env python

import os

def child_process():
    print "i am the child process and my pid is {0}".format(os.getpid())
    print "the child is exiting"
    
def parent_process():
    print "i am the parent process and my pid is {0}".format(os.getpid())
    
    chpid = os.fork()
    if chpid == 0:
        child_process()
    else:
        print "inside the parent process"
        print "the child pid is {0}".format(chpid)
        
        while True:
            pass
        
parent_process()