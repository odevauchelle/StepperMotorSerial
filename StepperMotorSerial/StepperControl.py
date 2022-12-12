import serial
from pylab import *
import json
from time import sleep


class Stepper :
    
    def __init__( self, port = None, dt = None, board_id = 'Stepper' ) :
 
        if dt is None :
            dt = 20 # milliseconds
        
        self.default_dt = dt
        self.id = board_id
 
        if not port is None :
            self.connect( port = port )
        
        else :
            for port_index in range(10) :
                
                port = '/dev/ttyACM' + str( port_index )
                
                print('Connecting to port ' + port + ' as ' + self.id )
                
                try :
                    self.connect( port = port )
                    break
                
                except Exception as e:
                    print(e)
        

    def write(self, message, serial_port = None ) :
           
        if serial_port is None :
            serial_port = self.serial
        
        return serial_port.write( message.encode() )

    def read( self, serial_port = None ) :
             
        if serial_port is None :
            serial_port = self.serial
        
        return serial_port.readline().decode().strip()


    def communicate( self, message, serial_port = None ) :
        
        self.write( message, serial_port = serial_port )
        
        return self.read( serial_port = serial_port )
    

    def test_connection( self, serial_port = None ):
        
        answer = self.communicate( 'id', serial_port = serial_port )
        
        print(answer)
        
        return self.id in answer


    def connect( self, port, **user_serial_kwargs ) :
        
        serial_kwargs = {}
        serial_kwargs.update( user_serial_kwargs ) 
      
        serial_port = serial.Serial( port = port, **serial_kwargs )
  
        if self.test_connection( serial_port = serial_port ) :
            self.serial = serial_port
            print( 'Connected on Stepper board at' + self.serial.port )
        
        else :
            serial_port.close()
            print( 'Port ' + port + 'closed.' )
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


    def wait_for_move( self, verbous = True ) :
        
        while True:
            if 'Done' in self.read() :
                break
            elif verbous :
                print('Not done yet.')
            
    
    def stop( self ) :
        return self.communicate('s')
    
    def close( self ) :
        print( 'Disconnecting from' + self.serial.port )
        self.serial.close()

def state_string_to_json( state_string ) :
    return  json.loads( '{' + state_string + '}' )
        
if __name__ == '__main__' :
    
    s = Stepper()
    print( s.get_state() )
    # ~ print( s.move( N = 100, direction = -1 ) )
    s.close()

    
