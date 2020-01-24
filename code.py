import board
import pulseio
import time

from adafruit_motor import servo

pwm = pulseio.PWMOut(board.A1, duty_cycle=2**15, frequency=50)
pan = servo.Servo(pwm)

print('Rotating')

while(True):
    for angle in range(0, 180, 5):
        pan.angle = angle
        time.sleep(0.05)
        
    for angle in range(180, 0, -5):
        pan.angle = angle
        time.sleep(0.05)