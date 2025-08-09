from PIL.Image import fromarray
from rich import print as rprint
from sys import exit
from subprocess import run
import numpy as np
import pymunk, cv2, numpyasciiart

space = pymunk.Space()
space.gravity = (0, 500)
render = np.zeros((512, 512, 3), dtype=np.uint8)
plane = None
img = np.array(fromarray(cv2.imread('plane.png')).resize((512, 512)))
arrows="←→↑↓"
mass = 1
inertia = 100
alt = 0
thrust = 0

def create_plane(space):
    global inertia, mass
    body = pymunk.Body(mass, inertia, pymunk.Body.DYNAMIC)
    body.position = (400, 0)
    shape = pymunk.Circle(body, 20)
    space.add(body, shape)
    return shape

def renderplane(plane):
    global render, alt, thrust, inertia, mass
    render[:] = 0
    render += cv2.warpAffine(img, np.float32([[1,0,(list(map(int, plane.body.position))[0]-250)],[0,1,(list(map(int, plane.body.position))[1]-250)]]), (512, 512))
    cv2.circle(render, tuple(map(int, plane.body.position)), 20, (255,255,255), 4)
    rprint(numpyasciiart.to_ascii(render, 100, 2.5, " ░░▒▒▓▓█") + f"\nAltitude: {alt}   Thrust: {thrust}   Gravity: {space.gravity[1]}   Inertia: {inertia}   Mass: {mass}    Direction: {"↑" if space.gravity[1] >= 0 else "↓"}")

plane = create_plane(space)

def start():
    global plane
    try:
        while True:
            renderplane(plane)
            space.step(0.02)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        run('clear')
        askInput()

def askInput():
    try:
        global alt, thrust, inertia, mass
        rprint(f"\nAltitude: {alt}   Thrust: {thrust}   Gravity: {space.gravity[1]}   Inertia: {inertia}   Mass: {mass}    Direction: {"↑" if space.gravity[1] >= 0 else "↓"}")
        gravity = int(input("Gravity: "))
        inertia = int(input("Inertia: "))
        mass = int(input("Mass: "))
        space.gravity = (0, gravity)
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

askInput()
