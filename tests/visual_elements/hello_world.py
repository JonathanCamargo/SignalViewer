#Basic kivy app running
# Showing the different ways to do warnings, errors and info stream
from kivy.app import App
from kivy.uix.label import Label
from kivy.logger import Logger

import warnings
class TestApp(App):
    def build(self):
	warnings.warn("this is a warning")
	Logger.warning("this is a warning in kivy")
        Logger.info('title: This is a info message.')
        Logger.debug('title: This is a debug message.')
        return Label(text="hi there")
TestApp().run()
