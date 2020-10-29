# button_update_test.py
# Jared Li 11/8/17

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.factory import Factory

kv = '''
MyWidget:
    box: box
    BoxLayout:
        id: box
'''

## Reads states from file and puts them in a list
with open('states.h', 'r') as f:
	states = []
	isState = False
	for line in f:
		if 'FSM_STATES' in line:	
			isState = True
		elif '}' in line:
			isState = False
		if isState:
			i = line.strip()
			states.append(i)
	states.pop(0)
	states.pop(0)
	print states 

## Creates buttons in a loop
class MyWidget(FloatLayout):
    box = ObjectProperty(None)

    def on_box(self, *args):
        for i in states:
            self.box.add_widget(Button(text=str(i)))
            self.box.add_widget(Button(text='Transition'))
            

Factory.register('MyWidget', cls=MyWidget)


class LoopApp(App):
    def build(self):
        return Builder.load_string(kv)


LoopApp().run()



















