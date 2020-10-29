import rospy
import threading
import importlib

from collections import deque
from custom_msgs.msg import *

def SubscriberFromPackage(topic_name,type_str):
#creates a subscriber for topic topic_name
#using the class given as a string: type_str
# in the form package_name/message_type
# returns None if fails otherwise returns the subscriber instance
    if topic_name is not "" and type_str is not "":
        #parse package name and message class_str
        split_type=type_str.split('/')
        package_name=split_type[0]
        class_name=split_type[1]+'Subscriber'
        try:
            module_=importlib.import_module('.'+package_name+'_sub',package='subscribers')
        except ImportError as e:
            print('ERROR in '+'.'+package_name+'_sub')
            raise ImportError("package %s not found %s"%(package_name,e))
        else:
            try:
                class_=getattr(module_,class_name)
                subscriber=class_(topic_name)
            except:

                raise ImportError("class %s not found"%class_name)
            else:
                return subscriber

def Subscriber(topic_name,type_str):
#creates a subscriber for topic topic_name
#using the class given as a string: type_str
# in the form package_name/message_type
# returns the subscriber instance
    try:
        subscriber=SubscriberFromPackage(topic_name,type_str)
    except ImportError as e:
        print('Attempting to create a GenericSubscriber -This is EXPERIMENTAL-')
        try:
            split_type=type_str.split('/')
            package_name=split_type[0]
            class_name=split_type[1]
            module_=importlib.import_module(package_name+'.msg')
            data_class=getattr(module_,class_name)
            subscriber=GenericSubscriber(topic_name,data_class)
        except ImportError as e:
            print('ERROR in '+package_name+'.msg')
            raise ImportError("package %s not found %s"%(package_name,e))
    return subscriber


# A generic subscriber class for interfacing any type of message in to the GUI
class GenericSubscriber(object):
    def __init__(self,topic,data_class,QUEUE_SIZE=1000):
        #Properties
        self.topic="" # topic name (e.g. /myrobot/someNamespace/somemessage)
        self.data_class="" # type of message in the form 'package_name/message_type' e.g. 'custom_msgs/JointState
        self.registered = True #indicates if subscriber is registered (i.e. listening to data)
        self.paused = False #indicates if subscriber pauses appending data to the queue
        self.channels = None
        self.queue = deque(maxlen=QUEUE_SIZE) #Queue for saving data
        self.subs = None # subscriber object

        if topic!="":
            self.topic=topic
            print("subscribing to "+topic)
        if data_class!="":
            self.topic=topic
            self.data_class=data_class
            print("using data class:"+str(data_class))
            self.channels=self.data_class.__slots__
            self.channel_types=self.data_class._slot_types
            print("with channels:"+str(self.channels))
        self.t=threading.Thread(target=self.listener())
        self.t.start()

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



    def listener(self):
        try:
            self.subs=rospy.Subscriber(self.topic, self.data_class, self.callback)
        except:
            print("Could not subscribe")
        else:
            self.registered=True

    def append(self, newElement):
        if self.paused == False:
            self.queue.append(newElement)

    def getQueue(self):
        return list(self.queue)

    def getChannels(self):
        return self.channels

    def unsubscribe(self):
        print("unsubscribing to "+self.topic)
        if self.subs is not None:
            self.subs.unregister()
            self.registered=False

    def subscribe(self):
        print("unsubscribing to "+self.topic)
        if self.subs is not None:
            self.subs.register()
            self.registered=True
