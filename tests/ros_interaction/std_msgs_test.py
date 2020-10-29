# Test ros subscription to std_msgs 
# With two different ways:
# a: low level subscription
# b: using the function Subscriber() to create a queued subscriber


import sys
sys.path.append('../..')

from subscribers.subscriber import Subscriber
from subscribers.std_msgs_sub import Float32Subscriber

import rospy
import warnings

import signal, sys, time

from std_msgs.msg import Float32

from StringIO import StringIO

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def callback(data):
    print(Float32._full_text)    
    print("callback from c data=%s"%data)
    
	

def main():
    print "START TEST"
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to end')
    #Launch ros node
    rospy.init_node('listener', anonymous=True)
    #Create subscribers in three different ways:
    
    #1. Use general subscriber passing topic name and type of message
    a=Subscriber("/x","std_msgs/String")
    #2. Use the specific subscriber for the message
    b=Float32Subscriber("/x")
    print(a)
	
    #3. Use rospy.subscriber function directly
    c=rospy.Subscriber("/x", Float32, callback)
    
    print(a.channels)
    if a.registered is False :
            warnings.warn("Something wrong with a subscriber")     
    if b.registered is False:
            warnings.warn("Something wrong with b subscriber")
           
    asize=0
    bsize=0
    while True:
        aqueue=a.getQueue()
        bqueue=b.getQueue()
        if len(aqueue)>asize:
	    asize=len(aqueue)
            print("a=%s"%aqueue)
        if len(bqueue)>bsize: 
 	    print("b=%s"%bqueue)	
	    bsize=len(bqueue)
	time.sleep(0.1)
        

if __name__ == "__main__":
    main()
   
