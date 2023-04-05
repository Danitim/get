import RPi.GPIO as GPIO
from time import sleep
from math import floor

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
cmp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(cmp, GPIO.IN)

def dec2bin(value):
    return [int (element) for element in bin(value)[2:].zfill(8)]

def set_volume(val):
    val = floor(val*2**8/58)
    vol = [0] * 8
    k = 1
    for i in range(7, -1, -1):
        if val < k:
            break
        vol[i] = 1
        k += 32
    GPIO.output(leds, vol)

def adc():
    val = 0
    for i in range(7, -1, -1):
        val += 2**i
        GPIO.output(dac, dec2bin(val))
        sleep(0.005)
        comp = GPIO.input(cmp)
        if comp == 0:
            val -= 2**i
    return val

try:
    while True:
        value = adc()
        set_volume(value)
        print(value, '{:.2f}'.format(3.3*value/256))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
