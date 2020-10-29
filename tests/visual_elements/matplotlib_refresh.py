#Basic kivy app running
# Showing the different ways to do warnings, errors and info stream
from kivy.app import App
from kivy.uix.label import Label
from kivy.logger import Logger

import matplotlib

from kivy.uix.widget import Widget

matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas

import matplotlib.pyplot as plt

import numpy as np
from numpy import array,arange, sin

import warnings

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

class guiLayout(GridLayout):
    #Root widget or layout for the GUI
    def __init__(self,**kvargs):
        super(guiLayout,self).__init__(orientation='vertical')
	self.cols=1
	self.rows=1
        Clock.schedule_once(lambda dt: self.build(), 0)
        Clock.schedule_interval(lambda dt: self.fillWithSomething(), 1/60)
	self.phase=0
        
    def build(self):
        print("Building Gui Layout dynamic children")
        t=array([0,1,2,3,4,5,6])
	x=array([1,1,2,2,1,1,2])
	fig,ax=plt.subplots()
	self.ax=ax	
	self.line1,=ax.plot(t,x)
	self.widget_a=FigureCanvas(figure=fig)
	self.add_widget(self.widget_a)      


    def fillWithSomething(self):
	self.phase=self.phase+0.1
	t=arange(0,10,0.01)
	x=np.sin(t*4+self.phase)
	self.ax.set_xlim([min(t),max(t)])
	self.ax.set_ylim([1.1*min(x),1.1*max(x)])
	self.line1.set_xdata(t)
	self.line1.set_ydata(x)
	self.widget_a.draw()

class TestApp(App):
    
    def build(self):
	self.gui = guiLayout()
        return self.gui
	
		
	



if __name__ == '__main__': 
	warnings.warn("this is a warning")
	Logger.warning("this is a warning in kivy")
	Logger.info('title: This is a info message.')
	Logger.debug('title: This is a debug message.')
	TestApp().run()

