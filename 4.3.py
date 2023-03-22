import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

p = GPIO.PWM(23, 1000)
p.start(0)

try:
    while True:
        f = int(input("Enter cycle period: "))
        p.ChangeDutyCycle(f)
        print(3.3 * f / 100)
finally:
    p.stop()
    GPIO.output(24, 0)
    GPIO.cleanup()