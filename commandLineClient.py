from robotArmControl import RobotArmControl
import logging
import sys

class Pins():
    def __init__(self):
        self.pins = {}
        self.pins["rotate"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["shoulder"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["elbow"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["wrist"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["claw"] = {1:None, 2:None, 3:None, "enable":False}
        self.pins["led"] = {1:None, "enable":False}

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s')    
    
    pins = Pins()
    pins.pins["led"][1] = "GPIO17"
    pins.pins["led"]["enable"] = True
    pins.pins["claw"][1] = "GPIO2"
    pins.pins["claw"][2] = "GPIO3"
    pins.pins["claw"][3] = "GPIO4"
    pins.pins["claw"]["enable"] = True

    # Creating an object for logging
    logger = logging.getLogger()
 
    # Setting the threshold of logger to INFO
    logger.setLevel(logging.INFO)
    
    # Create
    a = RobotArmControl(pins,1,1, logger = logger, remote=False)
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
            sys.exit()