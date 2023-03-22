import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(value):
    return [int (element) for element in bin(value)[2:].zfill(8)]

x = 0
dx = 1
try:
    t = int(input("Enter signal period: "))
    while True:
        if x == 255: dx = -1
        elif x == 0: dx = 1
        x += dx
        for i in range(len(dac)): GPIO.output(dac[i], dec2bin(x)[i])
        time.sleep(t/256)
except ValueError:
    print("Not an valid value")
finally:
    for elem in dac: GPIO.output(elem, 0)
    GPIO.cleanup()