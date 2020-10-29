#Create Layout for GUI
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

from kivy.clock import Clock

#from kivy.factory import Factory

#Class for a widget that displays data from a queue
# as TEXT

#Two ways of operation:
# (full=True) displays all the queue as text
# (full=False) displays the last value in the queue *DEFAULT

#Each widget should include the following methods:

# def build(self,channels):
#     Creates the visual elements corresponding to the channels in the queue
# def update(self,queue):
#     updates the contents of the elements with the new data in the queue

class CustomLabel(Label):
	def __init__(self,full=False,channels=["channel"],**kwargs):
		super(CustomLabel,self).__init__(**kwargs)


class TextWidget(Widget):
	full=False
	channels=None
	channel_box=ObjectProperty()
	data_box=ObjectProperty()
	def __init__(self,full=False,channels=["channel"],**kwargs):
		super(TextWidget,self).__init__(**kwargs)
		self.full=full
		Clock.schedule_once(lambda dt: self.build(channels), 0)

	def build(self,channels):
		self.channel_box.clear_widgets()
		self.data_box.clear_widgets()
		self.channels=channels
		for index,channel in enumerate(self.channels):
			self.channel_box.add_widget(CustomLabel(text=channel))	
			self.data_box.add_widget(CustomLabel(text=channel+" value"))
		
					
	def update(self,data):
		if data==[]:
			return
		if self.full is False:
			data=data[-1]
		if len(data)==len(self.channels):
			for index,channel in enumerate(self.channels):
				box_index=len(self.channels)-index-1
				self.data_box.children[box_index].text=str(data[index])
				
