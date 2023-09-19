from gpiozero import Button, LED, PWMLED, Motor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import time

factory = PiGPIOFactory(host='192.168.1.61')
Device.pin_factory = factory
led = PWMLED("GPIO17")
motor = Motor("GPIO2", "GPIO3", enable="GPIO4")
while 1:
    try:
        led.on()

        time.sleep(1)
        motor.forward(0.5)

        led.off()

        time.sleep(1)
        motor.backward(0.5)
    except:
        motor.stop()