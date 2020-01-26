import digitalio
import pulseio

from adafruit_motor import servo

def create_pwm(pin):
    return pulseio.PWMOut(pin, duty_cycle=2**15, frequency=50)


def create_output(pin):
    out = digitalio.DigitalInOut(pin)
    out.direction = digitalio.Direction.OUTPUT
    return out
    
    
def clamp(v, vmin, vmax):
    if v < vmin:
        return vmin
    elif v > vmax:
        return vmax
    else:
        return v


class Turret:
    ''' Laser Turret Control '''

    def __init__(self, pan, tilt, laser):
        self._pan_servo = servo.Servo(create_pwm(pan))
        self._tilt_servo = servo.Servo(create_pwm(tilt))

        self._laser = create_output(laser)

        self._pan_target = 90
        self._tilt_target = 90
        
        self._pan_servo.angle = self._pan_target
        self._tilt_servo.angle = self._tilt_target
        
    
    @property
    def pan(self):
        return self._pan_target
        
    
    @pan.setter
    def pan(self, value):
        v = clamp(value, 0, 180)
        self._pan_target = v
        self._pan_servo.angle = v

    
    @property
    def tilt(self):
        return self._tilt_target
        
    
    @tilt.setter
    def tilt(self, value):
        v = clamp(value, 90, 180)
        self._tilt_target = v
        self._tilt_servo.angle = v
        
    
    def toggle_laser(self):
        self._laser.value = not self._laser.value
        
        
    def fire(self):
        self._laser.value = True
        
        
    def stop(self):
        self._laser.value = False
        
