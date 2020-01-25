''' Receive and print IR codes.

Useful for determining which codes map to buttons on a remote.
'''

import board
import pulseio
import time

from remote import NecRemote
from settings import Button

ir_pulses = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
remote = NecRemote(ir_pulses)

print('Receiving IR')

while True:
    button = remote.poll()
    if button is not None:
        print(button)
        
    if button == Button.VolumeUp:
        print('Volume Up!')
    elif button == Button.VolumeDown:
        print('Volume Down!')
    elif button == Button.Left:
        print('Left!')
    time.sleep(0.1)
        