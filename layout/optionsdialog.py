#Create Layout for impedance parameters


from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from kivy.clock import Clock


#Convenience editing of dictionaries
from common.dict import getsemileafs_paths, getleaf_value, setleaf_value, isleaf

from kivy.uix.popup import Popup


from kivy.logger import Logger

posible_equations=('constant','scaleOnWeightEqn', 'scaleOnSpeedEqn', 'scaleAnkleStiffnessEqn','dampingEqn', 'scaleOnWeightEqn2Up', 'scaleOnWeightEqn2Down','previousValueEqn');
parameters=dict();

# Dictionary holding the posible equations
# and their parameters, types and default values.
parameters['constant']={};

parameters['scaleOnWeightEqn']={
    'C': {'default':0,'type':'float'},
    'initial_value': {'default':0,'type':'float'},
    'final_value': {'default':0,'type':'float'},
    'value': {'default':0, 'type': 'float'}
    }

parameters['scaleOnWeightEqn2Up']={
    'C': {'default':0,'type':'float'},
    'initial_value': {'default':0,'type':'float'},
    'final_value': {'default':0,'type':'float'},
    'value': {'default':0, 'type': 'float'},
    'initial_w': {'default':0, 'type': 'float'},
    'final_w': {'default':0, 'type': 'float'}
    }

parameters['scaleOnWeightEqn2Down']={
    'C': {'default':0,'type':'float'},
    'initial_value': {'default':0,'type':'float'},
    'final_value': {'default':0,'type':'float'},
    'value': {'default':0, 'type': 'float'},
    'initial_w': {'default':0, 'type': 'float'},
    'final_w': {'default':0, 'type': 'float'}
    }    

parameters['scaleOnSpeedEqn'] = {
    'A': {'default':0.141, 'type':'float'},
    'B': {'default':0.264, 'type':'float'}
    }

parameters['scaleAnkleStiffnessEqn'] = {
}

parameters['dampingEqn'] = {
    'P': {'default': 1, 'type': 'float'}
}

parameters['previousValueEqn'] = {
    'param_name': {'default': '', 'type': 'string'}
}

class OptionsDialog(ModalView):
# A class for creating a modal view with the options for a parameter
# options contain a dictionary with the equation and all its posible parameters
    semileaf_dict=None
    title_lbl=ObjectProperty(Label)
    paramsholder=ObjectProperty(BoxLayout)   
    def __init__(self,semileaf_path=None,semileaf_dict=None,**kwargs):
        super(OptionsDialog,self).__init__(**kwargs)
        self.semileaf_dict=semileaf_dict
        self.semileaf_path=semileaf_path
        Clock.schedule_once(lambda dt: self.build(), 0)
    
        
    def build(self):
        print("Options dialog build")
        self.populate()
    
    def populate(self):
        #Construct the options menu from a ROSParams object 
        self.clear() # Start from fresh
        if self.semileaf_dict is None:
            return
        #Fill the label
        self.title_lbl.text="Options for "+"/".join(self.semileaf_path)
        semileaf=self.semileaf_dict
        #Create labels+textboxes
        options=semileaf['options']
        equation=options['equation']
        boxLayout=BoxLayout(orientation='horizontal')
        boxLayout.add_widget(Label(text='equation:'))          
            
        spinner=Spinner(text=equation,values=posible_equations)
        spinner.bind(text=self.spinner_callback)
        boxLayout.add_widget(spinner)   
        self.paramsholder.add_widget(boxLayout)
    
        #Add parameter 
        for parameter in options.keys():
            if not parameter=='equation':
                boxLayout=BoxLayout(orientation='horizontal')
                boxLayout.add_widget(Label(text=parameter+':'))
                newTextInput=TextInput(text=str(options[parameter]))
                isfloat=False
                if not equation in parameters:
                    #ERROR this equation is not supported default parameters to float
                    Logger.info('Equation not supported')           
                    isfloat=True
                    
                else:
                    if parameters[equation][parameter]['type']=='float':
                        isfloat=True            
                newTextInput.bind(text=self.on_text_callback_generator(parameter,isfloat))
                boxLayout.add_widget(newTextInput)
                self.paramsholder.add_widget(boxLayout)

    def spinner_callback(self,spinner,text):
        print("selected eq:"+text)
        if text in posible_equations:
            # Change dictionary values for the defaults corresponding to
            # this equation's parameters
            new_options=dict()
            new_options['equation']=text
            eq_parameters=parameters[text]
            if type(eq_parameters) is dict:
                for parameter in eq_parameters.keys():
                    param=eq_parameters[parameter]
                    new_options[parameter]=param['default']
            print("\t%s"%new_options)   
            self.semileaf_dict['options']=new_options
        self.populate()
        
        
    def on_text_callback_generator(self,key,isfloat):
    #This function helps to create a callback function for each text input
    # modifying the appropiate key of the dictionary
        return lambda instance,value : self.change_paramvalue(key,value,isfloat)


    def change_paramvalue(self,param_key,value,isfloat=True):
        #Change the value for a key
        param_dict=self.semileaf_dict
        options=param_dict['options']
        #value always comes as a string
    
        if isfloat:
            try:
                value=float(value)
            except:
                    pass
        options[param_key]=value
    
    def clear(self):
        self.paramsholder.clear_widgets()
    
    

    
    
