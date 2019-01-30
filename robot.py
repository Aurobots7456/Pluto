#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.buttons import JoystickButton

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
        self.gameButton1 = JoystickButton(self.gamepad, 1)
        self.gameButton2 = JoystickButton(self.gamepad, 2)
        self.gameButton3 = JoystickButton(self.gamepad, 3)
        self.gameButton4 = JoystickButton(self.gamepad, 4)

        # solenoid
        self.squeezer = wpilib.DoubleSolenoid(0,1)

        # servo
        self.servo = wpilib.Servo(0)

        # compressor
        self.compressor = wpilib.Compressor(0)

        # camera
        wpilib.CameraServer.launch()

        """
            # While connected to the internet
            robotpy-installer download-opkg python37-robotpy-cscore

            # While connected to the network with a RoboRIO on it
            robotpy-installer install-opkg python37-robotpy-cscore
        """

        # networktables
        NetworkTables.initialize(server='10.74.56.2')
        self.table = NetworkTables.getTable('Robot')

    def autonomousInit(self):
        # Executed at the start of autonomous mode
        
        self.myRobot.setSafetyEnabled(True)

        # start the compressor running in closed loop control mode
        self.compressor.start()

        # Put Auto value with mode key into networktables
        self.table.putString('mode', 'Auto')

    def autonomousPeriodic(self):
        # Autonomous Mode(Sandstorm = identical to TeleOp)

        # tank drive with left and right sticks' Y axis
        self.myRobot.tankDrive(self.leftStick.getY() * -1, self.rightStick.getY() * -1)

        # if gameButton3 is pressed; set servo's angle to 180
        if self.gameButton3.get():
            self.servo.setAngle(180)

        # if gameButton4 is pressed; set servo's angle to 0
        elif self.gameButton4.get():
            self.servo.setAngle(0)

        # if gameButton1 is pressed and gameButton2 is not pressed; turn solenoid forward
        if self.gameButton1.get() and not(self.gameButton2.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kForward)

        # if gameButton2 is pressed and gameButton1 is not pressed; turn solenoid reverse
        elif self.gameButton2.get() and not(self.gameButton1.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kReverse)

        # if gameButton2 and gameButton1 are not pressed; turn solenoid off
        else:
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kOff)

    def teleopInit(self):
        # Executed at the start of teleop mode
        
        self.myRobot.setSafetyEnabled(True)

        # start the compressor running in closed loop control mode
        self.compressor.start()

        # Put TeleOp value with mode key into networktables
        self.table.putString('mode', 'TeleOp')

    def teleopPeriodic(self):
        # TeleOperated mode

        # tank drive with left and right sticks' Y axis
        self.myRobot.tankDrive(self.leftStick.getY() * -1, self.rightStick.getY() * -1)

        # if gameButton3 is pressed; set servo's angle to 180
        if self.gameButton3.get():
            self.servo.setAngle(180)

        # if gameButton4 is pressed; set servo's angle to 0
        elif self.gameButton4.get():
            self.servo.setAngle(0)

        # if gameButton1 is pressed and gameButton2 is not pressed; turn solenoid forward
        if self.gameButton1.get() and not(self.gameButton2.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kForward)

        # if gameButton2 is pressed and gameButton1 is not pressed; turn solenoid reverse
        elif self.gameButton2.get() and not(self.gameButton1.get()):
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kReverse)

        # if gameButton2 and gameButton1 are not pressed; turn solenoid off
        else:
            self.squeezer.set(wpilib.DoubleSolenoid.Value.kOff)

if __name__ == "__main__":
    wpilib.run(MyRobot)