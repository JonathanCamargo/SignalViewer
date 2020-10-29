#Create Layout for GUI

from kivy.uix.gridlayout import GridLayout

from signalslayout.viewer import SignalViewer
       
class MainSignalsLayout(GridLayout):
    def __init__(self,**kwargs):
        super(MainSignalsLayout,self).__init__(**kwargs)

