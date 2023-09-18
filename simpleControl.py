from gpiozero import Button, LED, PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import time

factory = PiGPIOFactory(host='192.168.1.61')
led = PWMLED(17, pin_factory=factory)
while 1:
    led.on()

    time.sleep(1)

    led.off()

    time.sleep(1)