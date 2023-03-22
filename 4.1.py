import RPi.GPIO as GPIO

dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(value):
    return [int (element) for element in bin(value)[2:].zfill(8)]

try:
    while True:
        s = input("Enter a number from 0 to 255: ")
        if s == 'q':
            print("Exitting...")
            break
        elif int(s) < 0 or int(s) > 255:
            print("Not a correct value")
        else:
            x = int(s)
            print("Currently outputing", 3.3*x/256, "volts")
            print(dec2bin(x))
            for i in range(len(dac)): GPIO.output(dac[i], dec2bin(x)[i])
except ValueError:
    print("This is not a integer")
finally:
    for elem in dac: GPIO.output(elem, 0)
    GPIO.cleanup()