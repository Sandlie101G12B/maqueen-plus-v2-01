let distance = 0
maqueenPlusV2.I2CInit()
basic.forever(function on_forever() {
    
    distance = maqueenPlusV2.readUltrasonic(DigitalPin.P13, DigitalPin.P14)
    if (distance < 30 && distance != 0) {
        maqueenPlusV2.controlMotor(maqueenPlusV2.MyEnumMotor.LeftMotor, maqueenPlusV2.MyEnumDir.Forward, 50)
        maqueenPlusV2.controlMotor(maqueenPlusV2.MyEnumMotor.RightMotor, maqueenPlusV2.MyEnumDir.Forward, 0)
        basic.pause(1000)
    } else {
        maqueenPlusV2.controlMotor(maqueenPlusV2.MyEnumMotor.AllMotor, maqueenPlusV2.MyEnumDir.Forward, 50)
    }
    
})
