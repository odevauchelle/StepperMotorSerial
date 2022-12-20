
import sys
sys.path.append('/home/olivier/git/StepperMotorSerial/')

import StepperMotorSerial as SMS

stepper = SMS.Stepper('/dev/ttyACM0')

stepper.move( N = 10, direction = -1 )

print(stepper.get_state())

stepper.close()
