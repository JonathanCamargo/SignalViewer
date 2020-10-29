#Create Layout for GUI
import sys

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from subprocess import Popen

from kivy.clock import Clock

from kivy.uix.popup import Popup

from layout.filechoosing import LoadDialog,SaveDialog

from roshandlers.rosbag import Rosbag
from roshandlers.recorder import Recorder

from subprocess import Popen

from extensions.arduino import Arduino

import rospy
from custom_msgs.msg import String
from std_msgs.msg import Header

import os

class Toolbar(GridLayout):
    record_btn=ObjectProperty()
    rosbag_input=ObjectProperty()
    duration_input=ObjectProperty()

    rosbag_name="test"        #File name for rosbag file (without extension)
    parameters_name="parameters"  #File name for parameters file (without extension)
    isRecording=False
    path="/home"        #Path for the workspace
    popup=ObjectProperty

    def __init__(self,**kwargs):
        super(Toolbar,self).__init__(**kwargs)
        Clock.schedule_once(lambda dt:self.build(),0)

    def build(self):
        print("Toolbar build")
        thisApp=App.get_running_app()
        self.path=thisApp.config.get('section1','path')
        if self.path[-1]!='/':
            self.path=self.path+'/'

        self.mainLayout_ref=self.parent.parent

        self.rosbag_name=thisApp.config.get('section1','SubjectID')
        self.parameters_name=thisApp.config.get('section1','SubjectID')
        self.rosnamespace=thisApp.config.get('section2','rosNamespace')

        self.rosbag_path=self.path+self.rosbag_name+'.bag'
        self.parameters_path=self.path+self.parameters_name+'.params'
        self.rosbag_input.text=self.rosbag_path
        self.rosbag_input.bind(text=self.textbox_callback)
        self.recorder=Recorder()
        eriscommandstopic=self.rosnamespace+'/eris/command'
        self.eriscommands_pub=rospy.Publisher(eriscommandstopic,String,queue_size=10)

    def open_callback(self):
        print("open dialog")
        content=LoadDialog(path=self.path)
        content.cancel_callback=self.cancel
        content.open_callback=self.open_file
        self.popup=Popup(title="open configuration file",content=content)
        self.popup.open()

    def open_file(self,path):
        self.popup.dismiss()
        print(path)
        try:
            Popen(["rosparam", "load",path])
            msg_str="Parameters loaded"
        except:
            msg_str="Error loading file"
        finally:
            self.popup = Popup(title='Loading',content=Label(text=msg_str),size_hint=(None, None), size=(200, 200))
            self.popup.open()


    def save_callback(self):
        print("save dialog")
        content=SaveDialog(path=self.path)
        content.cancel_callback=self.cancel
        content.save_callback=self.save_file
        content.text_input.text=self.parameters_path
        print(content.text_input)
        self.popup=Popup(title="Save configuration file",content=content)
        self.popup.open()

    def save_file(self,path):
        self.popup.dismiss()
        try:

            Popen(["rosparam", "dump",path])
            msg_str="Parameters saved"
        except:
            msg_str="Error saving file"
        finally:
            self.popup = Popup(title='Saving',content=Label(text=msg_str),size_hint=(None, None), size=(200, 200))
            self.popup.open()

    def cancel(self):
           self.popup.dismiss()


    def signal_viewer_callback(instance):
        dirname=os.path.dirname(__file__) #This directory
        main_signals_script= os.path.join(dirname,'..','main_signals.py')
        Popen(["python", main_signals_script])

    def record_callback(self,instance):
        if self.isRecording is False:
            print("Recoding to rosbag")
            a=self.mainLayout_ref.ros.get_published_topics()
            #Do only topics that are relayed (published under /record namespace)
            topicList=[out[0] for out in a]
            topicList=[topic for topic in topicList if "record" in topic ]
            print(topicList)
            if len(topicList)==0:
                self.popup=Popup(title="ERROR",content=Label(text="No /record/* topics found"),
               size_hint=(None, None), size=(200, 200))
                self.popup.open()
                Clock.schedule_once(lambda dt: self.cancel(), 1)
            else:
                print(topicList)
                self.rosbag=Rosbag(self.rosbag_path,topics=topicList)
                self.rosbag.record(duration=self.duration_input.text)
                print("Recording on remote")
                self.recorder.record(self.rosbag_path)
                self.record_btn.text="stop"
                self.isRecording=True
                self.rosbag_input.disabled=True
                scheduled_time=float(self.duration_input.text)*60.0
                print('Stopping bag in '+str(scheduled_time)+' s')
                self.event_stopRecording=Clock.schedule_once(lambda dt:self.stopRecording(),float(self.duration_input.text)*60.0)


            #Send SD_REC command to activate record in Eris (if available)
            msgs=String()
            header=Header(stamp=rospy.Time.now())
            a=self.rosbag_path.split('/')
            a=a[-1].split('.')
            filename=a[0]
            msgs.data='SD_REC '+filename
            self.eriscommands_pub.publish(msgs)

        else:
            print('asdsd')
            self.stopRecording()

    def stopRecording(self):
        if self.isRecording is True:
            print("Stop recording to rosbag")
            self.event_stopRecording.cancel()
            self.rosbag.stop()
            self.record_btn.text="record"
            self.isRecording=False
            self.rosbag_input.disabled=False
            print("Stop recording on remote")
            self.recorder.stop()
            print("Stop recording on eris")
            msgs=String()
            header=Header(stamp=rospy.Time.now())
            msgs.data='SD_NREC'
            self.eriscommands_pub.publish(msgs)


    def textbox_callback(self, instance, value):
        self.rosbag_path=value

    def settings_callback(self,instance):
        print("Settings")
        App.get_running_app().open_settings()
        self.build()
