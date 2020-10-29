#!python

from kivy.uix.settings import SettingItem

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock

 
from kivy.uix.button import Button

class RecordSelector(BoxLayout):
    topics_dict={} 
    checkboxes=ObjectProperty(None)

    def __init__(self,**kwargs):
          print('asdqwd')

          print(kwargs)
          super(RecordSelector,self).__init__(**kwargs)
          print('asdawd')
          print('algo2')
          
          #Clock.schedule_once(lambda dt:self.build(),0)





class SettingButtons(SettingItem):

    def __init__(self, **kwargs):
        #self.register_event_type('on_release')
        # For Python3 compatibility we need to drop the buttons keyword when calling super.
        kw = kwargs.copy()
        #kw.pop('buttons', None)
        super(SettingButtons, self).__init__(**kw)
        #for aButton in kwargs["buttons"]:
        #    oButton=Button(text=aButton['title'], font_size= '15sp')
        #    oButton.ID=aButton['id']

        # obutton=Button(text='asdqwdqwfe')
        
        self.add_widget(RecordSelector())

    def build(self):
        print('asdqadqdw')
        #self.selector.populate(['a','ddd'])

    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return
    def On_ButtonPressed(self,instance):
        self.panel.settings.dispatch('on_config_change',self.panel.config, self.section, self.key, instance.ID)


'''

class RecordSelector(BoxLayout):
    topics_dict={} 
    checkboxes=ObjectProperty(None)

    def __init__(self,**kwargs):
          print('asdqwd')
          super(RecordSelector,self).__init__(**kwargs)
          print('algo2')
          
          #Clock.schedule_once(lambda dt:self.build(),0)

    def build(self,topics_dict=None):
        #Get its own copy of topics
        self.show=[]
        self.active=[]
        print('build signal selector')
        if topics_dict is not None:
            self.topics_dict=topics_dict
        #else:
        #    self.topics_dict=self.viewer_ref.topics_dict
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
        self.populate(filterout)
'''
