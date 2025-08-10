from rich import print as rprint
from sys import exit
from subprocess import run
import numpy as np
import pymunk, cv2, numpyasciiart
from time import sleep
from keyboard import on_press_key

space = pymunk.Space()
space.gravity = (0, 0)
render = np.zeros((512, 512, 3), dtype=np.uint8)
plane = None
img = np.array(cv2.resize(cv2.imread('plane.png'), (512, 512), interpolation=cv2.INTER_AREA))

gravity = 9.81
mass = 1500
inertia = 100
alt = 0
plane_knots = 0
knots = 0
vertical_speed = 0
drag = 0
thrust = 0
wing_area = 16.2
AoA = 4
rho = 1.225
v = 0
lift = 0
drag = 0

width = 100
height_adjust_stretch = 3

def lift_coefficient(aoa_deg):
    return 0.1 * aoa_deg

def drag_coefficient(aoa_deg):
    return 0.02 + 0.04 * aoa_deg**2

def blit_img(dst, src, center_x, center_y):
    h, w = src.shape[:2]
    x0 = center_x - w//2
    y0 = center_y - h//2
    x1 = x0 + w
    y1 = y0 + h
    sx0 = max(0, -x0); sy0 = max(0, -y0)
    dx0 = max(0, x0); dy0 = max(0, y0)
    dx1 = min(dst.shape[1], x1); dy1 = min(dst.shape[0], y1)
    if dx0 >= dx1 or dy0 >= dy1:
        return
    dst[dy0:dy1, dx0:dx1] = src[sy0:(sy0 + (dy1-dy0)), sx0:(sx0 + (dx1-dx0))]

def calibrate_screen():
    global height_adjust_stretch, width
    try:
        run("clear")
        rprint(numpyasciiart.to_ascii(render, width, height_adjust_stretch, "█") + "\nPlease adjust your terminal to fit the box above.\n[green]Ctrl+C to edit resolution.    Enter to continue.[/green]")
        input()
        run("clear")
        askInput()
    except KeyboardInterrupt:
        run("clear")
        rprint("[italic]*Bigger resolution means higher quality but more lag.[/italic]")
        height_adjust_stretch = float(input("Height adjust stretch: "))
        width = float(input("Width: "))
        calibrate_screen()

def create_plane(space):
    body = pymunk.Body(mass, inertia, pymunk.Body.DYNAMIC)
    body.position = (250, 200)
    shape = pymunk.Circle(body, 20)
    space.add(body, shape)
    return shape

def renderplane(plane):
    global render
    render[:] = 0
    pos_x, pos_y = map(int, plane.body.position)
    blit_img(render, img, pos_x, pos_y)
    cv2.circle(render, (pos_x, pos_y), 20, (255, 255, 255), 4)
    rprint(numpyasciiart.to_ascii(render, width, height_adjust_stretch, " ░░▒▒▓▓█") + f"\nGravity: {gravity}   Inertia: {inertia}   Mass: {mass}   Vertical Speed: {vertical_speed}   Thrust: {thrust}   Air Density at Sea Level (kg/m³): {rho}   Wing Area(m²): {wing_area}\nAngle of Attack: {AoA}   Velocity: {v}   Knots: {plane_knots}\n\n[green]Ctrl+C to edit variables\nR to recenter plane[/green]")

plane = create_plane(space)

def start():
    global plane, alt, plane_knots, vertical_speed, v, lift, drag
    try:
        while True:
            renderplane(plane)
            sleep(0.02)

            v = plane_knots * 0.51444

            cl = lift_coefficient(AoA)
            cd = drag_coefficient(AoA)
            lift = 0.5 * rho * v**2 * cl * wing_area
            drag = 0.5 * rho * v**2 * cd * wing_area

            vertical_accel = (lift - mass * gravity) / mass
            horizontal_accel = (thrust - drag) / mass

            plane_knots += (horizontal_accel * 0.02) / 0.51444
            vertical_speed += vertical_accel * 0.02

            alt += vertical_speed * 0.02

            vx = v
            vy = vertical_speed
            px_dx = vx * 0.02
            px_dy = -vy * 0.02
            plane.body.position = (
                plane.body.position[0] + px_dx,
                plane.body.position[1] + px_dy
            )

    except KeyboardInterrupt:
        run('clear')
        askInput()

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

def reset_plane_position(event=None):
    plane.body.position = (250, 200)

on_press_key("r", reset_plane_position)

calibrate_screen()
