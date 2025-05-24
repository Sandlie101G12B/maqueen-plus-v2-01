let direction: string;
//  Initialize
maqueenPlusV2.I2CInit()

let path_memory = [[], []]
//  Constants
let OBSTACLE_THRESHOLD = 25
let SCAN_ANGLE_LEFT = 45
let SCAN_ANGLE_RIGHT = 135
let SCAN_ANGLE_CENTER = 90

// display.scroll("G3")
// maqueenPlusV2.led_all_on()
// maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_CENTER)
// sleep(300)
// maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.OPEN)
// sleep(500)
// maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.CLOSE)
// music.play(music.BA_DING)
function follow_line_until_node() {
    // start_time = running_time()
    // while True:
    // left = maqueenPlusV2.read_line_sensor(maqueenPlusV2.MyEnumLineSensor.LEFT_SENSOR)
    // right = maqueenPlusV2.read_line_sensor(maqueenPlusV2.MyEnumLineSensor.RIGHT_SENSOR)
    // if left and right:
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
    // elif left:
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 20)
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
    // elif right:
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 20)
    // else:
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    // break
    // end_time = running_time()
    return
}

// end_time - start_time
function scan_for_obstacles(): string {
    // maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_LEFT)
    // sleep(300)
    let left_dist = maqueenPlusV2.readUltrasonic(DigitalPin.P13, DigitalPin.P14)
    // maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_RIGHT)
    // sleep(300)
    let right_dist = maqueenPlusV2.readUltrasonic(DigitalPin.P13, DigitalPin.P14)
    // maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_CENTER)
    if (left_dist > OBSTACLE_THRESHOLD) {
        return "L"
    } else if (right_dist > OBSTACLE_THRESHOLD) {
        return "R"
    } else {
        return "NONE"
    }
    
}

function turn_and_log(direction: string, move_time: any) {
    // timestamp = running_time()
    let timestamp = 5
    path_memory.push([timestamp, direction, move_time])
    if (direction == "L") {
        return
    } else if (direction == "R") {
        // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, -30)
        // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 30)
        return
    }
    
}

// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 30)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, -30)
// sleep(600)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
// music.play(music.POWER_UP)
function deliver_package() {
    return
}

// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
// maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.OPEN)
// music.play(music.JUMP_UP)
function replay_path(reverse: boolean = true) {
    let direction: any;
    // sequence = list(reversed(path_memory)) if reverse else path_memory
    let sequence = [[], []]
    for (let i = 0; i < sequence.length; i++) {
        let [_, direction, move_time] = sequence[i]
        if (reverse) {
            direction = direction == "R" ? "L" : "R"
        }
        
        if (direction == "L") {
            return
        } else if (direction == "R") {
            // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, -30)
            // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 30)
            return
        }
        
    }
}

// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 30)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, -30)
// sleep(600)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
// sleep(move_time)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
function pickup_package2() {
    return
}

// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
// sleep(1000)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
// maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
// maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.CLOSE)
// music.play(music.BA_DING)
function shutdown() {
    deliver_package()
    // maqueenPlusV2.led_all_off()
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    // maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    return
}

//  === Main Mission ===
startup()
let move_time = follow_line_until_node()
for (let _ = 0; _ < 3; _++) {
    direction = scan_for_obstacles()
    if (direction == "NONE") {
        break
    }
    
    turn_and_log(direction, move_time)
    move_time = follow_line_until_node()
}
deliver_package()
replay_path(true)
pickup_package2()
replay_path(false)
shutdown()
