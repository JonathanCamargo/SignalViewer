# TOOLS for manipulation of dictionaries


# This was made for getting the leafs' paths for all the leafs in a nested dictionary
# this is important for grabing parameters from the parameters server when they are grouped
# for example: /fsm/EarlyStance/knee/k /fsm/EarlyStance/ankle/k
# if we want to get all the parameters from EarlyStance we do
# params('/fsm/EarlyStance') this will give parameters as a dictionary:
# {'knee':{'k': somevalue,'b':somevalue},'ankle':{'k': somevalue,'b':somevalue}}

# We then can take the keys in a more convenient structure:
# [['knee','k'],['knee','b'],['ankle','k'],['ankle','b']]

def isleaf(dict_elem):
	if type(dict_elem) is dict:
		return False
	else:
		return True

def issemileaf(dict_elem):
	if type(dict_elem) is dict:
		if 'value' in dict_elem:
			return True
		else:
			return False
	else:
		return True

def getleafs_paths(dictionary,path=None):
	if path is None:
		path=[];
	leafs_paths=[];
	for key in dictionary.keys():
		child=dictionary[key]
		if isleaf(child) is True:
			tmp=path[:]
			tmp.append(key)
			child_name=tmp
			leafs_paths.append(child_name[:])
			#print("child")
			#print(child_name)	
			#print(leafs_paths)
		else:
			tmp=path[:]
			tmp.append(key)
			children_paths=getleafs_paths(dictionary[key],tmp)
			#print("im not leaf")
			leafs_paths.extend(children_paths)
			#print(leafs_paths)
		
	return leafs_paths

def getsemileafs_paths(dictionary,path=None):
	#Same as getleafs_paths but consider entries with 'value' key as a leaf
	if path is None:
		path=[];
	leafs_paths=[];
	for key in dictionary.keys():
		child=dictionary[key]
		if issemileaf(child) is True:
			tmp=path[:]
			tmp.append(key)
			child_name=tmp
			leafs_paths.append(child_name[:])
			#print("child")
			#print(child_name)	
			#print(leafs_paths)
		else:
			tmp=path[:]
			tmp.append(key)
			children_paths=getsemileafs_paths(dictionary[key],tmp)
			#print("im not leaf")
			leafs_paths.extend(children_paths)
			#print(leafs_paths)
		
	return leafs_paths

def getleaf_value(dictionary,keys_list):
#Gets the value of a leaf element
	tmp=dictionary
	for key in keys_list:
		tmp=tmp[key]
	return tmp

def setleaf_value(dictionary,keys_list,value):
#Gets the value of a leaf element
	tmp=dictionary
	for i,key in enumerate(keys_list):
	
		if i<len(keys_list)-1:
			tmp=tmp[key]
		else:
			tmp[key]=value
		
	


