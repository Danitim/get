import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(15, gpio.OUT)
gpio.setup(14, gpio.IN)

while True:
    gpio.output(15, gpio.input(14))