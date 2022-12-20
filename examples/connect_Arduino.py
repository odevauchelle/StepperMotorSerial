import serial
from time import sleep

arduino = serial.Serial('/dev/ttyACM0', timeout = 1, baudrate = 9600 )

for _ in range(5) :

    arduino.write('id\n'.encode())
    print( arduino.readline() )

arduino.close()
