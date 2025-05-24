from microbit import *
import maqueenPlusV2
import music

# === Init robot shortcut ===
robot = maqueenPlusV2
robot.i2c_init()
path_memory = []

# === Constants ===
OBSTACLE_THRESHOLD = 25  # cm
SCAN_ANGLE_LEFT = 45
SCAN_ANGLE_RIGHT = 135
SCAN_ANGLE_CENTER = 90

# === Enums ===
S1 = robot.MyEnumServo.S1
GRIPPER = robot.MyEnumServo.GRIPPER

LEFT_MOTOR = robot.MyEnumMotor.LEFT_MOTOR
RIGHT_MOTOR = robot.MyEnumMotor.RIGHT_MOTOR

OPEN = robot.MyEnumOpenClose.OPEN
CLOSE = robot.MyEnumOpenClose.CLOSE

LEFT_SENSOR = robot.MyEnumLineSensor.LEFT_SENSOR
RIGHT_SENSOR = robot.MyEnumLineSensor.RIGHT_SENSOR

# === Functions ===

def startup():
    display.scroll("G3")
    robot.led_all_on()
    robot.control_servo(S1, SCAN_ANGLE_CENTER)
    sleep(300)
    robot.control_gripper(GRIPPER, OPEN)
    sleep(500)
    robot.control_gripper(GRIPPER, CLOSE)
    music.play(music.BA_DING)

def follow_line_until_node():
    while True:
        left = robot.read_line_sensor(LEFT_SENSOR)
        right = robot.read_line_sensor(RIGHT_SENSOR)

        if left and right:
            robot.control_motor(LEFT_MOTOR, 50)
            robot.control_motor(RIGHT_MOTOR, 50)
        elif left:
            robot.control_motor(LEFT_MOTOR, 20)
            robot.control_motor(RIGHT_MOTOR, 50)
        elif right:
            robot.control_motor(LEFT_MOTOR, 50)
            robot.control_motor(RIGHT_MOTOR, 20)
        else:
            robot.control_motor(LEFT_MOTOR, 0)
            robot.control_motor(RIGHT_MOTOR, 0)
            break

def scan_for_obstacles():
    robot.control_servo(S1, SCAN_ANGLE_LEFT)
    sleep(300)
    left_dist = robot.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)

    robot.control_servo(S1, SCAN_ANGLE_RIGHT)
    sleep(300)
    right_dist = robot.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)

    robot.control_servo(S1, SCAN_ANGLE_CENTER)

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
        robot.control_motor(LEFT_MOTOR, -30)
        robot.control_motor(RIGHT_MOTOR, 30)
    elif direction == 'R':
        robot.control_motor(LEFT_MOTOR, 30)
        robot.control_motor(RIGHT_MOTOR, -30)
    
    sleep(600)
    robot.control_motor(LEFT_MOTOR, 0)
    robot.control_motor(RIGHT_MOTOR, 0)
    music.play(music.POWER_UP)

def deliver_package():
    robot.control_motor(LEFT_MOTOR, 0)
    robot.control_motor(RIGHT_MOTOR, 0)
    robot.control_gripper(GRIPPER, OPEN)
    music.play(music.JUMP_UP)

def reverse_path():
    for _, dir in reversed(path_memory):
        if dir == 'L':
            robot.control_motor(LEFT_MOTOR, 30)
            robot.control_motor(RIGHT_MOTOR, -30)
        elif dir == 'R':
            robot.control_motor(LEFT_MOTOR, -30)
            robot.control_motor(RIGHT_MOTOR, 30)
        sleep(600)
        follow_line_until_node()

def pickup_package2():
    robot.control_motor(LEFT_MOTOR, 50)
    robot.control_motor(RIGHT_MOTOR, 50)
    sleep(1000)
    robot.control_motor(LEFT_MOTOR, 0)
    robot.control_motor(RIGHT_MOTOR, 0)
    robot.control_gripper(GRIPPER, CLOSE)
    music.play(music.BA_DING)

def shutdown():
    follow_line_until_node()
    deliver_package()
    robot.led_all_off()
    robot.control_motor(LEFT_MOTOR, 0)
    robot.control_motor(RIGHT_MOTOR, 0)

# === Main Mission ===
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
