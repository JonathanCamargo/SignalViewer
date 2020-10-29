import sys

sys.path.append('../..')

from extensions.arduino import Arduino

def main(**args):	
    a=Arduino('/dev/ttyACM0')
    a.sendtext('$')

if __name__=="__main__":
    main()
