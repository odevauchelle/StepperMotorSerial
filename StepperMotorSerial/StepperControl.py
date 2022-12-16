#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import json
from time import sleep

class Stepper :

    def __init__( self, port, dt = 20, board_id = 'Stepper' ) :

        self.dt = dt # ms
        self.id = board_id
        self.stepper_revolution_time = 4*self.dt/1000 # s
        self.timeout = 0.1 + 2*self.stepper_revolution_time

        self.connect( port = port )

    def write(self, message, serial_port = None ) :

        if serial_port is None :
            serial_port = self.serial

        message = ( message + '\n' ).encode( )

        serial_port.write( message )


    def read( self, serial_port = None) :

        if serial_port is None :
            serial_port = self.serial

        try :
            answer = serial_port.readline()
            return answer.strip().decode( )

        except :
            raise NameError('No answer from stepper Arduino on ' + serial_port.port )


    def communicate( self, message, serial_port = None ) :

        self.write( message, serial_port = serial_port )

        return self.read( serial_port = serial_port )


    def test_connection( self, serial_port = None ):

        answer = self.communicate( 'id', serial_port = serial_port )

        return self.id in answer


    def connect( self, port, **user_serial_kwargs ) :

        serial_kwargs = dict( baudrate = 9600, timeout = self.timeout )
        serial_kwargs.update( user_serial_kwargs )

        serial_port = serial.Serial( port = port, **serial_kwargs )

        serial_port.reset_input_buffer()
        serial_port.reset_output_buffer()

        if self.test_connection( serial_port = serial_port ) :
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
            dt = self.dt

        state_instruction = '>>' + str(dt) + ',' + str(N) + ',' + str(direction)

        initial_state = state_string_to_json( self.communicate( state_instruction ) )

        if wait :
            self.wait_for_move()

        return initial_state


    def wait_for_move( self ) :

        while True:

            sleep( 5*self.stepper_revolution_time )

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
    s.move( N = 10, direction = -1 )
    print( s.get_state() )
    s.close()
