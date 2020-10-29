from kivy.app import App

from kivy.properties import ObjectProperty

from signalslayout.mainsignalslayout import MainSignalsLayout

import os

dirname = os.path.dirname(__file__) #This directory


class main_signalsApp(App):
    gui=ObjectProperty(MainSignalsLayout)
    def build(self):
        self.gui =MainSignalsLayout()
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
        'Key1':'12',
        'key2':'42'
        })

    def build_settings(self,settings):
        settings.add_json_panel('Settings',  self.config,os.path.join(dirname,'settings/signals.json'))

if __name__ == '__main__':
    main_signalsApp().run()
