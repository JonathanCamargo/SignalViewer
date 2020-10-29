#TEST HOW LAYOUT WORKS
import sys

sys.path.append('..')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.clock import Clock

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
        

class guiLayout(BoxLayout):
    #Root widget or layout for the GUI
    widget_a=ObjectProperty()
    def __init__(self,**kvargs):
        super(guiLayout,self).__init__(orientation='vertical')
        Clock.schedule_once(lambda dt: self.build(), 0)
        Clock.schedule_once(lambda dt: self.fillWithSomething(), 1)

        
    def build(self):
        print("Building Gui Layout dynamic children")

        print("Setting channels for widget a:")        
        a=["channel1","channel2","channel3"]
        
    def fillWithSomething(self):
	print("asd")
	boxl=BoxLayout(orientation='horizontal')
	lbl=Label(text="hola")
	boxl.add_widget(lbl)
	lbl=Label(text="hossla")
	boxl.add_widget(lbl)
		
	self.add_widget(boxl)
        boxl=BoxLayout(orientation='horizontal')
	lbl=Label(text="hola")
	boxl.add_widget(lbl)
	lbl=Label(text="hossla")
	boxl.add_widget(lbl)
		
	self.add_widget(boxl)
        
        
class test_layoutApp(App):
    gui=ObjectProperty(GridLayout)
    def build(self):
        self.gui = guiLayout()
        return self.gui
    def on_start(self):
        pass
    def on_pause(self):
        #To do: save your work here resume is not guaranteed
        pass
    def on_resume(self):
        #To do: app is back alive
        pass
        
        
if __name__ == '__main__': 
    test_layoutApp().run()
