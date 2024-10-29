import badger2040
import math
import time
import pngdec

WIDTH = 296  # Badger2040 screen width
HEIGHT = 128  # Badger2040 screen height
RUNNING = True
REFRESH_RATE = 2.0
WAVE_AMPLITUDE = 25
WAVE_FREQUENCY = 0.006
WAVE_SPEED = 1.0
WAVE_THICKNESS = 8

# Text constants
LEFT_PADDING = 5
NAME_HEIGHT = 35  # Reduced from 50 to bring last name higher
DETAILS_HEIGHT = 18

# Badge text
FIRST_NAME = "Chris"
LAST_NAME = "Lloyd-Jones"
JOB_TITLE = "Architecture & Strategy"

def draw_logo():
    try:
        png.open_file("/badges/avaBwSolid64.png")
        # Position the 64x64 logo in the top right
        png.decode(WIDTH - 64 - 5, 5)  # 5px padding from top and right edges
    except OSError:
        print("Could not load logo image")

def draw_name():
    # Draw the firstname
    badger.set_font("sans")
    badger.set_thickness(4)

    # Calculate appropriate text size for first name
    name_size = 1.2  # Starting size
    while True:
        name_length = badger.measure_text(FIRST_NAME, name_size)
        if name_length >= WIDTH/2 and name_size >= 0.1:
            name_size -= 0.01
        else:
            badger.text(FIRST_NAME, int(LEFT_PADDING), 15, int(WIDTH/2), name_size)
            break

    # Draw the lastname
    lastname_size = 0.9
    badger.text(LAST_NAME, int(LEFT_PADDING), int(NAME_HEIGHT), int(WIDTH/2), lastname_size)

    # Draw the job title
    badger.set_font("sans")
    badger.set_thickness(2)
    badger.text(JOB_TITLE, int(LEFT_PADDING), HEIGHT - 9, int(WIDTH/2), 0.55)
    
    # Write Avanade in tiny text
    badger.set_thickness(2)
    badger.text("Avanade",int(LEFT_PADDING),HEIGHT-23,4,0.45)

def draw_sine_wave(offset, amplitude, vertical_offset, thickness=WAVE_THICKNESS):
    points = []
    for x in range(0, WIDTH, 2):
        # More dramatic progression from smooth to dynamic
        progress = x / WIDTH

        # Add downward slope
        slope = progress * 50  # Determines how much the waves angle down

        # Cubic increase for more dramatic right side
        freq_mod = WAVE_FREQUENCY * (1.0 + (2.5 * progress * progress * progress))
        # Quadratic amplitude increase
        amp_mod = amplitude * (0.7 + (0.8 * progress * progress))

        # Add slope to y-position
        y = int(math.sin((x * freq_mod) + offset) * amp_mod) + vertical_offset + int(slope)
        points.append((x, y))

    # Draw the wave with the specified thickness
    for i in range(thickness):
        offset_points = [(x, y + i) for x, y in points]
        for j in range(len(offset_points) - 1):
            x1, y1 = offset_points[j]
            x2, y2 = offset_points[j + 1]
            badger.line(x1, y1, x2, y2)

def draw_waves(time_offset):
    badger.set_pen(15)  # White background
    badger.clear()

    # Draw logo first (in background)
    draw_logo()

    # Start waves lower on left and angle down
    base_height = HEIGHT * 1//2  # Start position for waves

    # Draw waves closer together on the left
    badger.set_pen(0)
    draw_sine_wave(time_offset, WAVE_AMPLITUDE, base_height - 15)

    # Smaller vertical offset between waves at start
    badger.set_pen(0)
    draw_sine_wave(time_offset + math.pi/1.1, WAVE_AMPLITUDE, base_height + 5)

    # Draw name on top
    badger.set_pen(0)
    draw_name()

    badger.update()

def write_text(text):
    badger.set_pen(15)
    badger.clear()
    badger.set_pen(0)
    badger.set_font("bitmap8")
    badger.set_thickness(1)
    badger.text(text, 25, 25)
    badger.update()
    time.sleep(1)

# ----------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------
badger = badger2040.Badger2040()
badger.set_update_speed(1)
png = pngdec.PNG(badger.display)
time_offset = 0

while True:
    if badger.pressed(badger2040.BUTTON_B):
        RUNNING = not RUNNING
        write_text('Running: ' + str(RUNNING))

    if badger.pressed(badger2040.BUTTON_UP):
        if REFRESH_RATE - 0.5 > 0:
            REFRESH_RATE -= 0.5
        write_text('Refresh rate: ' + str(REFRESH_RATE))

    if badger.pressed(badger2040.BUTTON_DOWN):
        REFRESH_RATE += 0.5
        write_text('Refresh rate: ' + str(REFRESH_RATE))

    if RUNNING:
        draw_waves(time_offset)
        time_offset += WAVE_SPEED * REFRESH_RATE
        time.sleep(REFRESH_RATE)
