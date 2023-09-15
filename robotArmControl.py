from gpiozero import Device, PWMLED, LED, Motor
import logging

class RobotArmControl():

    # Initialise the class and set some instance variables
    def __init__(self,pins,motorSpeed,ledBrightness, logger):
        self.logger = logger
        self.raspberryPi = self.isRaspberryPi()

        if not self.raspberryPi:
            self.logger.info("You are not running on a Raspberry Pi. Real hardware interaction will be disabled")
        else:
            self.logger.info("You are running on a Raspberry Pi. Hardware pins will be used")
        self.pins = pins
        self.motorSpeed = motorSpeed
        self.ledBrightness = ledBrightness

        print(self.isRaspberryPi())

    # Determine if the code is running on a Raspberry Pi
    def isRaspberryPi(self):
        try:
            with open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): 
                    return True
        except Exception: 
            pass
        return False
    
    
    # # Function to drive the shoulder motor
    # def driveShoulderMotor(self,direction):
    #     self.logger.info(f"Switch-on called for shoulder motor, with direction {direction}")
    #     motorType="shoulder"
    #     self.driveMotor(motorType, direction)
    
    # # Function to drive the elbow motor
    # def driveElbowMotor(self,direction):
    #     self.logger.info(f"Switch-on called for elbow motor, with direction {direction}")
    #     motorType="elbow"
    #     self.driveMotor(motorType, direction)
    
    # # Function to drive the wrist motor
    # def driveWristMotor(self,direction):
    #     self.logger.info(f"Switch-on called for wrist motor, with direction {direction}")
    #     motorType="wrist"
    #     self.driveMotor(motorType, direction)
    
    # # Function to drive the claw motor
    # def driveClawMotor(self,direction):
    #     self.logger.info(f"Switch-on called for claw motor, with direction {direction}")
    #     motorType="claw"
    #     self.driveMotor(motorType, direction) 
    
    # # Function to drive the rotate motor
    # def driveRotateMotor(self,direction):
    #     self.logger.info(f"Switch-on called for rotate motor, with direction {direction}")
    #     motorType="rotate"
    #     self.driveMotor(motorType, direction)
        
    # Function to drive a motor, with the type defined by the previous functions
    def driveMotor(self,motorType, direction):
        self.logger.info(f"Drive motor function called for {motorType} motor, with direction {direction}")
        pins = self.pins.pins[motorType]
        pin1 = pins[1]
        pin2 = pins[2]

        if self.raspberryPi:
            motor = Motor(pin1, pin2, pwm=True)
        
            # The direction is controlled by a function argument
            if direction == "extend" or direction == "left":
                motor.forward(self.motorSpeed)
            elif direction == "retract" or direction == "right":
                motor.backward(self.motorSpeed)

    # A function to set the motor speeds
    def setMotorSpeed(self, motorType):
        self.logger.info(f"Drive speed function called for {motorType} motor, with speed {self.motorSpeed}")
        pins = self.pins.pins[motorType]
        pin1 = pins[1]
        if self.raspberryPi:
            motorSpeed = PWMLED(pin1)
            motorSpeed.value = self.motorSpeed

    # A function to stop the motor
    def stopMotor(self,motorType):
        self.logger.info(f"Stop motor function called for {motorType} motor")
        if self.raspberryPi:
            pins = self.pins.pins[motorType]
            pin1 = pins[1]
            pin2 = pins[2]
            motor = Motor(pin1, pin2)
            motor.stop()
        
    # A function to control the brightness of the LED
    def controlLedBrightness(self, ledBrightness):
        self.ledBrightness = ledBrightness
        self.logger.info(f"Control LED function called for LED, with brightness {self.ledBrightness}")
        pin = self.pins.pins["led"][1]
    
        if self.raspberryPi:
            led = PWMLED(pin)
            if not led.is_active:
                led.on()
            led.value = self.ledBrightness
        
    # A function to switch off the LED
    def stopLed(self):
        self.logger.info("Stop LED function called")
        if self.raspberryPi:
            pin = self.pins.pins["led"][1]
            led = LED(pin)
            led.off()
    
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s')    
    
    # Creating an object
    logger = logging.getLogger()
 
    # Setting the threshold of logger to INFO
    logger.setLevel(logging.INFO)
    
    a = RobotArmControl("a","b","c", logger = logger)