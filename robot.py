#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.buttons import JoystickButton
from wpilib.robotcontroller import RobotController

import ctre

import networktables
from networktables import NetworkTables
from networktables import NetworkTablesInstance

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        # Robot initialization function

        # VictorSPX = Motor Controllers
        self.frontLeftMotor = ctre.WPI_VictorSPX(0)
        self.rearLeftMotor = ctre.WPI_VictorSPX(1)

        self.frontRightMotor = ctre.WPI_VictorSPX(4)
        self.rearRightMotor = ctre.WPI_VictorSPX(5)

        self.basketMotor = ctre.WPI_VictorSPX(3)
        
        # digital inputs
        self.basketLimitSwitch = wpilib.DigitalInput(0)

        # motor controller groups for each side of robot
        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        # differential drive with left and right motor controller groups
        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # joysticks
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.gamepad = wpilib.Joystick(2)

        # joystick buttons
        self.leftButton1 = JoystickButton(self.leftStick, 1)
        self.rightButton1 = JoystickButton(self.rightStick, 1)

        self.gameButton1 = JoystickButton(self.gamepad, 1)
        self.gameButton2 = JoystickButton(self.gamepad, 2)
        self.gameButton5 = JoystickButton(self.gamepad, 5)
        self.gameButton6 = JoystickButton(self.gamepad, 6)
        self.gameButton7 = JoystickButton(self.gamepad, 7)
        self.gameButton8 = JoystickButton(self.gamepad, 8)

        # solenoid
        self.squeezer = wpilib.DoubleSolenoid(0,1)

        # compressor
        self.compressor = wpilib.Compressor(0)

        # camera
        wpilib.CameraServer.launch()

        # networktables
        NetworkTables.initialize(server='10.74.56.2')
        self.SmartDashboard = NetworkTables.getTable('SmartDashboard')
        self.table = NetworkTables.getTable('Robot')

        x = 0

    def robotPeriodic(self):
        # Runs with every robot package, no matter the mode

        # post voltage value to the networktables
        self.SmartDashboard.putNumber('voltage', RobotController.getBatteryVoltage())

    def autonomousInit(self):
        # Executed at the start of autonomous mode
        
        self.myRobot.setSafetyEnabled(False)

        # start the compressor running in closed loop control mode
        self.compressor.start()

        # Put Auto value with mode key into networktables
        self.table.putString('mode', 'Auto')

    def autonomousPeriodic(self):
        # Autonomous Mode(Sandstorm = identical to TeleOp)

        # tank drive with left and right sticks' Y axis
        if self.leftButton1.get() or self.rightButton1.get():
            self.myRobot.tankDrive(self.leftStick.getY() * -1, self.rightStick.getY() * -1)

        else:
            self.myRobot.tankDrive(self.leftStick.getY() * -1 * 0.5, self.rightStick.getY() * -1 * 0.5)

        # if gameButton5 is pressed; lower basket
        if self.gameButton5.get() and not self.gameButton6.get():
            if not self.basketLimitSwitch.get():
                self.basketMotor.set(-1)
            else:
                self.basketMotor.set(0)
        
        # if gameButton5 is pressed; raise basket
        elif self.gameButton6.get() and not self.gameButton5.get():
            self.basketMotor.set(1)

        # else, leave the basket still
        else:
            self.basketMotor.set(0)

        # if gameButton1 is pressed and gameButton2 is not pressed; turn solenoid forward
        if self.gameButton1.get() and not(self.gameButton2.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kForward)

        # if gameButton2 is pressed and gameButton1 is not pressed; turn solenoid reverse
        elif self.gameButton2.get() and not(self.gameButton1.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kReverse)

    def teleopInit(self):
        # Executed at the start of teleop mode
        
        self.myRobot.setSafetyEnabled(False)

        # start the compressor running in closed loop control mode
        self.compressor.start()

        # Put TeleOp value with mode key into networktables
        self.table.putString('mode', 'TeleOp')

        x = 0

    def teleopPeriodic(self):
        # TeleOperated mode

        # tank drive with left and right sticks' Y axis
        if self.leftButton1.get() or self.rightButton1.get():
            self.myRobot.tankDrive(self.leftStick.getY() * -1, self.rightStick.getY() * -1)

        else:
            self.myRobot.tankDrive(self.leftStick.getY() * -1 * 0.5, self.rightStick.getY() * -1 * 0.5)

        # lower the basket
        if self.gameButton5.get() and not self.gameButton6.get():

            # limit switch
            if not self.basketLimitSwitch.get():
                self.basketMotor.set(-1)
            else:
                self.basketMotor.set(0)

        # raise the basket
        elif self.gameButton6.get() and not self.gameButton5.get():

            self.basketMotor.set(1)

        else:

            self.basketMotor.set(0)
        
        # if gameButton1 is pressed and gameButton2 is not pressed; turn solenoid forward
        if self.gameButton1.get() and not(self.gameButton2.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kForward)

        # if gameButton2 is pressed and gameButton1 is not pressed; turn solenoid reverse
        elif self.gameButton2.get() and not(self.gameButton1.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kReverse)


    def disabledInit(self):
        # Disabled mode

        self.squeezer.set(wpilib.DoubleSolenoid.Value.kOff)

if __name__ == "__main__":
    wpilib.run(MyRobot)