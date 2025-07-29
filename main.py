from PIL.Image import fromarray
from rich import print as rprint
import numpy as np
import pymunk, cv2, numpyasciiart

space = pymunk.Space()
space.gravity = (0, 500)
render = np.zeros((512, 512, 3), dtype=np.uint8)
apples = []
img = np.array(fromarray(cv2.imread('plane.png')).resize((512, 512)))

def create_apples(space):
    body = pymunk.Body(1, 100, pymunk.Body.DYNAMIC)
    body.position = (400, 0)
    shape = pymunk.Circle(body, 20)
    space.add(body, shape)
    return shape

def draw_apples(apples):
    global render
    render[:] = 0
    for apple in apples:
        render += cv2.warpAffine(img, np.float32([[1,0,(list(map(int, apple.body.position))[0]-250)],[0,1,(list(map(int, apple.body.position))[1]-250)]]), (512, 512))
        cv2.circle(render, tuple(map(int, apple.body.position)), 20, (255,255,255), 4)
        rprint(numpyasciiart.to_ascii(render, 100, 2.5, " ░░▒▒▓▓█"))

apples.append(create_apples(space))

while True:
    draw_apples(apples)
    space.step(0.02)
    cv2.waitKey(1)
