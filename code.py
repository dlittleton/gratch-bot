import board
import digitalio
import pulseio
import time

from adafruit_circuitplayground import cp
from adafruit_irremote import GenericDecode, IRNECRepeatException
from adafruit_motor import servo

ir_pulses = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
ir_decoder = GenericDecode()

laser = digitalio.DigitalInOut(board.A3)
laser.direction = digitalio.Direction.OUTPUT
laser.value = False

cp.pixels.brightness = 0.1
led_off = (0, 0, 0)
led_purple = (50, 0, 50)
led_red = (255, 0, 0)
cp.pixels.fill(led_off)

pwm_pan = pulseio.PWMOut(board.A1, duty_cycle=2**15, frequency=50)
pan = servo.Servo(pwm_pan)

print('Rotating')
fails = 0

def try_decode_ir():
    global fails
    pulse = ir_decoder.read_pulses(ir_pulses, pulse_window=0.01, blocking=False)
    if pulse:
        try:
            value = ir_decoder.decode_bits(pulse)
            print(value)
            print(value[0] ^ value[1])
            print(value[2] ^ value[3])
        except IRNECRepeatException:
            print('Repeat!')
        except:
            fails += 1
            if not fails % 10:
                print('Failures: ', fails)
            pass

while(True):
    laser.value = True
    for angle in range(0, 180, 5):
        try_decode_ir()
        #cp.pixels.fill(led_off)
        #cp.pixels[(angle - 1) // 18] = led_purple
        pan.angle = angle
        time.sleep(0.05)
      
    laser.value = False  
    for angle in range(180, 0, -5):
        try_decode_ir()
        #cp.pixels.fill(led_off)
        #cp.pixels[(angle - 1) // 18] = led_purple
        pan.angle = angle
        time.sleep(0.05)