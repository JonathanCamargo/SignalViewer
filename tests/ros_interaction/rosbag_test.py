# Test rosparams
# With two different ways:
# a: low level subscription
# b: using the function Subscriber() to create a queued subscriber


import sys
sys.path.append('../..')

import rospy
import warnings

import signal, sys, time

from roshandlers.rosbag import Rosbag


bag=Rosbag()

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
    
	

def main():
    print "START TEST"
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to end')
   
    print("bag file:%s"%bag.path)
    print("start recording")
    bag.record()


    for i in range(5):
	# While this infinite loop is running you can open a terminal and modify 
 	# the value in the param server (e.g. rosparam set /test/param1 10.4)
	# the value should refresh accordingly in the print parameter line
	print("Hi!")
	time.sleep(1)

    bag.stop()


    
        

if __name__ == "__main__":
    main()
   
