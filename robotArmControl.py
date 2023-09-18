from gpiozero import Device, PWMLED, LED, Motor
import logging
import sys

class Pins():
    def __init__(self):
        self.pins = {"rotate":{1:None, 2:None, 3:None}, "shoulder":{1:None, 2:None, 3:None}, "elbow":{1:None, 2:None, 3:None}, "wrist":{1:None, 2:None, 3:None}, "claw":{1:None, 2:None, 3:None}, "led":{1:None}}

class RobotArmControl():

    # Initialise the class and set some instance variables
    def __init__(self,pins,motorSpeed,ledBrightness, logger):
        self.logger = logger
        self.raspberryPi = self.isRaspberryPi()

        self.pins = pins
        self.motorSpeed = motorSpeed
        self.ledBrightness = ledBrightness

        self.motorObjects = {}
        self.motorSpeedObjects = {}

        if self.raspberryPi:

            motorTypesList = ["claw","shoulder","elbow","wrist","claw"]
            for motorType in motorTypesList:
                self.motorObjects[motorType] = Motor(self.pins.pins[motorType][1],self.pins.pins[motorType][2])
                self.motorSpeedObjects[motorType] = PWMLED(self.pins.pins[motorType][3])
            self.led = LED(self.pins.pins["led"][1])

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

        if self.raspberryPi:
            motor = self.motorObjects[motorType]
        
            # The direction is controlled by a function argument
            if direction == "extend" or direction == "left":
                motor.forward(self.motorSpeed)
            elif direction == "retract" or direction == "right":
                motor.backward(self.motorSpeed)

    # A function to set the motor speeds
    def setMotorSpeed(self, motorType):
        self.logger.info(f"Drive speed function called for {motorType} motor, with speed {self.motorSpeed}")
        if self.raspberryPi:
            motorSpeed = self.motorSpeedObjects[motorType]
            motorSpeed.value = self.motorSpeed

    # A function to stop the motor
    def stopMotor(self,motorType):
        self.logger.info(f"Stop motor function called for {motorType} motor")
        if self.raspberryPi:
            motor = self.motorObjects[motorType]
            motor.stop()
        
    # A function to control the brightness of the LED
    def controlLedBrightness(self, ledBrightness):
        self.ledBrightness = ledBrightness
        self.logger.info(f"Control LED function called for LED, with brightness {self.ledBrightness}")
        
        if self.raspberryPi:
            if not self.led.is_active:
                self.led.on()
            self.led.value = self.ledBrightness
        
    # A function to switch off the LED
    def stopLed(self):
        self.logger.info("Stop LED function called")
        if self.raspberryPi:
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
    
    a = RobotArmControl(pins,1,1, logger = logger)

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
            a.setMotorSpeed("claw")
        elif char == "2":
            a.motorSpeed = 0.6666
            a.setMotorSpeed("claw")
        elif char == "3":
            a.motorSpeed = 0.9999
            a.setMotorSpeed("claw")
        elif char == "q":
            sys.exit()