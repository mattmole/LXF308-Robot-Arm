from gpiozero import Device, PWMLED, Motor
from gpiozero.pins.pigpio import PiGPIOFactory
import logging
import sys

class Pins():
    def __init__(self):
        self.pins = {"rotate":{1:None, 2:None, 3:None}, "shoulder":{1:None, 2:None, 3:None}, "elbow":{1:None, 2:None, 3:None}, "wrist":{1:None, 2:None, 3:None}, "claw":{1:None, 2:None, 3:None}, "led":{1:None}}

class RobotArmControl():

    # Initialise the class and set some instance variables
    def __init__(self,pins,motorSpeed,ledBrightness, logger, remote=False, remoteIP = "192.168.1.61"):
        self.logger = logger
        self.raspberryPi = self.isRaspberryPi()

        self.remote = remote
        self.remoteIP = remoteIP

        self.factory = PiGPIOFactory(host=self.remoteIP)
        if self.remote:
            Device.pin_factory = self.factory

        self.pins = pins
        self.motorSpeed = motorSpeed
        self.ledBrightness = ledBrightness

        self.motorObjects = {}
        self.motorSpeedObjects = {}

        print("Remote: ", self.remote)
        if self.raspberryPi or self.remote == True:

            motorTypesList = ["claw","shoulder","elbow","wrist","rotate"]
            for motorType in motorTypesList:
                if self.pins.pins[motorType][1] != None and self.pins.pins[motorType][2] != None and self.pins.pins[motorType][3] != None:
                    self.motorObjects[motorType] = Motor(self.pins.pins[motorType][1],self.pins.pins[motorType][2],pwm=True,enable=self.pins.pins[motorType][3])
                    #self.motorSpeedObjects[motorType] = PWMLED(self.pins.pins[motorType][3])
            
            self.led = PWMLED(self.pins.pins["led"][1])
        if not self.raspberryPi:
            self.logger.info("You are not running on a Raspberry Pi. Real hardware interaction will be disabled")
        else:
            self.logger.info("You are running on a Raspberry Pi. Hardware pins will be used")

    # Determine if the code is running on a Raspberry Pi
    def isRaspberryPi(self):
        try:
            with open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): 
                    return True
        except Exception: 
            pass
        return False
    

    # Function to drive a motor, with the type defined by the previous functions
    def driveMotor(self,motorType, direction):
        self.logger.info(f"Drive motor function called for {motorType} motor, with direction {direction}")

        if self.raspberryPi or self.remote:
            motor = self.motorObjects[motorType]
        
            # The direction is controlled by a function argument
            if direction == "extend" or direction == "left":
                motor.forward(self.motorSpeed)
            elif direction == "retract" or direction == "right":
                motor.backward(self.motorSpeed)

    # A function to set the motor speeds
#    def setMotorSpeed(self, motorType):
#        self.logger.info(f"Drive speed function called for {motorType} motor, with speed {self.motorSpeed}")
#f
#         if self.raspberryPi:
#            motorSpeed = self.motorSpeedObjects[motorType]
#            motorSpeed.value = self.motorSpeed

#            self.motorSpeed
    # A function to stop the motor
    def stopMotor(self,motorType):
        self.logger.info(f"Stop motor function called for {motorType} motor")
        if self.raspberryPi or self.remote:
            motor = self.motorObjects[motorType]
            motor.stop()
        
    # A function to control the brightness of the LED
    def controlLedBrightness(self):
        self.logger.info(f"Control LED function called for LED, with brightness {self.ledBrightness}")
        
        if self.raspberryPi or self.remote:
            if not self.led.is_active:
                self.led.on()
            self.led.value = self.ledBrightness
        
    # A function to switch off the LED
    def stopLed(self):
        self.logger.info("Stop LED function called")
        if self.raspberryPi or self.remote:
            self.led.off()
    
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s')    
    
    pins = Pins()
    pins.pins["led"][1] = 17
    pins.pins["claw"][1] = 2
    pins.pins["claw"][2] = 3
    pins.pins["claw"][3] = 4

    # Creating an object
    logger = logging.getLogger()
 
    # Setting the threshold of logger to INFO
    logger.setLevel(logging.INFO)
    
    a = RobotArmControl(pins,1,1, logger = logger, remote=True)

    while 1:
        char = input()

        if char == "f":
            a.driveMotor("claw","extend")
        elif char == "b":
            a.driveMotor("claw","retract")
        elif char == "s":
            a.stopMotor("claw")
        elif char == "1":
            a.motorSpeed = 0.3333
        elif char == "2":
            a.motorSpeed = 0.6666
        elif char == "3":
            a.motorSpeed = 0.9999
        elif char == "4":
            a.ledBrightness = 0.3333
            a.controlLedBrightness()
        elif char == "5":
            a.ledBrightness = 0.6666
            a.controlLedBrightness()
        elif char == "6":
            a.ledBrightness = 0.9999
            a.controlLedBrightness()
        elif char == "o":
            a.stopLed()
        elif char == "q":
            sys.exit()