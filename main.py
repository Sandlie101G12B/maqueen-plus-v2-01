from microbit import display, sleep, running_time
import maqueen

# Constants
OBSTACLE_THRESHOLD = 25
SCAN_ANGLE_LEFT = 45
SCAN_ANGLE_RIGHT = 135
SCAN_ANGLE_CENTER = 90
LEFT = 0
RIGHT = 1
BOTH = 2  # For headlights logic
ON = 1
OFF = 0

path_memory = []


def headlights(select, state):
    if select == LEFT:
        maqueen.write_led(LEFT, state)
    elif select == RIGHT:
        maqueen.write_led(RIGHT, state)
    else:
        maqueen.write_led(LEFT, state)
        maqueen.write_led(RIGHT, state)

def set_servo_angle(servo, angle):
    maqueen.servo_run(servo, angle)

def stop():
    maqueen.motor_stop(maqueen.Motors.ALL)

def drive(speed_left, speed_right=None):
    if speed_right is None:
        speed_right = speed_left
    maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, speed_left)
    maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, speed_right)

def spin_left(speed):
    maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CCW, speed)
    maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, speed)

def spin_right(speed):
    maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, speed)
    maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CCW, speed)



def read_line_sensor(sensor):
    return maqueen.read_patrol(sensor)

def rangefinder():
    return maqueen.ultrasonic()

def startup():
    display.scroll("Group 38")
    headlights(BOTH, ON)
    set_servo_angle(maqueen.Servos.S1, SCAN_ANGLE_CENTER)
    set_servo_angle(maqueen.Servos.S2, 0)  # Open gripper
    set_servo_angle(maqueen.Servos.S2, 90)  # Close gripper
    display.clear()

def follow_line_until_node():
    start_time = running_time()
    while True:
        left = read_line_sensor(maqueen.PatrolSensors.L1)
        right = read_line_sensor(maqueen.PatrolSensors.R1)
        if left and right:
            drive(50, 50)
        elif left:
            drive(20, 50)
        elif right:
            drive(50, 20)
        else:
            stop()
            break
    end_time = running_time()
    return end_time - start_time

def scan_for_obstacles():
    set_servo_angle(maqueen.Servos.S1, SCAN_ANGLE_LEFT)
    left_dist = rangefinder()
    set_servo_angle(maqueen.Servos.S1, SCAN_ANGLE_RIGHT)
    right_dist = rangefinder()
    set_servo_angle(maqueen.Servos.S1, SCAN_ANGLE_CENTER)
    if left_dist > OBSTACLE_THRESHOLD:
        return 'L'
    elif right_dist > OBSTACLE_THRESHOLD:
        return 'R'
    else:
        return 'NONE'

def turn_and_log(direction, move_time):
    path_memory.append((direction, move_time))
    if direction == 'L':
        spin_left(50)
        stop()
    elif direction == 'R':
        spin_right(50)
        stop()

def deliver_package():
    stop()
    set_servo_angle(maqueen.Servos.S2, 0)  # Open gripper

def replay_path(reverse=True):
    sequence = list(reversed(path_memory)) if reverse else path_memory
    for direction, move_time in sequence:
        if reverse:
            direction = 'L' if direction == 'R' else 'R'
        if direction == 'L':
            spin_left(50)
            stop()
        elif direction == 'R':
            spin_right(50)
            stop()
        drive(50, 50)
        stop()

def pickup_package2():
    drive(50, 50)
    stop()
    set_servo_angle(maqueen.Servos.S2, 90)  # Close gripper

def shutdown():
    deliver_package()
    headlights(BOTH, OFF)
    stop()

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