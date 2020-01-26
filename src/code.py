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

ir_pulses = pulseio.PulseIn(board.IR_RX, maxlen=500, idle_state=True)
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
    
    
class State:
    Idle = 0
    Move = 1
    Delay = 2
    Firing = 3
    
state = State.Idle
next_state = State.Idle
target = 0

cp.play_file('resources/ready.wav')
while True:
    button = remote.poll()
    
    # Hackety hack, not buttons while running.
    # REFACTOR!
    if state != State.Idle and button != Button.StopMode:
        button = None
   
    # Press Buttons
    if button == Button.Up:
        laser_turret.tilt += 5
    elif button == Button.Right:
        laser_turret.pan -= 5
    elif button == Button.Down:
        laser_turret.tilt -= 5
    elif button == Button.Left:
        laser_turret.pan += 5
    elif button == Button.PlayPause:
        laser_turret.toggle_laser()
        remote.clear_last_button()
    elif button == Button.Enter:
        save_position()
        remote.clear_last_button()
    elif button == Button.StopMode:
        remote.clear_last_button()
        if state == State.Idle and positions:
            cp.play_file('resources/firing.wav')
            state = State.Move
        else:
            state = State.Idle
            cp.play_tone(500, .25)
            cp.play_tone(400, .25)
    elif button == Button.Back:
        clear_positions()
        remote.clear_last_button()
        
        
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

