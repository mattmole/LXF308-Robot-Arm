from gpiozero import Device, PWMLED, Motor
from gpiozero.pins.pigpio import PiGPIOFactory
import logging
import sys

class Pins():
    """Class used to store details of the pins used for motor / LED control"""
    def __init__(self):
        self.pins = {}
        self.pins["rotate"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["shoulder"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["elbow"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["wrist"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["claw"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["led"] = {1:None, "enable":False}

class RobotArmControl():
    """Class used to interact with GPIO pins and can connect to a remote device as well"""
    def __init__(self,pins,motorSpeed,ledBrightness, logger, remote=False, remoteIP = ""):
        # Variables used to allow instance-wide access
        self.logger = logger
        self.raspberryPi = self.isRaspberryPi()

        self.remote = remote
        self.remoteIP = remoteIP
        self.factory = None

        self.pins = pins
        self.motorSpeed = motorSpeed
        self.ledBrightness = ledBrightness

        # Dictionary used to store all motor objects and a variable to store the LED object 
        self.motorObjects = {}
        self.led = None

        # Print some messages to show information
        if self.raspberryPi:
            self.logger.info("You are running on a Raspberry Pi.")
        elif not self.raspberryPi:
            self.logger.info("You are not running on a Raspberry Pi.")
        if self.remote:
            self.logger.info("You are connecting to remote GPIO. Hardware pins will be used")
        else:
            self.logger.info("Remote GPIO is not configured")

    def createGPIODevices(self):
        """Generate the GPIO objects"""
        # Connect to remote pins if this is configured
        if self.remote and self.factory == None:
            try:
                self.factory = PiGPIOFactory(host=self.remoteIP)
                Device.pin_factory = self.factory
            except IOError:
                return False
        # Generate motor objects for each defined motor
        if self.raspberryPi or self.remote == True:
            motorTypesList = ["claw","shoulder","elbow","wrist","rotate"]
            for motorType in motorTypesList:
                # Close the GPIO if already defined
                if self.pins.pins[motorType]["enable"] and motorType in self.motorObjects:
                    self.logger.info(f"Destroying existing GPIO and creating new: {motorType}")
                    self.closeGPIO(motorType)
                # Create the objects for control
                if self.pins.pins[motorType]["enable"] and self.pins.pins[motorType][1] != None and self.pins.pins[motorType][2] != None and self.pins.pins[motorType][3] != None:
                    self.motorObjects[motorType] = Motor(self.pins.pins[motorType][1],self.pins.pins[motorType][2],pwm=True,enable=self.pins.pins[motorType][3])
            # Close the PWMLED object if already defined
            if self.pins.pins["led"]["enable"] and self.led != None:
                self.logger.info("Destroying existing GPIO for LED and creating new")
                self.closeGPIO("led")
            # Create the PWMLED object
            if self.pins.pins["led"]["enable"]:           
                self.led = PWMLED(self.pins.pins["led"][1])
        return True
    
    def isRaspberryPi(self):
        """Determine if the code is running on a Raspberry Pi"""
        try:
            with open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): 
                    return True
        except Exception: 
            pass
        return False
    
    def driveMotor(self,motorType, direction):
        """Function to drive a motor, with the type defined by the previous function"""
        self.logger.info(f"Drive motor function called for {motorType} motor, with direction {direction}")

        # Use some conditions to determine whether to write to GPIO pins or to simulate
        if (self.raspberryPi or self.remote) and self.pins.pins[motorType]["enable"]:
            motor = self.motorObjects[motorType]
        
            # The direction is controlled by a function argument
            if direction == "extend" or direction == "left":
                motor.forward(self.motorSpeed)
            elif direction == "retract" or direction == "right":
                motor.backward(self.motorSpeed)
        elif not self.pins.pins[motorType]["enable"]:
            self.logger.info("Motor was not enabled")

    def stopMotor(self,motorType):
        """A function to stop the motor"""
        self.logger.info(f"Stop motor function called for {motorType} motor")
        if (self.raspberryPi or self.remote) and self.pins.pins[motorType]["enable"]:
            motor = self.motorObjects[motorType]
            motor.stop()
        elif not self.pins.pins[motorType]["enable"]:
            self.logger.info("Motor not enabled")
        
    def controlLedBrightness(self):
        """A function to control the brightness of the LED"""
        self.logger.info(f"Control LED function called for LED, with brightness {self.ledBrightness}")
        
        if (self.raspberryPi or self.remote) and self.pins.pins["led"]["enable"]:
            if not self.led.is_active:
                self.led.on()
            self.led.value = self.ledBrightness
        
    def stopLed(self):
        """A function to switch off the LED"""
        self.logger.info("Stop LED function called")
        if (self.raspberryPi or self.remote) and self.pins.pins["led"]["enable"]:
            self.led.off()

    def closeGPIO(self, outputType):
        """A function to close a GPIO device"""
        if self.pins.pins[outputType]["enable"]:
            if outputType in self.motorObjects and outputType != "led":
                self.motorObjects[outputType].close()
            if outputType == "led" and self.pins.pins["led"]["enable"]:
                self.led.close()

    def closeAllGPIO(self):
        """A function to close all GPIO objects"""
        if self.pins.pins["led"]["enable"] and self.led != None:
            self.led.close()
        motorTypesList = ["claw","shoulder","elbow","wrist","rotate"]
        for motorType in motorTypesList:
            # Close the GPIO if already defined
            if self.pins.pins[motorType]["enable"] and motorType in self.motorObjects:
                self.motorObjects[motorType].close()

if __name__ == "__main__":
    # Create a logger object
    logging.basicConfig(format='%(asctime)s %(message)s')    
    
    # Create a Pins object
    pins = Pins()
    pins.pins["led"][1] = "GPIO17"
    pins.pins["led"]["enable"] = True
    pins.pins["claw"][1] = "GPIO2"
    pins.pins["claw"][2] = "GPIO3"
    pins.pins["claw"][3] = "GPIO4"
    pins.pins["claw"]["enable"] = True

    # Configure the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create an object to control the hardware and create the necessary motor / LED objects    
    a = RobotArmControl(pins,1,1, logger = logger, remote=True, remoteIP="192.168.1.61")
    a.createGPIODevices()

    # Start an infinite loop
    while 1:
        # Request a character
        char = input()

        #Operate the relevant motors / speeds / LEDs based on the key that has been pressed
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
            a.closeAllGPIO()
            sys.exit()