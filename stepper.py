import gpiod
import time

# Define the control pins
ControlPin = [14, 15, 18, 23]

# Define the segment patterns
SEG_RIGHT = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

SEG_LEFT = [
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1]
]

DELAY = 0.001  # Control the speed with this delay value


def setup_gpio():
    chip = gpiod.Chip('gpiochip4')
    lines = [chip.get_line(pin) for pin in ControlPin]
    for line in lines:
        line.request(consumer="stepper_motor", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    return chip, lines


def power_down_gpio(lines):
    for line in lines:
        line.set_value(0)
    time.sleep(0.01)  # Small delay to ensure the command is registered


def release_gpio(chip, lines):
    power_down_gpio(lines)
    for line in lines:
        line.release()
    chip.close()


def run_stepper_motor(lines, segments, steps, delay):
    for _ in range(steps):
        for halfstep in range(8):
            for pin in range(4):
                lines[pin].set_value(segments[halfstep][pin])
            time.sleep(delay)


def rotate_motor(angle):
    steps_per_rev = 512  # Adjust this based on the motor specification
    steps = int((abs(angle) / 360.0) * steps_per_rev)
    chip, lines = setup_gpio()

    try:
        if angle > 0:
            run_stepper_motor(lines, SEG_RIGHT, steps, DELAY)
        elif angle < 0:
            run_stepper_motor(lines, SEG_LEFT, steps, DELAY)
    finally:
        release_gpio(chip, lines)
