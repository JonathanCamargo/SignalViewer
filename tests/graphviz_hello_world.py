from graphviz import Digraph

import pydot
from dot_parser import *

color_transparent='#00000000'
color_focus='#4BFA94F0'
color_normal='#FFFFFFFF'

graphs=pydot.graph_from_dot_file('example.dot')
print(graphs)

#for graph in graphs:
#	for i in graph.get_subgraph_list():
#		pass	
		#for name in i.get_attributes().iterkeys():
			#cluster=Cluster(
		#	print(i.obj_dict['name'])


#Remove background

#graph.set_bgcolor(color_normal)
#graph.write('somefile.png',format='png')

'''
dot = Digraph(comment='The Round Table',format='png')
dot.node('A', 'King Arthur')
dot.source(data)
dot.attr('graph',bgcolor='#ff00005f')
print(dot.source)
dot.render('output/round-table.gv',view=True)
'''
'''
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text="hi there")

TestApp().run()
'''
