''' Receive and print IR codes.

Useful for determining which codes map to buttons on a remote.
'''

import board
import pulseio
import time

from remote import NecRemote
from settings import Button, Pin
from turret import Turret

ir_pulses = pulseio.PulseIn(board.IR_RX, maxlen=500, idle_state=True)
remote = NecRemote(ir_pulses)

laser_turret = Turret(Pin.PAN, Pin.TILT, Pin.LASER)

print('Receiving IR')
target = 90
while True:
    button = remote.poll()
    if button is not None:
        print(button)

    if button == Button.Right:
        target -= 5
        target = max(target, 0)
        laser_turret.pan.angle = target
    elif button == Button.Left:
        target += 5
        target = min(target, 180)
        laser_turret.pan.angle = target        
    elif button == Button.PlayPause:
        laser_turret.laser.value = not laser_turret.laser.value
        remote.clear_last_button()

