from microbit import *
import maqueenPlusV2
import music

# Initialize robot
maqueenPlusV2.i2c_init()
path_memory = []

OBSTACLE_THRESHOLD = 25  # cm
SCAN_ANGLE_LEFT = 45     # degrees left
SCAN_ANGLE_RIGHT = 135   # degrees right
SCAN_ANGLE_CENTER = 90

def startup():
    display.scroll("G3")  # Group number
    maqueenPlusV2.led_all_on()
    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, 90)
    basic.pause(300)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.OPEN)
    basic.pause(500)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.CLOSE)
    music.play(music.BA_DING)

def follow_line_until_node():
    while True:
        left = maqueenPlusV2.read_line_sensor(maqueenPlusV2.MyEnumLineSensor.LEFT_SENSOR)
        right = maqueenPlusV2.read_line_sensor(maqueenPlusV2.MyEnumLineSensor.RIGHT_SENSOR)

        if left and right:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
        elif left:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 20)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
        elif right:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 20)
        else:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
            break

def scan_for_obstacles():
    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_LEFT)
    basic.pause(300)
    left_dist = maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)

    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_RIGHT)
    basic.pause(300)
    right_dist = maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)

    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_CENTER)

    if left_dist > OBSTACLE_THRESHOLD:
        return 'L'
    elif right_dist > OBSTACLE_THRESHOLD:
        return 'R'
    else:
        return 'NONE'

def turn_and_log(direction):
    timestamp = running_time()
    path_memory.append((timestamp, direction))

    if direction == 'L':
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, -30)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 30)
    elif direction == 'R':
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 30)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, -30)
    basic.pause(600)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    music.play(music.POWER_UP)

def deliver_package():
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.OPEN)
    # Rainbow simulation skipped — adjust if your library supports RGB
    music.play(music.JUMP_UP)

def reverse_path():
    for _, dir in reversed(path_memory):
        if dir == 'L':
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 30)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, -30)
        elif dir == 'R':
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, -30)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 30)
        basic.pause(600)
        follow_line_until_node()

def pickup_package2():
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
    basic.pause(1000)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.CLOSE)
    music.play(music.BA_DING)

def shutdown():
    follow_line_until_node()
    deliver_package()
    maqueenPlusV2.led_all_off()
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)

# === Main Mission Start ===
startup()
follow_line_until_node()

for _ in range(3):
    direction = scan_for_obstacles()
    if direction == 'NONE':
        break
    turn_and_log(direction)
    follow_line_until_node()

deliver_package()
reverse_path()
pickup_package2()
reverse_path()
shutdown()
