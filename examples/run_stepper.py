
from pylab import *

import sys
sys.path.append('/home/olivier/git/StepperMotorSerial/')

import StepperMotorSerial as SMS

stepper = SMS.Stepper()

stepper.move( N = 500, direction = -1 )


stepper.close()
