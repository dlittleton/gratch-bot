''' Receive and print IR codes.

Useful for determining which codes map to buttons on a remote.
'''

import board
import pulseio
import random
import time

from adafruit_circuitplayground import cp

from remote import NecRemote
from settings import Button, Pin
from turret import Turret

LED_GREEN = (0, 200, 0)
LED_OFF = (0, 0, 0)
cp.pixels.brightness = 0.01

ir_pulses = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
remote = NecRemote(ir_pulses)

laser_turret = Turret(Pin.PAN, Pin.TILT, Pin.LASER)

positions = []

def save_position():
    if len(positions) < 10:
        cp.play_tone(500, 0.25)
        cp.play_tone(600, 0.25)
        positions.append((laser_turret.pan, laser_turret.tilt))
        
    for i in range(len(positions)):
        cp.pixels[i] = LED_GREEN
        

def clear_positions():
    positions.clear()
    cp.play_tone(500, 0.25)
    cp.play_tone(400, 0.25)
    cp.pixels.fill(LED_OFF)
    
    
class Controls:
    
    def __init__(self):
        self._toggle = False
        self._add = False
        self._mode = False
        self._mode_last = 0

    @property
    def up(self):
        return cp.touch_A5
        
    @property
    def right(self):
        return cp.touch_A6
       
    @property
    def down(self):
        return cp.touch_A4
       
    @property
    def left(self):
        return cp.touch_A7
        
    
    @property
    def toggle(self):
        value = cp.button_b
        debounced = (not self._toggle) and value
        self._toggle = value
        return debounced
        
    @property
    def add(self):
        value = cp.button_a
        debounced = (not self._toggle) and value
        self._add = value
        return debounced
        
    @property
    def mode(self):
        value = cp.button_b
        debounced = (not self._mode) and value
        self._mode = value
        
        if debounced:
            diff = time.monotonic() - self._mode_last
            if diff < .3:
                return True
            self._mode_last = time.monotonic()
        
        return False
        
        
        
controls = Controls()
        
    
class State:
    Idle = 0
    Move = 1
    Delay = 2
    Firing = 3
    
state = State.Idle
next_state = State.Idle
target = 0

while True:
    button = remote.poll()
    
    if state == State.Idle:
        if button == Button.StopMode or controls.mode:
            remote.clear_last_button()
            if positions:
                cp.play_tone(400, .1)
                cp.play_tone(500, .1)
                cp.play_tone(600, .1)
                cp.play_tone(700, .1)
                cp.play_tone(800, .1)
                state = State.Move 
        if button == Button.Up or controls.up:
            laser_turret.tilt += 5
        elif button == Button.Right or controls.right:
            laser_turret.pan -= 5
        elif button == Button.Down or controls.down:
            laser_turret.tilt -= 5
        elif button == Button.Left or controls.left:
            laser_turret.pan += 5
        elif button == Button.PlayPause or controls.toggle:
            laser_turret.toggle_laser()
            remote.clear_last_button()
        elif button == Button.Enter or controls.add:
            save_position()
            remote.clear_last_button()      
        elif button == Button.Back:
            clear_positions()
            remote.clear_last_button()
    
    else:
    
        if button == Button.StopMode:
            remote.clear_last_button()
            state = State.Idle
            cp.play_tone(500, .25)
            cp.play_tone(400, .25)
            laser_turret.stop()
        
    
    if state == State.Move:
        laser_turret.stop()
        
        pos = random.choice(positions)
        laser_turret.pan = pos[0]
        laser_turret.tilt = pos[1]
        
        target = time.monotonic() + random.randrange(1, 5)
        state = State.Delay
        next_state = State.Firing
    elif state == State.Firing:
        laser_turret.fire()
        cp.play_tone(500, .5)
        
        target = time.monotonic() + random.randrange(4, 10)
        state = State.Delay
        next_state = State.Move
    elif state == State.Delay:
        if time.monotonic() > target:
            state = next_state
            
    time.sleep(0.05)

