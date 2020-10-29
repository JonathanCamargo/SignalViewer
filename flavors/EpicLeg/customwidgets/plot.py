#Create Layout for GUI
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
import matplotlib

matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from numpy import array

from kivy.factory import Factory
from copy import deepcopy

#Classes for widgets that displays data from a queue
# as matplotlib plots

# Use the N parameter in the constructor to plot the desired ammount of data


#Each widget should include the following methods:
# def build(self,channels):
#     Creates the visual elements corresponding to the channels in the queue
# def update(self,queue):
#     updates the contents of the elements with the new data in the queue



class PlotWidget(Widget):
	channels=None
	widget_a=ObjectProperty(FigureCanvas)
	def __init__(self,full=False,channels=["channel"],title=None,**kwargs):
		super(PlotWidget,self).__init__(**kwargs)
		self.full=full
		self.channels=channels
		self.lines=[];
		self.has_time=True
		self.title=title
		Clock.schedule_once(lambda dt: self.build(channels), 0)


	def build(self,channels):
		self.lines=[]
		self.channels=channels[:]
		#ignore header
		if 'header' in self.channels:
			self.channels.remove('header')
		else:
			self.has_time=False
		self.figure,self.axis=plt.subplots()
		t=array([0,1,2,3,4,5,6])
		x=array([1,1,2,2,1,1,2])
		fig,ax=plt.subplots()
		self.ax=ax
		for channel in self.channels:
			print(channel)
			line,=ax.plot(t,x)
			self.lines.append(line)
		#self.ax.legend(self.lines,self.channels,loc=4)
		if self.title is not None:
			fig.suptitle(self.title)
		self.widget_a=FigureCanvas(figure=fig)
		self.add_widget(self.widget_a)
		self.bind(pos=self.pos_callback)
		self.bind(size=self.size_callback)
		self.size_callback()
		self.pos_callback()
		#self.lines[1]=None

	def pos_callback(self,*args):
		self.widget_a.pos=self.pos

	def size_callback(self,*args):
		self.widget_a.size=self.size


	def update_data(self,time,data):
		#This takes a time np array and a data list of np vectors
		#data is each channel
		t=time
		min_data=0
		max_data=0
		for i,x in enumerate(data):
			if self.lines[i] is not None:
				#Sort? TODO
				self.lines[i].set_xdata(t)
				self.lines[i].set_ydata(x)
				if min(x)<min_data:
					min_data=min(x)
				if max(x)>max_data:
					max_data=max(x)

		self.ax.set_xlim([min(t),max(t)])
		self.ax.set_ylim([1.1*min_data,1.1*max_data])
		#print(self.lines)
		self.widget_a.draw()


	def update(self,queue):
		#This takes a queue with data in the form:
		#([time ch1 ch2 ... chi ...] [time ch1 ch2 ... chi ...])

                #transform from [time channels][time channels]...
		# to time=[time1 time2 time3 ...]
		# channels=([ch1_1 ch1_2 ch1_3 ...],[ch2_1 ch2_2 ch2_3],[chi_1 chi_2 chi_3...], ...)
		data=np.array(queue)
		if data.size<3:
			return
		if self.has_time is False:
			#create time index 0,1,2...
			time = np.expand_dims(np.arange(data.shape[0]),1)
			data= np.concatenate((time,data),axis=1)
		else:
			time=data[:,0] #if time exists it must be on col0
		vectors=[]
		if(time.size<3):
			return
		for i,channel in enumerate(self.channels):
			vectors.append(data[:,i+1]) #not safe please improve

		self.update_data(time,vectors)
