#Create Layout for GUI

from kivy.uix.gridlayout import GridLayout

from viewer import SignalViewer
       
class StatsLayout(GridLayout):
    def __init__(self,**kwargs):
        super(StatsLayout,self).__init__(**kwargs)

