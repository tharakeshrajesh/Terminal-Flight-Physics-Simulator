# Importing libraries

from rich import print as rprint
from sys import exit
from subprocess import run
import numpy as np
import pymunk, cv2, numpyasciiart
from time import sleep
from keyboard import on_press_key
from sys import platform

space = pymunk.Space() # Creating a pymunk space
space.gravity = (0, 0) # Giving the space gravity but in our case we are using this to accelerate the plane
render = np.zeros((512, 512, 3), dtype=np.uint8) # Creating a 512x512 pixel numpy array
plane = None # Creating a plane object
img = np.array(cv2.resize(cv2.imread('plane.png'), (512, 512), interpolation=cv2.INTER_AREA)) # Creating another numpy array with the plane inside it this time

# Variables
gravity = 9.81 # Gravity of the simulation, the actual one
mass = 1500 # Mass of the airplane
inertia = 100 # Inertia of the airplane
alt = 0 # Altitude of the airplane
plane_knots = 0 # The actual knots the plane is moving at
knots = 0 # The target knots the plane should reach
vertical_speed = 0 # The vertical speed the plane is traveling at
drag = 0 # Drag force or air resistance
thrust = 0 # Thrust of the airplane
wing_area = 16.2 # Area of the wing in m² (small plane example)
AoA = 4 # angle of attack
rho = 1.225 # air density at sea level (kg/m³)
v = 0 # Velocity of the plane
lift = 0 # Lift force of the plane
# I just realized that there were two drag varaibles, not anymore though

width = 100 # Default width of the terminal "screen"
height_adjust_stretch = 3 # Height adjustment for it

# Some math functions for calculations

def lift_coefficient(aoa_deg):
    return 0.1 * aoa_deg  # crude linear approx

def drag_coefficient(aoa_deg):
    return 0.02 + 0.04 * aoa_deg**2  # typical U-shape curve

# Image blitting function (more efficient and faster than the older warp affine)
def blit_img(dst, src, center_x, center_y):
    h, w = src.shape[:2] # I forgot what these do so I will come back to this later
    x0 = center_x - w//2
    y0 = center_y - h//2
    x1 = x0 + w
    y1 = y0 + h
    # clip to dst bounds
    sx0 = max(0, -x0); sy0 = max(0, -y0)
    dx0 = max(0, x0); dy0 = max(0, y0)
    dx1 = min(dst.shape[1], x1); dy1 = min(dst.shape[0], y1)
    if dx0 >= dx1 or dy0 >= dy1:
        return
    dst[dy0:dy1, dx0:dx1] = src[sy0:(sy0 + (dy1-dy0)), sx0:(sx0 + (dx1-dx0))]


# Clear function
def clear():
    if platform.lower() == "win32": # Checks if platform is windows
        run(["cls"], shell=True) # Runs cls for windows because windows wants to be special
    else:
        run(["clear"], shell=True) # But Mac and Linux are normal

# Screen calibration function to adjust the "screen" to fit
def calibrate_screen():
    global height_adjust_stretch, width
    try:
        clear()
        rprint(numpyasciiart.to_ascii(render, width, height_adjust_stretch, "█") + "\nPlease adjust your terminal to fit the box above.\n[green]Ctrl+C to edit resolution.    Enter to continue.[/green]")
        input()
        clear()
        askInput()
    except KeyboardInterrupt:
        clear()
        rprint("[italic]*Bigger resolution means higher quality but more lag.[/italic]")
        height_adjust_stretch = float(input("Height adjust stretch: "))
        width = float(input("Width: "))
        calibrate_screen()


# Function to create the actual plane object IN the pymunk space
def create_plane(space):
    body = pymunk.Body(mass, inertia, pymunk.Body.DYNAMIC)
    body.position = (250, 200)
    shape = pymunk.Circle(body, 20)
    space.add(body, shape)
    return shape

# Rendering function
def renderplane(plane):
    global render
    render[:] = 0 # Clears the render of its old frame
    pos_x, pos_y = map(int, plane.body.position) # Extracts the x and y positions of the plane
    blit_img(render, img, pos_x, pos_y) # Blits the image to move the plane to the x and y positions of the plane
    cv2.circle(render, (pos_x, pos_y), 20, (255, 255, 255), 4) # Creates a circle that will act as the plane
    # Prints and displays to the terminal
    rprint(numpyasciiart.to_ascii(render, width, height_adjust_stretch, " ░░▒▒▓▓█") + f"\nGravity: {gravity}   Inertia: {inertia}   Mass: {mass}   Vertical Speed: {vertical_speed}   Thrust: {thrust}   Air Density at Sea Level (kg/m³): {rho}   Wing Area(m²): {wing_area}\nAngle of Attack: {AoA}   Velocity: {v}   Knots: {plane_knots}\n\n[green]Ctrl+C to edit variables\nR to recenter plane[/green]")

plane = create_plane(space)

# Repeating function to render each frame
def start():
    global plane, alt, plane_knots, vertical_speed, v, lift, drag
    try:
        while True:
            renderplane(plane) # Renders the frame
            sleep(0.02)  # 50 FPS

            # Convert speed to m/s for new velocity
            v = plane_knots * 0.51444

            # Physics: Lift & Drag
            cl = lift_coefficient(AoA) # Calculates lift coefficient
            cd = drag_coefficient(AoA) # Calculates drag coefficient
            lift = 0.5 * rho * v**2 * cl * wing_area # Calculates the lift using the coefficient, velocity, wing area, and air density
            drag = 0.5 * rho * v**2 * cd * wing_area # Same thing but for drag

            # Accelerations
            vertical_accel = (lift - mass * gravity) / mass # Calculates the vertical acceleration
            horizontal_accel = (thrust - drag) / mass # Same thing but for horizontal

            # Update speeds
            plane_knots += (horizontal_accel * 0.02) / 0.51444 # Slowly increases the plane's speed in knots
            vertical_speed += vertical_accel * 0.02 # Slowly increases the plane's vertical speed

            # Update altitude
            alt += vertical_speed * 0.02

            # Move plane body
            vx = v # More math I forgot
            vy = vertical_speed
            px_dx = vx * 0.02
            px_dy = -vy * 0.02  # Negative if up is decreasing y
            plane.body.position = (
                plane.body.position[0] + px_dx,
                plane.body.position[1] + px_dy
            )

    except KeyboardInterrupt:
        run('clear')
        askInput()

# Function to ask for user set variables
def askInput():
    try:
        global inertia, mass, vertical_speed, gravity, thrust, rho, wing_area, AoA, space
        rprint(f"Gravity: {gravity}   Inertia: {inertia}   Mass: {mass}   Vertical Speed: {vertical_speed}   Thrust: {thrust}   Air Density at Sea Level (kg/m³): {rho}   Wing Area(m²): {wing_area}\nAngle of Attack: {AoA}   Velocity: {v}   Knots: {plane_knots}\n\n[green]The above values are the defaults, you can now type your own values to test with or reenter the defaults.[/green]\n[red]Ctrl+C to quit[/red]\n")
        gravity = float(input("Gravity: "))
        inertia = float(input("Inertia: "))
        mass = float(input("Mass: "))
        vertical_speed = float(input("Vertical Speed: "))
        thrust = float(input("Thrust: "))
        rho = float(input("Air Density at Sea Level (kg/m³): "))
        wing_area = float(input("Wing Area (m²): "))
        space.gravity = (0, (knots * 0.51444 - plane_knots * 0.51444))
        run('clear')
        start()
    except KeyboardInterrupt:
        run('clear')
        exit(0)
    except Exception as e:
        run('clear')
        rprint("[red]That is not an option! Please try again.[/red]")
        askInput()
        return

# Function to reset the plane to camera view
def reset_plane_position(event=None):
    plane.body.position = (250, 200)

on_press_key("r", reset_plane_position) # Resets plane to camera view when R key is pressed

calibrate_screen()



