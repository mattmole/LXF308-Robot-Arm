from gpiozero import Motor, PWMLED, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import sys

factory = PiGPIOFactory(host='192.168.1.61')
Device.pin_factory = factory

ledPin = "GPIO17"
motorPin1 = "GPIO2"
motorPin2 = "GPIO3"
motorPin3 = "GPIO4"
motorSpeed = 1

led = PWMLED(ledPin)
motor = Motor(motorPin1, motorPin2, motorPin3, pwm=True)

while 1:
    char = input()

    if char == "1":
        motorSpeed = 0.3333
    elif char == "2":
        motorSpeed = 0.6666
    elif char == "3":
        motorSpeed = 0.9999
    elif char=="4":
        led.value = 0.1111
    elif char == "5":
        led.value = 0.33333
    elif char == "6":
        led.value = 0.66666
    elif char == "7":
        led.value = 0.9999
    elif char == "o":
        led.off()
    elif char == "f":
        motor.forward()
    elif char == "b":
        motor.backward()
    elif char == "q":
        sys.exit()
