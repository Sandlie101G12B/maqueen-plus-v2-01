from microbit import *
import maqueenPlusV2
import music

# Initialize
maqueenPlusV2.i2c_init()
path_memory = []

# Constants
OBSTACLE_THRESHOLD = 25
SCAN_ANGLE_LEFT = 45
SCAN_ANGLE_RIGHT = 135
SCAN_ANGLE_CENTER = 90

def startup():
    display.scroll("G3")
    maqueenPlusV2.led_all_on()
    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_CENTER)
    sleep(300)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.OPEN)
    sleep(500)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.CLOSE)
    music.play(music.BA_DING)

def follow_line_until_node():
    start_time = running_time()
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
    end_time = running_time()
    return end_time - start_time

def scan_for_obstacles():
    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_LEFT)
    sleep(300)
    left_dist = maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)

    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_RIGHT)
    sleep(300)
    right_dist = maqueenPlusV2.read_ultrasonic(DigitalPin.P13, DigitalPin.P14)

    maqueenPlusV2.control_servo(maqueenPlusV2.MyEnumServo.S1, SCAN_ANGLE_CENTER)

    if left_dist > OBSTACLE_THRESHOLD:
        return 'L'
    elif right_dist > OBSTACLE_THRESHOLD:
        return 'R'
    else:
        return 'NONE'

def turn_and_log(direction, move_time):
    timestamp = running_time()
    path_memory.append((timestamp, direction, move_time))

    if direction == 'L':
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, -30)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 30)
    elif direction == 'R':
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 30)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, -30)

    sleep(600)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    music.play(music.POWER_UP)

def deliver_package():
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.OPEN)
    music.play(music.JUMP_UP)

def replay_path(reverse=True):
    sequence = list(reversed(path_memory)) if reverse else path_memory

    for i in range(len(sequence)):
        _, direction, move_time = sequence[i]

        if reverse:
            direction = 'L' if direction == 'R' else 'R'

        if direction == 'L':
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, -30)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 30)
        elif direction == 'R':
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 30)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, -30)

        sleep(600)

        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
        sleep(move_time)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)

def pickup_package2():
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 50)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 50)
    sleep(1000)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)
    maqueenPlusV2.control_gripper(maqueenPlusV2.MyEnumServo.GRIPPER, maqueenPlusV2.MyEnumOpenClose.CLOSE)
    music.play(music.BA_DING)

def shutdown():
    deliver_package()
    maqueenPlusV2.led_all_off()
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, 0)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, 0)

# === Main Mission ===
startup()
move_time = follow_line_until_node()

for _ in range(3):
    direction = scan_for_obstacles()
    if direction == 'NONE':
        break
    turn_and_log(direction, move_time)
    move_time = follow_line_until_node()

deliver_package()
replay_path(reverse=True)
pickup_package2()
replay_path(reverse=False)
shutdown()
