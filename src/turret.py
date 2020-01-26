import digitalio
import pulseio

from adafruit_motor import servo

def create_pwm(pin):
    return pulseio.PWMOut(pin, duty_cycle=2**15, frequency=50)
    

def create_output(pin):
    out = digitalio.DigitalInOut(pin)
    out.direction = digitalio.Direction.OUTPUT
    return out

class Turret:
    ''' Laser Turret Control '''
    
    def __init__(self, pan, tilt, laser):
        self.pan = servo.Servo(create_pwm(pan))
        self.tilt = servo.Servo(create_pwm(tilt))
        
        self.laser = create_output(laser)
        
        self.pan.angle = 90
        self.tilt.angle = 90
        