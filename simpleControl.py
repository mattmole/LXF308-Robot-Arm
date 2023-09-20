from gpiozero import Button, LED, PWMLED, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import time

factory = PiGPIOFactory(host='192.168.1.61')
Device.pin_factory = factory
led = PWMLED(17)#, pin_factory=factory)
led.on()
while 1:

    for i in range(0,100,1):
        led.value = i / 100
        time.sleep(0.05)
    led.off()
    time.sleep(1)

