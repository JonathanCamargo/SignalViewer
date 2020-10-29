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

from subscribers.subscriber import Subscriber


class SignalSelector(BoxLayout):
    topics_dict={}
    viewer_ref=ObjectProperty(None)
    display_ref=ObjectProperty(None)

    checkboxes=ObjectProperty(None)

    def __init__(self,**kwargs):
          super(SignalSelector,self).__init__(**kwargs)

    def setreferences(self,viewer,display):
        self.viewer_ref=viewer
        self.display_ref=display

    def build(self,topics_dict=None):
        #Get its own copy of topics
        self.show=[]
        self.active=[]
        if topics_dict is not None:
            self.topics_dict=topics_dict
        else:
            self.topics_dict=self.viewer_ref.topics_dict
        self.filter_input.bind(text=self.on_filter)

    def populate(self,topics_list=None):
        MAXDISPLAY=20
        self.checkboxes.clear_widgets()
        if topics_list is not None:
            if len(topics_list)>MAXDISPLAY:
                topics_list=topics_list[0:MAXDISPLAY]
            #populate with topics from the list
            for topic in topics_list:
                if self.topics_dict[topic] is not None:
                    self.addcheckbox(topic)
        else:
            # populate with all
            n=0
            for key in self.topics_dict:
                n=n+1
                if n>MAXDISPLAY:
                    break
                self.addcheckbox(key)



    def addcheckbox(self,topic):
        topic_name=topic
        topic_type=self.topics_dict[topic]['type']
        print("add %s, %s"% (topic_name,topic_type))
        checkbox=CheckBox()
        if self.topics_dict[topic]['active'] is True:
            checkbox.active=True
        callback= self.create_checkbox_callback(topic_name)
        checkbox.bind(active=callback)
        label=Label(text=topic_name)
        self.checkboxes.add_widget(checkbox)
        self.checkboxes.add_widget(label)

    def create_checkbox_callback(self,topic_name):
        return lambda checkbox,value : self.on_checkbox(checkbox,value,topic_name)

    def on_checkbox(self,checkbox,value,topic_name):
        if value:
            self.viewer_ref.activateTopic(topic_name)
        else:
            self.viewer_ref.deactivateTopic(topic_name)

    def on_filter(self,instance,value):
        filterout=filter(lambda x: value in x,self.topics_dict.keys())
        self.populate([a for a in filterout])
