import RPi.GPIO as GPIO
from time import sleep

dac = [26, 19, 13, 6, 5, 11, 9, 10]
cmp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(cmp, GPIO.IN)

def dec2bin(value):
    return [int (element) for element in bin(value)[2:].zfill(8)]

def adc():
    for x in range(256):
        GPIO.output(dac, dec2bin(x))
        sleep(0.001)
        if GPIO.input(cmp) == 0:
            return x
    return 0

try:
    while True:
        value = adc()
        if value:
            print(value, '{:.2f}'.format(3.3*value/256))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
