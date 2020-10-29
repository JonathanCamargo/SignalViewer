#  python filter_bar.py
# A test to implement functionality to filter content
# The task is to have a list of names (that in the end will create labels in the display)
# place a textInput bar
# use the text input bar to enter a text
# e.g. name/
# e.g. name/oth
# e.g. aname
# the filter is a function that reads a list of strings and compares each string to see if it contains the filter_text value. it should return a list of indexes where a match exists.

import sys
sys.path.append('..')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput



class InputLayout(BoxLayout):
    #Widget for showing the value of a float variable
    input = ObjectProperty(TextInput)

    def __init__(self, **kvargs):
        super(InputLayout, self).__init__(**kvargs)
        Clock.schedule_once(lambda dt: self.build(), 0)

    def build(self):
        print("build")
        self.input.bind(text=self.parent.on_input_callback)

    def update(self, dt):
        text = str(self.subs1.data)
        self.xlabel.setText(text)


class guiLayout(BoxLayout):
    #Root widget or layout for the GUI
    floatwidget = ObjectProperty(None)

    def __init__(self, **kvargs):
        super(guiLayout, self).__init__(orientation='vertical')
        self.all_names = [
            'name/othername/aname', 'name/othername/aname',
            'name/othername/bname', 'name/othername/cname',
            'name/thisothername/aname', 'nameZ/othername/aname',
            'nameZ/othername/aname'
        ]
        Clock.schedule_once(lambda dt: self.build(self.all_names), 0)

    def build(self, names_list):
        self.clear_labels()
        for i, name in enumerate(names_list):
            #create labels
            print(name)
            self.grid.add_widget(Label(text=name))

    def clear_labels(self):
        #Delete all labels in the widget
        self.grid.clear_widgets()

    def on_input_callback(self, instance, value):
        print(value)
        # TO DO #
        # This is where the filter does the work#
        new_names = filter(lambda x: value in x, self.all_names)
        self.build(new_names)


# TO DO #
# use the filter output to generate a new (filtered) names_list
# -> name_list=something
# Draw the gui again
# self.build(names_list)


class filter_barApp(App):
    gui = ObjectProperty(BoxLayout)

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
    filter_barApp().run()
