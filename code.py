import board
import digitalio
import pulseio
import time

from adafruit_circuitplayground import cp
from adafruit_motor import servo

laser = digitalio.DigitalInOut(board.A3)
laser.direction = digitalio.Direction.OUTPUT
laser.value = False

cp.pixels.brightness = 0.1
led_off = (0, 0, 0)
led_purple = (50, 0, 50)

pwm_pan = pulseio.PWMOut(board.A1, duty_cycle=2**15, frequency=50)
pan = servo.Servo(pwm_pan)

print('Rotating')

while(True):
    laser.value = True
    for angle in range(0, 180, 5):
        cp.pixels.fill(led_off)
        cp.pixels[(angle - 1) // 18] = led_purple
        pan.angle = angle
        time.sleep(0.05)
      
    laser.value = False  
    for angle in range(180, 0, -5):
        cp.pixels.fill(led_off)
        cp.pixels[(angle - 1) // 18] = led_purple
        pan.angle = angle
        time.sleep(0.05)