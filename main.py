distance = 0
maqueenPlusV2.i2c_init()

def on_forever():
    global distance
    distance = maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)
    if distance < 30 and distance != 0:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
            maqueenPlusV2.MyEnumDir.FORWARD,
            50)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
            maqueenPlusV2.MyEnumDir.FORWARD,
            0)
        basic.pause(1000)
    else:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR,
            maqueenPlusV2.MyEnumDir.FORWARD,
            50)
basic.forever(on_forever)
