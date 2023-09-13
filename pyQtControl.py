from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QMenu, QSlider, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from rich import print

font = QFont("Arial", 14)

class Pins():
    def __init__(self):
        self.pins = {"rotate":{1:None, 2:None}, "shoulder":{1:None, 2:None}, "elbow":{1:None, 2:None}, "wrist":{1:None, 2:None}, "claw":{1:None, 2:None}, "led":{1:None}}

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
    def __init__(self, pins, windowWidth = 400, windowHeight = 600):
        super().__init__()

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
        shoulderPin1Combo = CustomQComboBox()
        shoulderPin1Combo.addItems(pinChoicesStr)
        shoulderPin2Combo = CustomQComboBox()
        shoulderPin2Combo.addItems(pinChoicesStr)
        shoulderHLayout = QHBoxLayout()
        shoulderHLayout.addWidget(shoulderPin1Combo)
        shoulderHLayout.addWidget(shoulderPin2Combo)

        # Objects for defining elbow motor pins
        elbowPinsLabel = CustomQLabel("Define pins used for the elbow motor")
        elbowPin1Combo = CustomQComboBox()
        elbowPin1Combo.addItems(pinChoicesStr)
        elbowPin2Combo = CustomQComboBox()
        elbowPin2Combo.addItems(pinChoicesStr)
        elbowHLayout = QHBoxLayout()
        elbowHLayout.addWidget(elbowPin1Combo)
        elbowHLayout.addWidget(elbowPin2Combo)

        # Objects for defining elbow motor pins
        wristPinsLabel = CustomQLabel("Define pins used for the elbow motor")
        wristPin1Combo = CustomQComboBox()
        wristPin1Combo.addItems(pinChoicesStr)
        wristPin2Combo = CustomQComboBox()
        wristPin2Combo.addItems(pinChoicesStr)
        wristHLayout = QHBoxLayout()
        wristHLayout.addWidget(wristPin1Combo)
        wristHLayout.addWidget(wristPin2Combo)

        # Objects for defining claw motor pins
        clawPinsLabel = CustomQLabel("Define pins used for the claw motor")
        clawPin1Combo = CustomQComboBox()
        clawPin1Combo.addItems(pinChoicesStr)
        clawPin2Combo = CustomQComboBox()
        clawPin2Combo.addItems(pinChoicesStr)
        clawHLayout = QHBoxLayout()
        clawHLayout.addWidget(clawPin1Combo)
        clawHLayout.addWidget(clawPin2Combo)


        # Objects for defining rotate motor pins
        rotatePinsLabel = CustomQLabel("Define pins used for the rotate motor")
        rotatePin1Combo = CustomQComboBox()
        rotatePin1Combo.addItems(pinChoicesStr)
        rotatePin2Combo = CustomQComboBox()
        rotatePin2Combo.addItems(pinChoicesStr)
        rotateHLayout = QHBoxLayout()
        rotateHLayout.addWidget(rotatePin1Combo)
        rotateHLayout.addWidget(rotatePin2Combo)

        # Objects for defining rotate motor pins
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
        self.pins.pins["rotate"][1] = pinChoices[0]
        self.pins.pins["rotate"][2] = pinChoices[0]
        self.pins.pins["shoulder"][1] = pinChoices[0]
        self.pins.pins["shoulder"][2] = pinChoices[0]
        self.pins.pins["elbow"][1] = pinChoices[0]
        self.pins.pins["elbow"][2] = pinChoices[0]
        self.pins.pins["wrist"][1] = pinChoices[0]
        self.pins.pins["wrist"][2] = pinChoices[0]
        self.pins.pins["claw"][1] = pinChoices[0]
        self.pins.pins["claw"][2] = pinChoices[0]
        self.pins.pins["led"][1] = pinChoices[0]

        # Add the signals for setting the pins
        rotatePin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"rotate",1))
        rotatePin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"rotate",2))
        shoulderPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"shoulder",1))
        shoulderPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"shoulder",2))
        elbowPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"elbow",1))
        elbowPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"elbow",2))
        wristPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"wrist",1))
        wristPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"wrist",2))
        clawPin1Combo.textActivated.connect(lambda x: self.setPinValue(x,"claw",1))
        clawPin2Combo.textActivated.connect(lambda x: self.setPinValue(x,"claw",2))
        ledPinCombo.textActivated.connect(lambda x: self.setPinValue(x,"led",1))

        # Create a widget, define the vLayout to it and then assign the widget to be the main widget of the main window
        widget = QWidget()
        widget.setLayout(vLayout)
        self.setCentralWidget(widget)

    #Set the pin values in the pins object when the combo boxes are used
    def setPinValue(self, arg, pinType, pinNumber):
        self.pins.pins[pinType][pinNumber] = int(arg)


class MainWindow(QMainWindow):

    def __init__(self, configWindow, pins, windowWidth = 400, windowHeight = 700):
        super().__init__()

        self.configWindow = configWindow
        self.pins = pins

        # Set the window's title
        self.setWindowTitle("Robot Arm Controller")


        # Variables to hold useful values
        self.motorSpeed = 1
        self.ledBrightness = 1

        #Set the window sizes
        self.setMaximumHeight(windowHeight)
        self.setMaximumWidth(windowWidth)
        self.setMinimumHeight(windowHeight)
        self.setMinimumWidth(windowWidth)

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
        ledSlider = QSlider(Qt.Orientation.Horizontal)
        ledSlider.setMinimum(0)
        ledSlider.setMaximum(255)
        ledSlider.setValue(255)

        ledHLayout = QHBoxLayout()
        ledHLayout.addWidget(ledButton)
        ledHLayout.addWidget(ledSlider)

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
        ledSlider.valueChanged.connect(self.setLedBrightness)
        ledSlider.valueChanged.connect(self.sendLedBrightness)
        leftRotateButton.clicked.connect(lambda x: self.buttonPressed(x,"rl"))
        rightRotateButton.clicked.connect(lambda x: self.buttonPressed(x,"rr"))
        extendShoulderButton.clicked.connect(lambda x: self.buttonPressed(x,"es"))
        retractShoulderButton.clicked.connect(lambda x: self.buttonPressed(x,"rs"))
        extendElbowButton.clicked.connect(lambda x: self.buttonPressed(x,"ee"))
        retractElbowButton.clicked.connect(lambda x: self.buttonPressed(x,"re"))
        extendWristButton.clicked.connect(lambda x: self.buttonPressed(x,"ew"))
        retractWristButton.clicked.connect(lambda x: self.buttonPressed(x,"rw"))
        openClawButton.clicked.connect(lambda x: self.buttonPressed(x,"oc"))
        closeClawButton.clicked.connect(lambda x: self.buttonPressed(x,"cc"))
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
        
    # Create a function to set the LED brightness variable
    def setLedBrightness(self, brightnessValue):
        self.ledBrightness = brightnessValue / 255

    # Create a function to handle if a motor control button is pressed
    def buttonPressed(self,*args):
        print(args)

    # Create a function to handle if the LED control button is pressed
    def ledButtonPressed(self, buttonState):
        if buttonState:
            print("Switching on")
        else:
            print("Switching off")

    # Create a function to send a different brightness value when the LED brightness slider is changed
    def sendLedBrightness(self):
        print(self.ledBrightness)

class CustomQApplication(QApplication):
    def __init__(self,args):
        super().__init__(args)

        pins = Pins()
        configWindow = ConfigWindow(pins=pins)
        mainWindow = MainWindow(configWindow = configWindow, pins="pins")

        self.exec()


if __name__ == "__main__":

    app = CustomQApplication([])

    #app.exec()