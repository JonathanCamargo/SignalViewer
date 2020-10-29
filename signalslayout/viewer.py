#Create Layout for GUI
from roshandlers.rosconnector import ROSConnector
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from threading import Thread
from customwidgets.text import TextWidget
from customwidgets.plot import PlotWidget
from subscribers.subscriber import Subscriber

from signalslayout.signaldisplay import SignalDisplay
from signalslayout.signalselector import SignalSelector
from signalslayout.autoselector import WidgetSelect
from signalslayout.autoselector import AutoSelect


class SignalViewer(GridLayout):
    signalselector=ObjectProperty(SignalSelector)
    signaldisplay=ObjectProperty(SignalDisplay)

    ros=ROSConnector()
    counter=0
    popup=ObjectProperty(None)
    event=None

    #Dictionary of all topics:
    # {topic_name: {'active': True/False,'sub':subscriber}
    # List of all subscribers
    topics_dict={}

    # Matching List with True for active subscriber

    def __init__(self,**kwargs):
        super(SignalViewer,self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.initROS(), 2)


    def initROS(self):
        #Connect to ROS? try to do it in parallel
        t = Thread(target=self.ros.connect)
        t.start()
        self.event=Clock.schedule_interval(lambda dt: self.checkROS(), 1/10)

    def checkROS(self):
        if not self.ros.isOK():
            self.counter=self.counter+1;
            if self.counter==1:
                self.popup = Popup(title='Connecting to ROS',
                          content=Label(text='Attempting connection'),
                         size_hint=(None, None), size=(200, 200))
                self.popup.open()
            elif self.counter>50:
                self.popup.content=Label(text='ERROR: verify ROS')
        else:
            if self.popup is not None: self.popup.dismiss()
            self.event.cancel()
            self.build()

    def build(self):
        #Fill the list of topics
        self.signalselector.setreferences(self,self.signaldisplay)
        self.signaldisplay.setreferences(self,self.signalselector)
        topics_list=self.ros.get_published_topics()
        self.generateTopicsDict(topics_list)
        self.signalselector.build()
        self.signaldisplay.build()

    	#Try to do a hardcoded selection from a friend function#
    	#Experimental#
        for topic_name in self.topics_dict:
        	if AutoSelect(topic_name):
        		print("AutoSelect: %s"%topic_name)
        		self.activateTopic(topic_name)
    	#####################################################
        self.signalselector.populate()
        self.enableUpdates()


    def generateTopicsDict(self,topics_list):
    	#Take a list of topics and create the topics dictionary
    	for topic_entry in topics_list:
    		topic=topic_entry[0]
    		topic_type=topic_entry[1]
    		self.topics_dict[topic]={'type':topic_type,'active':False,'subs':None}



    def enableUpdates(self):
        self.event=Clock.schedule_interval(lambda dt: self.updateDisplay(), 1/10.0)

    def disableUpdates(self):
        self.event.cancel()

    def updateDisplay(self):
        self.signaldisplay.update()

    def activateTopic(self,topic_name):
        self.disableUpdates()
        topic_type=self.topics_dict[topic_name]['type']
        print("activate %s of type %s"%(topic_name,topic_type))
        failed=True
        try:
            sub=Subscriber(topic_name,topic_type)
            self.topics_dict[topic_name]['active']=True
            self.topics_dict[topic_name]['subs']=sub
            failed=False
        except Exception as e:
            print(e)
            error_str="%s: \n\rType not supported"%topic_type
            self.popup = Popup(title='Error',content=Label(text=error_str),size_hint=(None, None), size=(200, 200))
            self.popup.open()
            self.signalselector.populate()
        if failed is not True:
            #Try to do a hardcoded selection from a friend function#
            #Experimental#
            WidgetClass=WidgetSelect(topic_type)
            print("Using widget:"+str(WidgetClass))
            self.signaldisplay.add(topic_name,WidgetClass)
            self.enableUpdates()


    def deactivateTopic(self,topic_name):
    	self.disableUpdates()
    	topic_type=self.topics_dict[topic_name]['type']
    	print("deactivate %s of type %s"%(topic_name,topic_type))
    	self.topics_dict[topic_name]['active']=False
    	sub=self.topics_dict[topic_name]['subs']
    	sub.unsubscribe()
    	self.signaldisplay.remove(topic_name)
    	self.enableUpdates()
