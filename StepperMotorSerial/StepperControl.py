#!/usr/bin/env python
# -*- coding: utf-8 -*-


import serial
from serial.tools import list_ports
from pylab import *
import json
from time import sleep

class Stepper :
    
    def __init__( self, port, dt = 20, board_id = 'Stepper', encoding = 'latin-1' ) :

        self.default_dt = dt
        self.id = board_id
        self.encoding = encoding
        
        self.connect( port = port )

    def write(self, message, serial_port = None ) :
        
        if serial_port is None :
            serial_port = self.serial
            
        message = message.encode( self.encoding )

        serial_port.reset_input_buffer()

        serial_port.write( message )


    def read( self, serial_port = None) :
             
        if serial_port is None :
            serial_port = self.serial
        
        try :
            answer = serial_port.readlines()[-1]
            return answer.strip().decode( self.encoding )
        
        except :
            raise NameError('No answer from stepper Arduino on ' + serial_port.port )


    def communicate( self, message, serial_port = None, waiting_time = 1 ) :
                
        self.write( message, serial_port = serial_port )

        sleep( waiting_time )

        return self.read( serial_port = serial_port )
    

    def test_connection( self, serial_port = None ):
        
        answer = self.communicate( 'id', serial_port = serial_port )

        return self.id in answer


    def connect( self, port, **user_serial_kwargs ) :
        
        serial_kwargs = dict( baudrate = 115200, timeout = 0.1 )
        serial_kwargs.update( user_serial_kwargs ) 
      
        serial_port = serial.Serial( port = port, **serial_kwargs )
                

        if True :# self.test_connection( serial_port = serial_port ) :
            self.serial = serial_port
            print( 'Connected on Stepper board at' + self.serial.port )
        
        else :
            serial_port.close()
            print( 'Port ' + port + ' closed.' )
            raise NameError('Not a Stepper board on ' + port )

    
    def get_state( self ):

        return state_string_to_json( self.communicate('?') )
    
    def move( self, dt = None, N = -1, direction = 1, wait = True ):
        
        if dt is None :
            dt = self.default_dt
    
        state_instruction = '>>' + str(dt) + ',' + str(N) + ',' + str(direction)
    
        initial_state = state_string_to_json( self.communicate( state_instruction ) )
    
        if wait :
            self.wait_for_move()
    
        return initial_state


    def wait_for_move( self, check_time = .1 ) :
        
        while True:
            
            sleep( check_time )
            
            try :
                if 'Done' in self.read() :
                    break
            except :
                pass
    
    def stop( self ) :
        return self.communicate('s')
    
    def close( self ) :
        print( 'Disconnecting from' + self.serial.port )
        self.serial.close()

def state_string_to_json( state_string ) :
    return  json.loads( '{' + state_string + '}' )
        
if __name__ == '__main__' :
    
    s = Stepper( port = '/dev/ttyACM1')
    print( s.get_state() )
    # ~ print( s.move( N = 100, direction = -1 ) )
    s.close()

    
