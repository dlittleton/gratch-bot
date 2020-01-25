''' Receive and print IR codes.

Useful for determining which codes map to buttons on a remote.
'''

import board
import pulseio

from adafruit_irremote import GenericDecode, IRNECRepeatException

ir_pulses = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
ir_decoder = GenericDecode()

print('Receiving IR')

while True:
    pulse = ir_decoder.read_pulses(ir_pulses, pulse_window=0.01)
    try:
        value = ir_decoder.decode_bits(pulse)
        print(value)
    except IRNECRepeatException:
        print('Repeat')
    except:
        pass


    
    