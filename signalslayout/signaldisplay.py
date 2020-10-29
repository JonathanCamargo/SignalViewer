#Create Layout for GUI

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from threading import Thread

from customwidgets.text import TextWidget

from customwidgets.plot import PlotWidget

from subscribers.subscriber import Subscriber


class SignalDisplay(GridLayout):
    plots_dict={} #Dictionary of current plots in the display
    topics_dict={} #Local access to the dictionary of all available topics

    viewer_ref=ObjectProperty(None)
    display_ref=ObjectProperty(None)

    def __init__(self,**kwargs):
          super(SignalDisplay,self).__init__(**kwargs)

    def setreferences(self,viewer,selector):
        self.viewer_ref=viewer
        self.selector_ref=selector

    def build(self,topics_dict=None):
        if topics_dict is not None:
            self.topics_dict=topics_dict
        else:
            self.topics_dict=self.viewer_ref.topics_dict


    def add(self,topic_name,widget_class=TextWidget):
        #add a widget for the topic
        subs=self.topics_dict[topic_name]['subs']
        #Get subscriber channels:
        channels=subs.getChannels()
        newplot=widget_class(channels=channels,title=topic_name)
        newGridElement=GridLayout(cols=1,rows=1)
        newGridElement.add_widget(newplot)
        self.add_widget(newGridElement)
        self.plots_dict[topic_name]=newplot

    def remove(self,topic_name):
        #remove the plot for the corresponding topic
        plot=self.plots_dict[topic_name]
        parentContainer=plot.parent
        parentContainer.parent.remove_widget(parentContainer)
        self.plots_dict.pop(topic_name)

    def update(self):
        for key in self.plots_dict:
            sub=self.topics_dict[key]['subs']
            plot=self.plots_dict[key]
            try:
                data=sub.getQueue()
            except:
                print('Error')
            #print(data)
            if data is not []:
                plot.update(data)
                pass
