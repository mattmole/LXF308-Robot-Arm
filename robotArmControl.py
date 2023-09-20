from gpiozero import Device, PWMLED, Motor
from gpiozero.pins.pigpio import PiGPIOFactory
import logging
import sys

class Pins():
    def __init__(self):
        self.pins = {"rotate":{1:None, 2:None, 3:None, "enable":None}, "shoulder":{1:None, 2:None, 3:None, "enable":None}, "elbow":{1:None, 2:None, 3:None, "enable":None}, "wrist":{1:None, 2:None, 3:None, "enable":None}, "claw":{1:None, 2:None, 3:None, "enable":None}, "led":{1:None, "enable":None}}

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
        self.led = None

        print("Remote: ", self.remote)
        #if self.raspberryPi or self.remote == True:
        #    self.createGPIODevices()   
        if self.raspberryPi:
            self.logger.info("You are running on a Raspberry Pi.")
        elif not self.raspberryPi:
            self.logger.info("You are not running on a Raspberry Pi.")
        if self.remote:
            self.logger.info("You are connecting to remote GPIO. Hardware pins will be used")
        else:
            self.logger.info("Remote GPIO is not configured")

    # Generate the GPIO objects
    def createGPIODevices(self):
        if self.raspberryPi or self.remote == True:
            motorTypesList = ["claw","shoulder","elbow","wrist","rotate"]
            for motorType in motorTypesList:
                if self.pins.pins[motorType]["enable"] and motorType in self.motorObjects:
                    self.logger.info(f"Destroying existing GPIO and creating new: {motorType}")
                    self.closeGPIO(motorType)
                if self.pins.pins[motorType]["enable"] and self.pins.pins[motorType][1] != None and self.pins.pins[motorType][2] != None and self.pins.pins[motorType][3] != None:
                    self.motorObjects[motorType] = Motor(self.pins.pins[motorType][1],self.pins.pins[motorType][2],pwm=True,enable=self.pins.pins[motorType][3])
                    print(self.motorObjects[motorType][0].pin)
                    pass
            if self.pins.pins["led"]["enable"] and self.led != None:
                self.logger.info("Destroying existing GPIO for LED and creating new")
                self.closeGPIO("led")
            if self.pins.pins["led"]["enable"]:           
                self.led = PWMLED(self.pins.pins["led"][1])

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

        if (self.raspberryPi or self.remote) and self.pins.pins[motorType]["enable"]:
            motor = self.motorObjects[motorType]
        
            # The direction is controlled by a function argument
            if direction == "extend" or direction == "left":
                motor.forward(self.motorSpeed)
            elif direction == "retract" or direction == "right":
                motor.backward(self.motorSpeed)
        elif not self.pins.pins[motorType]["enable"]:
            self.logger.info("Motor was not enabled")

    # A function to stop the motor
    def stopMotor(self,motorType):
        self.logger.info(f"Stop motor function called for {motorType} motor")
        if (self.raspberryPi or self.remote) and self.pins.pins[motorType]["enable"]:
            motor = self.motorObjects[motorType]
            motor.stop()
        elif not self.pins.pins[motorType]["enable"]:
            self.logger.info("Motor not enabled")
        
    # A function to control the brightness of the LED
    def controlLedBrightness(self):
        self.logger.info(f"Control LED function called for LED, with brightness {self.ledBrightness}")
        
        if (self.raspberryPi or self.remote) and self.pins.pins["led"]["enable"]:
            if not self.led.is_active:
                self.led.on()
            self.led.value = self.ledBrightness
        
    # A function to switch off the LED
    def stopLed(self):
        self.logger.info("Stop LED function called")
        if (self.raspberryPi or self.remote) and self.pins.pins["led"]["enable"]:
            self.led.off()

    def closeGPIO(self, outputType):
        if self.pins.pins[outputType]["enable"]:
            if outputType in self.motorObjects and outputType != "led":
                self.motorObjects[outputType].close()
            if outputType == "led" and self.pins.pins["led"]["enable"]:
                self.led.close()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s')    
    
    pins = Pins()
    pins.pins["led"][1] = "GPIO17"
    pins.pins["led"]["enable"] = True
    pins.pins["claw"][1] = "GPIO2"
    pins.pins["claw"][2] = "GPIO3"
    pins.pins["claw"][3] = "GPIO4"
    pins.pins["claw"]["enable"] = True

    # Creating an object
    logger = logging.getLogger()
 
    # Setting the threshold of logger to INFO
    logger.setLevel(logging.INFO)
    
    a = RobotArmControl(pins,1,1, logger = logger, remote=True)
    a.createGPIODevices()
    a.createGPIODevices()
    while 1:
        char = input()

        if char == "f":
            a.driveMotor("claw","retract")
        elif char == "b":
            a.driveMotor("claw","extend")
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
            #a.closeGPIO()
            sys.exit()