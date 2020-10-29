#Create Layout for GUI
import sys

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivy.properties import ObjectProperty
from subprocess import Popen

from kivy.clock import Clock

from kivy.uix.popup import Popup

from subprocess import Popen

from extensions.arduino import Arduino

import glob

from roshandlers.params import ROSParam


from subprocess import Popen,PIPE
import signal
import os

import rospy
from custom_msgs.msg import String
from std_msgs.msg import Header

class ErisBar(GridLayout):
    run_btn=ObjectProperty()
    port_spnr=ObjectProperty()
    eris_text=ObjectProperty()
    pid=None #pid for rosbag proces
    port_name='/dev/ttyACM0'
    isRunning=False
    popup=ObjectProperty


    def textCallback(self, msg):
        print(msg)
        self.eris_text.text = 'Eris says:    ' + msg.data

    def __init__(self,**kwargs):
        super(ErisBar,self).__init__(**kwargs)
        Clock.schedule_once(lambda dt:self.build(),0)

    def build(self):
        print("Toolbar build")
        thisApp=App.get_running_app()

        #self.path=thisApp.config.get('section1','path')
        availablePorts=glob.glob('/dev/ttyA*')
        self.port_spnr.values=availablePorts
        self.port=None
        if len(availablePorts)==0:
            self.port_spnr.text='No ports found'
        else:
            self.port_spnr.text=availablePorts[0]
            self.port=availablePorts[0]

        self.port_spnr.bind(text=lambda instance,sel:self.portselect_callback(instance,sel))
        self.eris_text.bind(text=self.scmd_bindCB)
        # Use a ROSParam object to edit parameters on the fly
        self.rosparams=ROSParam('/') #Use global namespace for now TODO get app namespace
        self.launchcommand=None
        self.text_sub=rospy.Subscriber('eris/text', String, self.textCallback)
        self.eriscommands_pub=rospy.Publisher('eris/command',String,queue_size=10)

    def portselect_callback(self,spinner,selection):
        print(selection)
        print("portselectcallback")
        self.port=selection

    def scmd_callback(self, instance):
        msg=String()
        msg.data=self.eris_text.text
        self.eriscommands_pub.publish(msg)
        print("Sent command: ", self.eris_text.text)

    def scmd_bindCB(self, instance, value):
        self.eris_text.text = value
    #print("User entered the following: %s", value)

    def run_callback(self):
        print("runcallback")
        if (self.isRunning==False):
            launchcommand=self.rosparams.get('/eris/launchcommand')
            print(launchcommand)
            if launchcommand==[]:
                self.popup=Popup(title="ERROR",content=Label(text="Please set the /eris/launchcommand parameter"),
                    size_hint=(None, None), size=(400, 200))
                self.popup.open()
                Clock.schedule_once(lambda dt: self.popup.dismiss(), 2)
            else:
                self.launchcommand=launchcommand

        if (self.isRunning==False) and (self.port is not None) and (self.launchcommand is not None):
            # Sets up the  port in the parameters server
            print('hola')
            port=self.port
            self.rosparams.set('eris/port',port)
            # Run the node defined in the parameters server
            # save the pid to kill it in the future
            self.run_btn.text='Stop'
            self.run_btn.background_color=[0.8,0.3,0.2,0.7]
            self.isRunning=True

            arg=self.launchcommand.split()
            print(arg)
            #Record rosbag in another process
            self.process=Popen(arg)
            self.pid=self.process.pid
            #print("Recording rosbag to %s (pid %s)"%(self.path,self.pid))

        elif self.isRunning==True:
            #Kill the node with pid
            #kill (self.pid)
            self.run_btn.text='Run'
            self.run_btn.background_color=[1,1,1,1]
            self.isRunning=False
            #print("Terminating launchfile with pid %s"%self.pid)
            ps_command = Popen("ps -o pid --ppid %d --noheaders" % self.pid,shell=True, stdout=PIPE)
            ps_output = ps_command.stdout.read()
            retcode = ps_command.wait()
            ps_output=ps_output.decode('utf-8')
            if not(retcode==0):
                print("problem with ps")
            else:
                for pid_str in ps_output.split("\n")[:-1]:
                    os.kill(int(pid_str), signal.SIGINT)
                    self.process.send_signal(signal.SIGINT)
