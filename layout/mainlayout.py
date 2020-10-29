#Create Layout for GUI


from roshandlers.rosconnector import ROSConnector

from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.gridlayout import GridLayout

from layout.toolbar import Toolbar
from layout.erisbar import ErisBar

from kivy.uix.popup import Popup
from kivy.clock import Clock


from threading import Thread

class MainLayout(GridLayout):

    #fsm=ObjectProperty(FSM) #reference to fsm object inside the main layout
    toolbar=ObjectProperty(Toolbar) #reference to toolbar object inside the main layout
    ros=ROSConnector()
    counter=0
    popup=ObjectProperty(None)
    event=None

    def __init__(self,**kvargs):
        super(MainLayout,self).__init__(**kvargs)
        Clock.schedule_once(lambda dt: self.initROS(), 2)
        self.popup=None
        self.counter=0

    def build(self):
        print("MainLayout build")

    def initROS(self):
        t = Thread(target=self.ros.connect)
        t.start()
        self.event=Clock.schedule_interval(lambda dt: self.checkROS(), 1/10)

    def checkROS(self):
        if self.popup==None:
            self.popup = Popup(title='Connecting to ROS',
                  content=Label(text='Attempting connection'),
                 size_hint=(None, None), size=(200, 200))
            self.popup.open()
        if not self.ros.isOK():
            self.counter=self.counter+1;
            if self.counter>5:
                self.popup.content=Label(text='ERROR: verify ROS')
        else:
            if self.popup is not None:
                self.popup.dismiss()
            self.event.cancel()
