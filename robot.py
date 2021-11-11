#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.buttons import JoystickButton

import ctre


class MyRobot(wpilib.TimedRobot):
    def init(self):
        # Enable safety
        self.myRobot.setSafetyEnabled(False)

        # Start the compressor running in closed loop control mode
        self.compressor.start()

    def periodic(self):
        if not self.directionToggleButton.get():
            self.directionActed = False
        if not self.toggleHatchButton.get():
            self.hatchActed = False
        if not self.toggleBasketButton.get():
            self.basketActed = False

        # If rightButton2 is pressed; change the direction to forward
        if self.directionToggleButton.get() and not self.directionActed:
            self.directionActed = True

            self.direction = -self.direction

        # Tank drive with left and right sticks' Y axis
        if self.speedUpButton.get():
            # Use full axis value for full speed
            self.myRobot.tankDrive(self.gamepad.getRawAxis(1) * self.direction,
                                   self.gamepad.getRawAxis(5) * self.direction)

        else:
            # Use half of the axis value for decreased speed
            self.myRobot.tankDrive(self.gamepad.getRawAxis(1) * self.direction * 0.5,
                                   self.gamepad.getRawAxis(5) * self.direction * 0.5)

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

        # If pushHatchButton is pressed and retractHatchButton is not; push the hatch
        if self.toggleHatchButton.get() and not self.hatchActed:
            self.hatchActed = True

            if self.hatchSolenoid.get() == wpilib.DoubleSolenoid.Value.kForward:
                self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
            else:
                self.hatchSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        # If pushBasketButton is pressed and retractBasketButton is not; push the basket
        if self.toggleBasketButton.get() and not self.basketActed:
            self.basketActed = True

            if self.basketSolenoid.get() == wpilib.DoubleSolenoid.Value.kForward:
                self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
            else:
                self.basketSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

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
        # Controller mapping (1-10): East, South, North, West, Right Bumper, Left Bumper, ?, ?, ?, ?
        self.toggleHatchButton = JoystickButton(self.gamepad, 1)
        self.toggleBasketButton = JoystickButton(self.gamepad, 2)
        self.directionToggleButton = JoystickButton(self.gamepad, 3)
        self.speedUpButton = JoystickButton(self.gamepad, 4)
        self.raiseBasketButton = JoystickButton(self.gamepad, 5)
        self.lowerBasketButton = JoystickButton(self.gamepad, 6)

        # Determine if already acted on
        self.hatchActed = False
        self.basketActed = False
        self.directionActed = False

        # Solenoids
        self.hatchSolenoid = wpilib.DoubleSolenoid(0, 1)
        self.basketSolenoid = wpilib.DoubleSolenoid(2, 3)

        # Compressor
        self.compressor = wpilib.Compressor(0)

        # Camera Server
        wpilib.CameraServer.launch()

    def autonomousInit(self):
        # Executed at the start of autonomous mode
        self.init()

    def autonomousPeriodic(self):
        # Autonomous Mode(Sandstorm = Identical to TeleOp)
        self.periodic()

    def teleopInit(self):
        # Executed at the start of teleop mode
        self.init()

    def teleopPeriodic(self):
        # TeleOperated mode
        self.periodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)
