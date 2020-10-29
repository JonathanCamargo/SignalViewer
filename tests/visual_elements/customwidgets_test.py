#TEST CUSTOM WIDGETS (without ROS)
#This app creates a 4x4 grid and adds a TextWidget in one
#of the slots.
import sys
sys.path.append('../..')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivy.uix.gridlayout import GridLayout

from customwidgets.text import TextWidget
from customwidgets.plot import PlotWidget        
import random

from kivy.logger import Logger


class guiLayout(GridLayout):
    #Root widget or layout for the GUI
    widget_a=ObjectProperty()
    widget_b=ObjectProperty()
    def __init__(self,**kvargs):
        super(guiLayout,self).__init__(orientation='vertical')
        Clock.schedule_once(lambda dt: self.build(), 0)
        
    def build(self):
	ch_names=["channel 1","channel 2","channel 3"]	
        Logger.info("Building Gui Layout dynamic children")
	Logger.info("Setting channels for widgets: %s"%ch_names)        
        self.widget_a.build(ch_names)
    	self.widget_b.build(ch_names)
        Clock.schedule_interval(lambda dt: self.fillWithSomething(), 1/3.0)
        
    def fillWithSomething(self):
	sample_data=[[random.random(),random.random(),random.random()],[random.random(),random.random(),random.random()],[random.random(),random.random(),random.random()],[random.random(),random.random(),random.random()]]
        self.widget_a.update(sample_data)
	self.widget_b.update(sample_data)
        
class customwidgets_testApp(App):
    gui=ObjectProperty(GridLayout)
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
   customwidgets_testApp().run()
