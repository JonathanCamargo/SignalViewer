import rospy
from subscriber import GenericSubscriber
from collections import deque

from custom_msgs.msg import *


class Float32Subscriber(GenericSubscriber):
    def __init__(self,topic):
        self.data_class=Float32
        super(Float32Subscriber,self).__init__(topic,self.data_class)
        self.channels=self.data_class.__slots__
        self.channel_types=self.data_class._slot_types

    def callback(self,msg):
        if __debug__:
            pass
        #rospy.loginfo(rospy.get_caller_id()+" %s",msg)
        if self.paused is False:
            #Get each field in the message
            data=[]
            for channel in self.channels:
                if channel is 'header':
                    #If header just take the timestamp
                    time=msg.header.stamp.secs+msg.header.stamp.nsecs/1.0E9
                    data.append(time)
                else:
                    data.append(getattr(msg,channel))
            self.append(data)
