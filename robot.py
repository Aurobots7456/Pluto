#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.buttons import JoystickButton
from wpilib.robotcontroller import RobotController

import ctre

import networktables
from networktables import NetworkTables
from networktables import NetworkTablesInstance


def init(self):
    # Enable safety
    self.myRobot.setSafetyEnabled(False)

    # Start the compressor running in closed loop control mode
    self.compressor.start()


def periodic(self):
    # If rightButton2 is pressed; change the direction to forward
    if self.directionForwardButton.get() and not(self.directionBackwardButton.get()):
        self.direction = -1

    # If rightButton3 is pressed; change the direction to backward
    elif self.directionBackwardButton.get() and not(self.directionForwardButton.get()):
        self.direction = 1

    # Tank drive with left and right sticks' Y axis
    if self.speedUpButton1.get() or self.speedUpButton2.get():
        # Use full axis value for full speed
        self.myRobot.tankDrive(self.gamepad.getRawAxis(1) * self.direction, self.gamepad.getRawAxis(5) * self.direction)

    else:
        # Use half of the axis value for decreased speed
        self.myRobot.tankDrive(self.gamepad.getRawAxis(1) * self.direction * 0.5, self.gamepad.getRawAxis(5) * self.direction * 0.5)

    # If gameButton5 is pressed; lower the basket
    if self.raiseBasketButton.get() and not self.lowerBasketButton.get():
        if not self.basketLimitSwitch.get():
            # If basketLimitSwitch is triggered stop the basket
            self.basketMotor.set(-1)
        else:
            self.basketMotor.set(0)

    # If gameButton6 is pressed; raise the basket
    elif self.lowerBasketButton.get() and not self.raiseBasketButton.get():
        self.basketMotor.set(1)

    else:
        self.basketMotor.set(0)

    # If pushHatchButton is pressed and gameButton2 is not; push the hatch
    if self.pushHatchButton.get() and not(self.retractHatchButton.get()):
        self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

    # If gameButton2 is pressed and gameButton1 is not; retract the hatch
    elif self.retractHatchButton.get() and not(self.pushHatchButton.get()):
        self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

    # If gameButton3 is pressed and gameButton4 is not; push the basket
    if self.pushBasketButton.get() and not(self.retractBasketButton.get()):
        self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

    # If gameButton4 is pressed and gameButton3 is not; retract the basket
    if self.retractBasketButton.get() and not(self.pushBasketButton.get()):
        self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        # Robot initialization function

        # VictorSPX = Motor Controllers
        self.frontLeftMotor = ctre.WPI_VictorSPX(0)
        self.rearLeftMotor = ctre.WPI_VictorSPX(1)

        self.frontRightMotor = ctre.WPI_VictorSPX(4)
        self.rearRightMotor = ctre.WPI_VictorSPX(5)

        self.basketMotor = ctre.WPI_VictorSPX(3)
        
        # Digital Inputs (Limit Switch)
        self.basketLimitSwitch = wpilib.DigitalInput(0)

        # Motor controller groups for each side of the robot
        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        # Differential drive with left and right motor controller groups
        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        self.direction = -1

        # Declare gamepad
        self.gamepad = wpilib.Joystick(1)

        # Declare buttons
        # Controller mapping (1-10): East, South, North, East, Right Bumper, Left Bumper, ?, ?, ?, ?
        self.pushHatchButton = JoystickButton(self.gamepad, 1)
        self.retractHatchButton = JoystickButton(self.gamepad, 2)
        self.pushBasketButton = JoystickButton(self.gamepad, 3)
        self.retractBasketButton = JoystickButton(self.gamepad, 4)
        self.raiseBasketButton = JoystickButton(self.gamepad, 5)
        self.lowerBasketButton = JoystickButton(self.gamepad, 6)
        self.speedUpButton1 = JoystickButton(self.gamepad, 7)
        self.speedUpButton2 = JoystickButton(self.gamepad, 8)
        self.directionForwardButton = JoystickButton(self.gamepad, 9)
        self.directionBackwardButton = JoystickButton(self.gamepad, 10)

        # Solenoids
        self.hatchSolenoid = wpilib.DoubleSolenoid(0, 1)
        self.basketSolenoid = wpilib.DoubleSolenoid(2, 3)

        # Compressor
        self.compressor = wpilib.Compressor(0)

        # Camera Server
        wpilib.CameraServer.launch()

    def autonomousInit(self):
        # Executed at the start of autonomous mode
        init(self)

    def autonomousPeriodic(self):
        # Autonomous Mode(Sandstorm = Identical to TeleOp)
        periodic(self)

    def teleopInit(self):
        # Executed at the start of teleop mode
        init(self)

    def teleopPeriodic(self):
        # TeleOperated mode
        periodic(self)


if __name__ == "__main__":
    wpilib.run(MyRobot)
