import sys
sys.path.append('..')
import rospy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from rospy import ROSInitException
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout

from subscribers.std_msgs_sub import Float32Subscriber

import threading

class Xlabel(Widget):
    value=StringProperty("")
    def setText(self,text):
        self.value=text;


 
def ROSConnect():
        ros_ok=False
        try:
            print("Connecting to rosmaster")
            rospy.init_node('listener', anonymous=True)
            ros_ok=True     
        except ROSInitException:
            print("Could not initialize ros node")
            ros_ok=False
        finally:
            pass
        return ros_ok
        
class ROSWidget(Widget):
    #ROS connection
    ros_ok=BooleanProperty(False)
    error_popup = ObjectProperty(Popup)

    def a_task(self):
        for i in range(0,100000):
            print("hola %s" % i)
    def __init__(self,**kvargs):
        super(ROSWidget,self).__init__(**kvargs)
        #Do this in a new thread
        ROSConnect()
        
   
        
        
class FloatWidget(Widget):
    #Widget for showing the value of a float variable
    xlabel = ObjectProperty(None)  
    subs1 = ObjectProperty(None)   
    
    def __init__(self,**kvargs):
        super(FloatWidget,self).__init__(**kvargs)
        self.initialize()
    def initialize(self):
        self.subscribeAll()
        Clock.schedule_interval(self.update, 1.0/60.0)

    def subscribeAll(self):
        self.subs1=Float32Subscriber("/x")
    
    def update(self, dt):
        text=str(self.subs1.data)
        self.xlabel.setText(text)
        
class guiLayout(BoxLayout):
    #Root widget or layout for the GUI
    floatwidget=ObjectProperty(None)    
    def __init__(self,**kvargs):
        super(guiLayout,self).__init__(orientation='vertical')
        
        
    
class guiApp(App):
    gui=ObjectProperty(BoxLayout)
    def build(self):
        self.gui = guiLayout()
        return self.gui
    def on_start(self):
        pass
    def on_pause(self):
        #To do: save your work here resume is not guaranteed
        pass
    def on_resume(self):
        #To do: app is back alive
        pass
        
        
if __name__ == '__main__': 
    guiApp().run()
