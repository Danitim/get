import RPi.GPIO as GPIO
import time


dac = [26, 19, 13, 6, 5, 11, 9, 10]
number = [0, 1, 0, 1, 0, 1, 0, 1]

n =    [0, 2, 5, 32, 64, 127, 255, 256]
#value  480 480 480 496 825 1625 3244 480

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

for c in range(0, 8):

    tmp = n[c]
    for i in range(0, 8):
        number[7-i] = tmp % 2
        tmp = tmp//2

    print(n[c], number)

    GPIO.output(dac, number)
    time.sleep(10)
    GPIO.output(dac, 0)

GPIO.cleanup()