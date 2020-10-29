from kivy.app import App
from kivy.properties import ObjectProperty

from layout.mainlayout import MainLayout

from kivy.config import ConfigParser,Config
from kivy.uix.settings import Settings
from kivy.core.window import Window

from layout.toolbar import Toolbar

from kivy.factory import Factory
from kivy.clock import Clock

from custom_msgs.msg import *

from settings.recordsettingspanel import SettingButtons

import subprocess
import rospy
import os

dirname = os.path.dirname(__file__) #This directory

class mainApp(App):
    gui=ObjectProperty(MainLayout)
    toolbar=ObjectProperty
    rosNamespace=''
    Window.size=(700,350)
    def build(self):
        config=self.config
        self.rosNamespace=config.get('section2','rosNamespace')
        self.gui =MainLayout()
        return self.gui

    def on_start(self):
        pass
    def on_pause(self):
        #To do: save your work here resume is not guaranteed
        pass
    def on_resume(self):
        #To do: app is back alive
        pass

    def build_config(self,config):
        config.setdefaults('section1',{
        'SubjectID':'AB',
        'path':'/home/ossip/AB'
        })
        config.setdefaults('section2',{
        'rosNamespace':''
        })

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('section1', 'SubjectID'):
                self.gui.toolbar.build()
            elif token == ('section1', 'path'):
                self.gui.toolbar.build()
            elif token == ('section2', 'rosNamespace'):
                self.rosNamespace=value;
                print("New ROS namespace: %s"%value)

    def build_settings(self,settings):
        settings.add_json_panel('Experiment', self.config,os.path.join(dirname,'settings/experiment_settings.json'))
        #settings.register_type('recordselector', SettingButtons)
        #settings.add_json_panel('Record', self.config,os.path.join(dirname,'settings/record_settings.json'))


if __name__ == '__main__':
    mainApp().run()
