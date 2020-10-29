# Test rosparams
# With two different ways:
# a: low level subscription
# b: using the function Subscriber() to create a queued subscriber


import sys
sys.path.append('../..')

import rospy
import warnings

import signal, sys, time

from roshandlers.params import ROSParam

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
    
	

def main():
    print "START TEST"
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to end')
    #Launch ros node
    rospy.init_node('listener', anonymous=True)
    param1=ROSParam('/test/param1')

    if param1.value is []:
	print("parameter is not set in server")
    else:
	print("parameter: %s , value: %s"%(param1.name,param1.value))
    
    # Modify the value of the parameter
    param1.value=5;
    param1.upload()
    #At this point you can check with rosparam list / rosparam get in terminal

    


    while True:
	# While this infinite loop is running you can open a terminal and modify 
 	# the value in the param server (e.g. rosparam set /test/param1 10.4)
	# the value should refresh accordingly in the print parameter line
	print("Hi!")
	param1.download()
	if param1.value is []:
		print("parameter is not set in server")
    	else:
		print("parameter: %s , value: %s"%(param1.name,param1.value))
	time.sleep(5)


    
        

if __name__ == "__main__":
    main()
   
