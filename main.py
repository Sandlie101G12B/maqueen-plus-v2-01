from microbit import *
import neopixel

i2c = globals()['i2c']
pin13 = globals()['pin13']
pin14 = globals()['pin14']
pin15 = globals()['pin15']
display = globals()['display']
NeoPixel = neopixel.NeoPixel
running_time = globals()['running_time']

neo_pixel = NeoPixel(pin15, 4)

def pause(ms):
    # Use microbit's built-in sleep for MakeCode
    from microbit import sleep
    sleep(ms)

# Assign MakeCode-compatible hardware symbols
# (In MakeCode Python, these are available by default)
# Remove all fallback assignments and use direct references

# Constants
I2C_ADDR = 0x10
VERSION_COUNT_I2C_ADDR = 0x32
VERSION_DATA_I2C_ADDR = 0x33

LEFT_MOTOR_I2C_ADDR = 0x00
AXLE_WIDTH = 0.095
FORWARD = 0
BACKWARD = 1

# Ultrasonic Rangefinder
US_TRIGGER = pin13
US_ECHO = pin14
MIN_DISTANCE = 2
MAX_DISTANCE = 450
MAX_DURATION = 38000
SPEED_OF_SOUND = 343.4 * 100 / 1000000  # cm/us

# NeoPixel
NEO_PIXEL_PIN = pin15
neo_pixel = neopixel.NeoPixel(NEO_PIXEL_PIN, 4)

# MakeCode Python compatibility layer
# Remove unsupported imports and fallback logic for MakeCode
# Use MakeCode's APIs and idioms

# i2c bus location on the micro:bit.
# NAME_I2C_ADDR are adresses for robot components on the i2c bus.
I2C_ADDR = 0x10

# robot version length and location
VERSION_COUNT_I2C_ADDR = 0x32
VERSION_DATA_I2C_ADDR = 0x33

# Motor constants
LEFT_MOTOR_I2C_ADDR = 0x00
# RIGHT_MOTOR_I2C_ADDR = 0x02 not used. I always set both.

AXLE_WIDTH = 0.095

FORWARD = 0
BACKWARD = 1

# IR sensor constants for version 2.1
LINE_SENSOR_I2C_ADDR = 0x1D
ANALOG_L2_I2C_ADDR = 0x26
ANALOG_L1_I2C_ADDR = 0x24
ANALOG_M_I2C_ADDR = 0x22
ANALOG_R1_I2C_ADDR = 0x20
ANALOG_R2_I2C_ADDR = 0x1E

ALL_ANALOG_SENSOR_I2C_ADDRS = [
    ANALOG_L2_I2C_ADDR,
    ANALOG_L1_I2C_ADDR,
    ANALOG_M_I2C_ADDR,
    ANALOG_R1_I2C_ADDR,
    ANALOG_R2_I2C_ADDR,
]

sensor_index = [4, 3, 2, 1, 0]

L2 = 0
L1 = 1
M = 2
R1 = 3
R2 = 4

DIGITAL_SENSOR_STATUS_I2C_ADDR = 0x1D
DIGITAL_SENSOR_MASK = [16, 8, 4, 2, 1]
DIGITAL_SENSOR_SHIFT = [4, 3, 2, 1, 0]

# Ultrasonic Rangefinder constants
US_TRIGGER = pin13
US_ECHO = pin14
MIN_DISTANCE = 2  # centimeters
MAX_DISTANCE = 450  # centimeters
MAX_DURATION = 38000  # microseconds
SPEED_OF_SOUND = 343.4 * 100 / 1000000  # centemeters/microsecond

# LED nts
LEFT_LED_I2C_ADDR = 0x0B
RIGHT_LED_I2C_ADDR = 0x0C
LEFT = 0
RIGHT = 1
BOTH = 2
ON = 1
OFF = 0

# Servos
SERVO_1 = 0x14
SERVO_2 = 0x15
SERVO_3 = 0x16

# NeoPixel tnts
NEO_PIXEL_PIN = pin15
RED = 0xFF0000
ORANGE = 0xFFA500
YELLOW = 0xFFFF00
GREEN = 0x00FF00
BLUE = 0x0000FF
INDIGO = 0x4B0082
VIOLET = 0x8A2BE2
PURPLE = 0xFF00FF
WHITE = 0xFF9070
# OFF = const(0x000000) use the other OFF zero is zero


# General purpose functions
def init_maqueen():
    global sensor_index
    version = maqueen_version()
    if version[-3:] == "2.0":
        sensor_index = [0, 1, 2, 3, 4]
    elif version[-3:] == "2.1":
        sensor_index = [4, 3, 2, 1, 0]
    pause(1000)
    display.clear()


def eight_bits(n):
    return max(min(n, 255), 0)


def one_bit(n):
    return max(min(n, 1), 0)


def maqueen_version():
    "Return the Maqueen board version as a string. The last 3 characters are the version."
    i2c.write(I2C_ADDR, bytes([VERSION_COUNT_I2C_ADDR]))
    count = int.from_bytes(i2c.read(I2C_ADDR, 1), "big")
    i2c.write(I2C_ADDR, bytes([VERSION_DATA_I2C_ADDR]))
    version = i2c.read(I2C_ADDR, count).decode("ascii")
    return version


def color_to_rgb(color):
    r = color >> 16
    g = color >> 8 & 0xFF
    b = color & 0xFF
    return r, g, b


# Motor functions
def stop():
    "Stop the robot's motors"
    drive(0)


def drive(speed_left, speed_right=None):
    "Drive forward at speed 0-255"
    if speed_right == None: speed_right = speed_left
    motors(speed_left, FORWARD, speed_right, FORWARD)


def backup(speed_left, speed_right=None):
    "Drive backwards at speed 0-255"
    if speed_right == None: speed_right = speed_left
    motors(speed_left, BACKWARD, speed_right, BACKWARD)


def spin_left(speed):
    "Spin the robot left at speed 0-255"
    motors(speed, BACKWARD, speed, FORWARD)


def spin_right(speed):
    "Spin the robot right at speed 0-255"
    motors(speed, FORWARD, speed, BACKWARD)


def motors(l_speed, l_direction, r_speed, r_direction):
    "Set both motor speeds 0-255 and directions (FORWARD, BACKWARD) left then right."
    buf = bytearray(5)
    buf[0] = LEFT_MOTOR_I2C_ADDR
    buf[1] = one_bit(l_direction)
    buf[2] = eight_bits(round(l_speed))
    buf[3] = one_bit(r_direction)
    buf[4] = eight_bits(round(r_speed))
    i2c.write(I2C_ADDR, buf)


# IR line sensor functions
def read_all_line_sensors():
    "Return an array of line sensor readings. Left to right."
    values = []
    for index in sensor_index:
        i2c.write(I2C_ADDR, bytes([ALL_ANALOG_SENSOR_I2C_ADDRS[index]]))
        buffer = i2c.read(I2C_ADDR, 2)
        values.append(buffer[1] << 8 | buffer[0])
    return values


def read_line_sensor(sensor):
    "Return a line sensor reading. On a line is about 240. Off line is about 70."
    i2c.write(I2C_ADDR, bytes([ALL_ANALOG_SENSOR_I2C_ADDRS[sensor_index[sensor]]]))
    buffer = i2c.read(I2C_ADDR, 2)
    return buffer[1] << 8 | buffer[0]


def sensor_on_line(sensor):
    "Return True if the line sensor sees a line."
    i2c.write(I2C_ADDR, bytes([DIGITAL_SENSOR_STATUS_I2C_ADDR]))
    sensor_state = int.from_bytes(i2c.read(I2C_ADDR, 1), "big")
    return (sensor_state & DIGITAL_SENSOR_MASK[sensor]) >> DIGITAL_SENSOR_SHIFT[
        sensor
    ] == 1

# LED head light functions
def headlights(select, state):
    "Turn LEFT, RIGHT, or BOTH headlights to ON or OFF."
    if select == LEFT:
        i2c.write(I2C_ADDR, bytearray([LEFT_LED_I2C_ADDR, state]))
    elif select == RIGHT:
        i2c.write(I2C_ADDR, bytearray([RIGHT_LED_I2C_ADDR, state]))
    else:
        i2c.write(I2C_ADDR, bytearray([LEFT_LED_I2C_ADDR, state, state]))


# Underglow lighting functions
neo_pixel = NeoPixel(pin15, 4)

def underglow_off():
    set_underglow(OFF)


def set_underglow_light(light, color):
    neo_pixel[light] = color_to_rgb(color)
    neo_pixel.show()

def set_servo_angle(servo, angle):
    angle = max(min(angle, 180), 0)
    i2c.write(I2C_ADDR, bytes([servo, angle]))

def set_underglow(color):
    rgb = color_to_rgb(color)
    for i in range(4):
        neo_pixel[i] = rgb
    neo_pixel.show()
#---------------------------------------------------------------------------------------



# Initialize
init_maqueen()

path_memory = []

# Constants
OBSTACLE_THRESHOLD = 25
SCAN_ANGLE_LEFT = 45
SCAN_ANGLE_RIGHT = 135
SCAN_ANGLE_CENTER = 90


def startup():
    display.scroll("Group 38")
    headlights(BOTH, ON)
    set_servo_angle(SERVO_1, SCAN_ANGLE_CENTER)
    # Simulate gripper open/close with servo if needed
    set_servo_angle(SERVO_2, 0)  # Open
    set_servo_angle(SERVO_2, 90)  # Close
    # Optionally play a sound here
    display.clear()


def follow_line_until_node():
    start_time = running_time()
    while True:
        left = read_line_sensor(L1)
        right = read_line_sensor(R1)
        if left > 150 and right > 150:
            drive(50, 50)
        elif left > 150:
            drive(20, 50)
        elif right > 150:
            drive(50, 20)
        else:
            stop()
            break
    end_time = running_time()
    return end_time - start_time


def scan_for_obstacles():
    set_servo_angle(SERVO_1, SCAN_ANGLE_LEFT)
    left_dist = 0
    set_servo_angle(SERVO_1, SCAN_ANGLE_RIGHT)
    right_dist = 0
    set_servo_angle(SERVO_1, SCAN_ANGLE_CENTER)
    if left_dist > OBSTACLE_THRESHOLD:
        return 'L'
    elif right_dist > OBSTACLE_THRESHOLD:
        return 'R'
    else:
        return 'NONE'


def turn_and_log(direction, move_time):
    # timestamp = running_time()
    path_memory.append((direction, move_time))
    if direction == 'L':
        spin_left(50)
        stop()
    elif direction == 'R':
        spin_right(50)
        stop()
    # Optionally play a sound here


def deliver_package():
    stop()
    set_servo_angle(SERVO_2, 0)  # Open gripper
    # Optionally play a sound here


def replay_path(reverse=True):
    sequence = list(reversed(path_memory)) if reverse else path_memory
    for _, direction, move_time in sequence:
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
    set_servo_angle(SERVO_2, 90)  # Close gripper
    # Optionally play a sound here


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
