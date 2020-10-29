import sys

sys.path.append('../..')

from common.dict import getleafs_paths , getleaf_value, setleaf_value

def main(**args):	
    dictionary={'ankle': {'k': 200, 'b': 15, 'theta_eq': 0}, 'knee': {'k': 172, 'b': 0, 'theta_eq': 0}}
    print("Dictionary: %s"%dictionary)
    a=getleafs_paths(dictionary)   
    print("Leafs:%s"%a)
    leaf_i=1
    print("Value for leaf %s : %s"%(a[leaf_i],getleaf_value(dictionary,a[leaf_i])))
    setleaf_value(dictionary,a[leaf_i],18.5)
    print("New Dictionary: %s"%dictionary)


if __name__=="__main__":
    main()
