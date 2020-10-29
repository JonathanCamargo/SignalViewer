#Autoselect functions are created to define hardcoded defaults
#depending on topic name and topic type for convenience.


from customwidgets.text import TextWidget
from customwidgets.plot import PlotWidget

def WidgetSelect(topic_type):
#returns the default plot type for a certain topic type
	selections={
	'custom_msgs/FsmState' : TextWidget
	}
	
	return selections.get(topic_type,PlotWidget)


def AutoSelect(topic_name):
#returns whether or not a topic name should be selected automatically in the
	
	selections={
	'/fsm/State' : False,
	'/ankle/joint_state' : True,
	'/knee/joint_state' : True,
	'/loadcell/wrench' : True
	}

	return selections.get(topic_name,False)

