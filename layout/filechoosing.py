from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from kivy.clock import Clock


class LoadDialog(FloatLayout):
#Class for generating a generic load dialog
#to use it, create an instance of LoadDialog and override the cancel and open _callback methods
    filechooser=ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = '.'

    def __init__(self,path='.',**kwargs):
    	super(LoadDialog,self).__init__(**kwargs)
    	self.path=path
    	Clock.schedule_once(lambda dt: self.build(),0)

    def build(self):
    	self.filechooser.path=self.path
    	self.filechooser.on_submit=self.on_submit_callback

    def cancel_callback(self):
	       print("cancel")

    def on_submit_callback(self,selection,touch):
    	self.path=selection[0]
    	self.open_callback(self.path)

    def _open_callback(self):
    	if len(self.filechooser.selection) > 0:
    		self.path=self.filechooser.selection[0]
    		self.open_callback(self.path)

    def open_callback(self,path):
	       print(path)



class SaveDialog(FloatLayout):
#Class for generating a generic save dialog
#to use it, create an instance of saveDialog and overide the cancel and open _callback methods
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

    filechooser=ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = '.'

    def __init__(self,path='.',**kwargs):
        super(SaveDialog,self).__init__(**kwargs)
        self.path=path
        Clock.schedule_once(lambda dt: self.build(),0)

    def build(self):
        self.filechooser.path=self.path
        self.filechooser.on_submit=self.on_submit_callback

    def cancel_callback(self):
        print("cancel")

    def on_submit_callback(self,selection,touch):
        self.path=selection[0]
        self.save_callback(self.path)

    def _save_callback(self):
        if len(self.filechooser.selection) > 0:
        	self.path=self.filechooser.selection[0]
        	self.save_callback(self.path)
        else:
        	self.save_callback(self.text_input.text)

    def save_callback(self,path):
        print(path)




class SelectDialog(FloatLayout):
    select = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
