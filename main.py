from microbit import *
import maqueen  # Replace this with your robot library
import music

robot = maqueen.MaqueenPlus()
path_memory = []  # To store turns

# Constants
OBSTACLE_THRESHOLD = 25  # cm
SCAN_ANGLE = 45  # degrees

def startup():
    display.scroll("G3")  # Replace with your group number
    robot.led_all_on()  # Turn on all LEDs
    robot.gripper_open()
    sleep(500)
    robot.gripper_close()  # Grabs Package 1
    music.play(music.BA_DING)

def follow_line_until_node():
    while True:
        left = robot.read_line_sensor('left')
        right = robot.read_line_sensor('right')

        if left and right:
            robot.motor_run(50, 50)  # Forward
            elif left:
                robot.motor_run(20, 50)  # Turn right
                elif right:
                    robot.motor_run(50, 20)  # Turn left
                else:
                    robot.motor_stop()
                    break  # Node reached
                                                                                                                    
def scan_for_obstacles():
    robot.servo_write(1, 90 - SCAN_ANGLE)
    sleep(300)
    left_dist = robot.ultrasonic_read()
                    
    robot.servo_write(1, 90 + SCAN_ANGLE)
    sleep(300)
    right_dist = robot.ultrasonic_read()
                                    
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
        robot.turn_left()
    elif direction == 'R':
        robot.turn_right()
    else:
        robot.motor_stop()
        music.play(music.POWER_UP)

def deliver_package():
    robot.motor_stop()
    robot.gripper_open()
    robot.rgb_led_show("rainbow")  # If supported
    music.play(music.JUMP_UP)

def reverse_path():
    for _, dir in reversed(path_memory):
        if dir == 'L':
            robot.turn_right()
        elif dir == 'R':
            robot.turn_left()
            follow_line_until_node()

def pickup_package2():
    robot.motor_run(50, 50)
    sleep(1000)  # Move toward the wall
    robot.motor_stop()
    robot.gripper_close()
    music.play(music.BA_DING)

def shutdown():
    follow_line_until_node()
    deliver_package()
    robot.led_all_off()
    robot.motor_stop()

startup()
follow_line_until_node()

for _ in range(3):  # Max 3 junctions
    direction = scan_for_obstacles()
    if direction == 'NONE':
        break
    turn_and_log(direction)
    follow_line_until_node()
    deliver_package()
    reverse_path()
    pickup_package2()
    reverse_path()  # Follow the same path again
    shutdown()
