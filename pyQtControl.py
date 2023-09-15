from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QMenu, QSlider, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from rich import print
from robotArmControl import RobotArmControl
import logging

font = QFont("Arial", 14)

class Pins():
    def __init__(self):
        self.pins = {"rotate":{1:None, 2:None, 3:None}, "shoulder":{1:None, 2:None, 3:None}, "elbow":{1:None, 2:None, 3:None}, "wrist":{1:None, 2:None, 3:None}, "claw":{1:None, 2:None, 3:None}, "led":{1:None}}

class CustomQLabel(QLabel):
    def __init__(self,text,font = font):
        super().__init__(text)
        self.setFont(font)

class CustomQPushButton(QPushButton):
    def __init__(self,text,font = font):
        super().__init__(text)
        self.setFont(font)

class CustomQComboBox(QComboBox):
    def __init__(self, font=font):
        super().__init__()
        self.setFont(font)

class ConfigWindow(QMainWindow):
    def __init__(self, pins, logger, windowWidth = 400, windowHeight = 800):
        super().__init__()

        self.logger = logger

        self.pins = pins

        #Set the window sizes
        self.setMaximumHeight(windowHeight)
        self.setMaximumWidth(windowWidth)
        self.setMinimumHeight(windowHeight)
        self.setMinimumWidth(windowWidth)

        # Set the window's title
        self.setWindowTitle("Configure the Robot Arm Controller")

        # Add widgets required for the connection
        spacerLabel = CustomQLabel("")

        # Valid pins for GPIO can be added to the combo box
        pinChoices = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,27,28,29,31,32,33,35,36,37,38,40]
        pinChoicesStr = []
        for pin in pinChoices:
            pinChoicesStr.append(str(pin))

        # Objects for defining shoulder motor pins
        shoulderPinsLabel = CustomQLabel("Define pins used for the shoulder motor")
        shoulderPin1Label = CustomQLabel("Pin 1")
        shoulderPin2Label = CustomQLabel("Pin 2")
        shoulderPin3Label = CustomQLabel("Speed")
        shoulderPin1Combo = CustomQComboBox()
        shoulderPin1Combo.addItems(pinChoicesStr)
        shoulderPin2Combo = CustomQComboBox()
        shoulderPin2Combo.addItems(pinChoicesStr)
        shoulderPin3Combo = CustomQComboBox()
        shoulderPin3Combo.addItems(pinChoicesStr)
        shoulderHLayout = QHBoxLayout()
        shVLayout1 = QVBoxLayout()
        shVLayout2 = QVBoxLayout()
        shVLayout3 = QVBoxLayout()
        shVLayout1.addWidget(shoulderPin1Label)
        shVLayout1.addWidget(shoulderPin1Combo)
        shVLayout2.addWidget(shoulderPin2Label)
        shVLayout2.addWidget(shoulderPin2Combo)
        shVLayout3.addWidget(shoulderPin3Label)
        shVLayout3.addWidget(shoulderPin3Combo)
        shoulderHLayout.addLayout(shVLayout1)
        shoulderHLayout.addLayout(shVLayout2)
        shoulderHLayout.addLayout(shVLayout3)

        # Objects for defining elbow motor pins
        elbowPinsLabel = CustomQLabel("Define pins used for the elbow motor")
        elbowPin1Label = CustomQLabel("Pin 1")
        elbowPin2Label = CustomQLabel("Pin 2")
        elbowPin3Label = CustomQLabel("Speed")
        elbowPin1Combo = CustomQComboBox()
        elbowPin1Combo.addItems(pinChoicesStr)
        elbowPin2Combo = CustomQComboBox()
        elbowPin2Combo.addItems(pinChoicesStr)
        elbowPin3Combo = CustomQComboBox()
        elbowPin3Combo.addItems(pinChoicesStr)
        elbowHLayout = QHBoxLayout()
        elVLayout1 = QVBoxLayout()
        elVLayout2 = QVBoxLayout()
        elVLayout3 = QVBoxLayout()
        elVLayout1.addWidget(elbowPin1Label)
        elVLayout1.addWidget(elbowPin1Combo)
        elVLayout2.addWidget(elbowPin2Label)
        elVLayout2.addWidget(elbowPin2Combo)
        elVLayout3.addWidget(elbowPin3Label)
        elVLayout3.addWidget(elbowPin3Combo)
        elbowHLayout.addLayout(elVLayout1)
        elbowHLayout.addLayout(elVLayout2)
        elbowHLayout.addLayout(elVLayout3)

        # Objects for defining wrist motor pins
        wristPinsLabel = CustomQLabel("Define pins used for the wrist motor")
        wristPin1Label = CustomQLabel("Pin 1")
        wristPin2Label = CustomQLabel("Pin 2")
        wristPin3Label = CustomQLabel("Speed")
        wristPin1Combo = CustomQComboBox()
        wristPin1Combo.addItems(pinChoicesStr)
        wristPin2Combo = CustomQComboBox()
        wristPin2Combo.addItems(pinChoicesStr)
        wristPin3Combo = CustomQComboBox()
        wristPin3Combo.addItems(pinChoicesStr)
        wristHLayout = QHBoxLayout()
        wrVLayout1 = QVBoxLayout()
        wrVLayout2 = QVBoxLayout()
        wrVLayout3 = QVBoxLayout()
        wrVLayout1.addWidget(wristPin1Label)
        wrVLayout1.addWidget(wristPin1Combo)
        wrVLayout2.addWidget(wristPin2Label)
        wrVLayout2.addWidget(wristPin2Combo)
        wrVLayout3.addWidget(wristPin3Label)
        wrVLayout3.addWidget(wristPin3Combo)
        wristHLayout.addLayout(wrVLayout1)
        wristHLayout.addLayout(wrVLayout2)
        wristHLayout.addLayout(wrVLayout3)

        # Objects for defining claw motor pins
        clawPinsLabel = CustomQLabel("Define pins used for the claw motor")
        clawPin1Label = CustomQLabel("Pin 1")
        clawPin2Label = CustomQLabel("Pin 2")
        clawPin3Label = CustomQLabel("Speed")
        clawPin1Combo = CustomQComboBox()
        clawPin1Combo.addItems(pinChoicesStr)
        clawPin2Combo = CustomQComboBox()
        clawPin2Combo.addItems(pinChoicesStr)
        clawPin3Combo = CustomQComboBox()
        clawPin3Combo.addItems(pinChoicesStr)
        clawHLayout = QHBoxLayout()
        clawVLayout1 = QVBoxLayout()
        clawVLayout2 = QVBoxLayout()
        clawVLayout3 = QVBoxLayout()
        clawVLayout1.addWidget(clawPin1Label)
        clawVLayout1.addWidget(clawPin1Combo)
        clawVLayout2.addWidget(clawPin2Label)
        clawVLayout2.addWidget(clawPin2Combo)
        clawVLayout3.addWidget(clawPin3Label)
        clawVLayout3.addWidget(clawPin3Combo)
        clawHLayout.addLayout(clawVLayout1)
        clawHLayout.addLayout(clawVLayout2)
        clawHLayout.addLayout(clawVLayout3)


        # Objects for defining rotate motor pins
        rotatePinsLabel = CustomQLabel("Define pins used for the rotate motor")
        rotatePin1Label = CustomQLabel("Pin 1")
        rotatePin2Label = CustomQLabel("Pin 2")
        rotatePin3Label = CustomQLabel("Speed")
        rotatePin1Combo = CustomQComboBox()
        rotatePin1Combo.addItems(pinChoicesStr)
        rotatePin2Combo = CustomQComboBox()
        rotatePin2Combo.addItems(pinChoicesStr)
        rotatePin3Combo = CustomQComboBox()
        rotatePin3Combo.addItems(pinChoicesStr)
        rotateHLayout = QHBoxLayout()
        rotateVLayout1 = QVBoxLayout()
        rotateVLayout2 = QVBoxLayout()
        rotateVLayout3 = QVBoxLayout()
        rotateVLayout1.addWidget(rotatePin1Label)
        rotateVLayout1.addWidget(rotatePin1Combo)
        rotateVLayout2.addWidget(rotatePin2Label)
        rotateVLayout2.addWidget(rotatePin2Combo)
        rotateVLayout3.addWidget(rotatePin3Label)
        rotateVLayout3.addWidget(rotatePin3Combo)
        rotateHLayout.addLayout(rotateVLayout1)
        rotateHLayout.addLayout(rotateVLayout2)
        rotateHLayout.addLayout(rotateVLayout3)

        # Objects for defining LED pins
        ledPinLabel = CustomQLabel("Define pin used for the LED")
        ledPinCombo = CustomQComboBox()
        ledPinCombo.addItems(pinChoicesStr)
        ledHLayout = QHBoxLayout()
        ledHLayout.addWidget(ledPinCombo)
        ledHLayout.addWidget(spacerLabel)

        vLayout = QVBoxLayout()
        vLayout.addWidget(rotatePinsLabel)
        vLayout.addLayout(rotateHLayout)
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(shoulderPinsLabel)
        vLayout.addLayout(shoulderHLayout)
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(elbowPinsLabel)
        vLayout.addLayout(elbowHLayout)
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(wristPinsLabel)
        vLayout.addLayout(wristHLayout)
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(clawPinsLabel)
        vLayout.addLayout(clawHLayout)
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(ledPinLabel)
        vLayout.addLayout(ledHLayout)

        # Set the pins in the pin object to the original value
        for pinType in self.pins.pins:
            for pin in self.pins.pins[pinType]:
                self.pins.pins[pinType][pin] = pinChoices[0]

        # Add the signals for setting the pins
        rotatePin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"rotate",1))
        rotatePin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"rotate",2))
        rotatePin3Combo.textActivated.connect(lambda x: self.setPinValue(x,"rotate",3))
        shoulderPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"shoulder",1))
        shoulderPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"shoulder",2))
        shoulderPin3Combo.textActivated.connect(lambda x: self.setPinValue(x,"shoulder",3))
        elbowPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"elbow",1))
        elbowPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"elbow",2))
        elbowPin3Combo.textActivated.connect(lambda x: self.setPinValue(x,"elbow",3))
        wristPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"wrist",1))
        wristPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"wrist",2))
        wristPin3Combo.textActivated.connect(lambda x: self.setPinValue(x,"wrist",3))
        clawPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"claw",1))
        clawPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"claw",2))
        clawPin3Combo.textActivated.connect(lambda x: self.setPinValue(x,"claw",3))
        ledPinCombo.textActivated.connect(lambda x: self.setPinValue(x,"led",1))

        # Create a widget, define the vLayout to it and then assign the widget to be the main widget of the main window
        widget = QWidget()
        widget.setLayout(vLayout)
        self.setCentralWidget(widget)

    #Set the pin values in the pins object when the combo boxes are used
    def setPinValue(self, arg, pinType, pinNumber):
        self.pins.pins[pinType][pinNumber] = int(arg)

class MainWindow(QMainWindow):

    def __init__(self, configWindow, pins, logger, windowWidth = 400, windowHeight = 700):
        super().__init__()

        # Variables to hold useful values
        self.motorSpeed = 1
        self.ledBrightness = 1

        #Set the window sizes
        self.setMaximumHeight(windowHeight)
        self.setMaximumWidth(windowWidth)
        self.setMinimumHeight(windowHeight)
        self.setMinimumWidth(windowWidth)

        self.logger = logger
        self.configWindow = configWindow
        self.pins = pins

        self.robotArmControl = RobotArmControl(self.pins, self.motorSpeed, self.ledBrightness, self.logger)

        # Set the window's title
        self.setWindowTitle("Robot Arm Controller")

        # Create a vertical layout object to hold other widgets and layouts
        vLayout = QVBoxLayout()

        # Create a label to use for spacers
        spacerLabel = CustomQLabel("")

        # Create the menu bar
        menuBar = self.menuBar()
        menuBar.setFont(font)
        configureMenu = menuBar.addMenu("&Configure")
        configureMenu.setFont(font)
        configApiMenuAction = configureMenu.addAction("Configure Pins")

        #Connect signals to slots to show the other windows when the menu options are clicked
        configApiMenuAction.triggered.connect(self.showConfigWindow)

        # Create the required widgets for controlling the speed of the motors
        speedLabel = CustomQLabel("Movement Speed")
        speedSlider = QSlider(Qt.Orientation.Horizontal)
        speedSlider.setMinimum(0)
        speedSlider.setMaximum(255)
        speedSlider.setValue(255)

        # Create the widgets for the rotation buttons
        rotateLabel = CustomQLabel("Rotation")
        leftRotateButton = CustomQPushButton("&Left")
        rightRotateButton = CustomQPushButton("R&ight")
        rotateHLayout = QHBoxLayout()
        rotateHLayout.addWidget(leftRotateButton)
        rotateHLayout.addWidget(rightRotateButton)

        # Create the widgets for the shoulder joint buttons
        shoulderLabel = CustomQLabel("Shoulder Joint")
        extendShoulderButton = CustomQPushButton("E&xtend")
        retractShoulderButton = CustomQPushButton("R&etract")
        shoulderHLayout = QHBoxLayout()
        shoulderHLayout.addWidget(extendShoulderButton)
        shoulderHLayout.addWidget(retractShoulderButton)

        # Create the widgets for the elbow joint buttons
        elbowLabel = CustomQLabel("Elbow Joint")
        extendElbowButton = CustomQPushButton("Ex&tend")
        retractElbowButton = CustomQPushButton("Retr&act")
        elbowHLayout = QHBoxLayout()
        elbowHLayout.addWidget(extendElbowButton)
        elbowHLayout.addWidget(retractElbowButton)

        # Create the widgets for the wrist joint buttons
        wristLabel = CustomQLabel("Wrist Joint")
        extendWristButton = CustomQPushButton("Exte&nd")
        retractWristButton = CustomQPushButton("&Retract")
        wristHLayout = QHBoxLayout()
        wristHLayout.addWidget(extendWristButton)
        wristHLayout.addWidget(retractWristButton)

        # Create the widgets for the claw joint buttons
        clawLabel = CustomQLabel("Claw Joint")
        openClawButton = CustomQPushButton("&Close")
        closeClawButton = CustomQPushButton("&Open")
        clawHLayout = QHBoxLayout()
        clawHLayout.addWidget(closeClawButton)
        clawHLayout.addWidget(openClawButton)

        # Create the widgets for the LED buttons and slider
        ledLabel = CustomQLabel("Light")
        ledButton = CustomQPushButton("On")
        ledButton.setCheckable(True)
        self.ledSlider = QSlider(Qt.Orientation.Horizontal)
        self.ledSlider.setMinimum(0)
        self.ledSlider.setMaximum(255)
        self.ledSlider.setValue(255)
        self.ledSlider.setDisabled(True)

        ledHLayout = QHBoxLayout()
        ledHLayout.addWidget(ledButton)
        ledHLayout.addWidget(self.ledSlider)

        # Create the layout for the main window
        vLayout.addWidget(speedLabel)
        vLayout.addWidget(speedSlider)
    
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(shoulderLabel)
        vLayout.addLayout(shoulderHLayout)

        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(elbowLabel)
        vLayout.addLayout(elbowHLayout)

        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(wristLabel)
        vLayout.addLayout(wristHLayout)
        
        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(clawLabel)
        vLayout.addLayout(clawHLayout)

        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(ledLabel)
        vLayout.addLayout(ledHLayout)

        vLayout.addWidget(spacerLabel)
        vLayout.addWidget(rotateLabel)
        vLayout.addLayout(rotateHLayout)

        # Create a widget, define the vLayout to it and then assign the widget to be the main widget of the main window
        widget = QWidget()
        widget.setLayout(vLayout)
        self.setCentralWidget(widget)

        self.show()

        # Use signals to link all buttons, sliders etc to functions (slots)
        speedSlider.valueChanged.connect(self.setMotorSpeed)
        self.ledSlider.valueChanged.connect(self.setLedBrightness)
        self.ledSlider.valueChanged.connect(self.sendLedBrightness)
        leftRotateButton.pressed.connect(lambda: self.buttonPressed("rotate","left"))
        leftRotateButton.released.connect(lambda: self.buttonReleased("rotate","left"))
        rightRotateButton.pressed.connect(lambda: self.buttonPressed("rotate","right"))
        rightRotateButton.released.connect(lambda: self.buttonReleased("rotate","right"))
        extendShoulderButton.pressed.connect(lambda: self.buttonPressed("shoulder", "extend"))
        extendShoulderButton.released.connect(lambda: self.buttonReleased("shoulder", "extend"))
        retractShoulderButton.pressed.connect(lambda: self.buttonPressed("shoulder","retract"))
        retractShoulderButton.released.connect(lambda: self.buttonReleased("shoulder","retract"))
        extendElbowButton.pressed.connect(lambda: self.buttonPressed("elbow","extend"))
        extendElbowButton.released.connect(lambda: self.buttonReleased("elbow","extend"))
        retractElbowButton.pressed.connect(lambda: self.buttonPressed("elbow", "retract"))
        retractElbowButton.released.connect(lambda: self.buttonReleased("elbow", "retract"))
        extendWristButton.pressed.connect(lambda: self.buttonPressed("wrist", "extend"))
        extendWristButton.released.connect(lambda: self.buttonReleased("wrist", "extend"))
        retractWristButton.pressed.connect(lambda: self.buttonPressed("wrist","retract"))
        retractWristButton.released.connect(lambda: self.buttonReleased("wrist","retract"))
        openClawButton.pressed.connect(lambda: self.buttonPressed("claw", "open"))
        openClawButton.released.connect(lambda: self.buttonReleased("claw", "open"))
        closeClawButton.pressed.connect(lambda: self.buttonPressed("claw","close"))
        closeClawButton.released.connect(lambda: self.buttonReleased("claw","close"))
        ledButton.toggled.connect(self.ledButtonPressed)

    # Slot used when window is closed
    def closeEvent(self, args):
        if self.configWindow.isVisible():
            self.configWindow.close()
        
    # Slot used to show the config window
    def showConfigWindow(self):
        self.configWindow.show()

    # Create a function to set the speed instance variable
    def setMotorSpeed(self,speedValue):
        self.motorSpeed = speedValue / 255
        self.robotArmControl.motorSpeed = self.motorSpeed
        
    # Create a function to set the LED brightness variable
    def setLedBrightness(self, brightnessValue):
        self.ledBrightness = brightnessValue / 255

    # Create a function to handle if a motor control button is pressed
    def buttonPressed(self, motorType, direction):
        self.robotArmControl.motorSpeed = self.motorSpeed
        self.robotArmControl.setMotorSpeed(motorType)
        self.robotArmControl.driveMotor(motorType, direction)

    def buttonReleased(self,motorType, direction):
        self.robotArmControl.stopMotor(motorType)

    # Create a function to handle if the LED control button is pressed
    def ledButtonPressed(self, buttonState):
        if buttonState:
            self.ledSlider.setDisabled(False)
            self.robotArmControl.controlLedBrightness(self.ledBrightness)
        else:
            self.robotArmControl.stopLed()
            self.ledSlider.setDisabled(True)

    # Create a function to send a different brightness value when the LED brightness slider is changed
    def sendLedBrightness(self):
        self.robotArmControl.controlLedBrightness(self.ledBrightness)

class CustomQApplication(QApplication):
    def __init__(self,args):
        super().__init__(args)
        logging.basicConfig(format='%(asctime)s %(message)s')    

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.INFO)

        pins = Pins()
        configWindow = ConfigWindow(pins, logger)
        mainWindow = MainWindow(configWindow, pins, logger)

        self.exec()


if __name__ == "__main__":
    
    app = CustomQApplication([])

    #app.exec()