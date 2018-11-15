# Paul Fulton
# Based on Python Users Group event 13Nov18
# See https://github.com/bennuttall/pgz-campug

import random
WIDTH = 1024
HEIGHT = 384
TIMER = 0

boxes = 10
box_max = 40

alien = Actor('alien')
alien.pos = (50, 320)

objects = []
bi = {'x':0, 'y':1, 'width':2, 'height':3, 'speed':4}
GREEN = (200,255,200)

initialized = False
paused = False


def draw():
    global objects, GREEN, bi, TIMER, paused
    screen.clear()
    alien.draw()    
    if paused:
        screen.draw.text(str(TIMER), (250, 100), fontsize = 260, color = "orange", scolor = (100,100,100), shadow = (1,1))
        return
    screen.draw.text(str(TIMER), (0, 30), color = "orange", shadow = (2,2), fontsize = 32, scolor = (100,100,100) )
    for box in objects:
        stamp = Rect((box[bi['x']], box[bi['y']]), (box[bi['width']], box[bi['height']]))
        screen.draw.filled_rect(stamp,GREEN)
        #screen.draw.filled_circle((box[bi['x']], box[bi['y']]), box[bi['width']], GREEN)

def initialize_objects():
    global boxes, objects, box_max
    for i in range(0,boxes):
            objects.append(create_box())

def create_box():
    global box_max    
    xrand = random.randint(0,WIDTH) + WIDTH
    yrand = random.randint(0,HEIGHT - box_max)
    box_size = random.randint(0,box_max - 20) + 10
    box_speed = random.randint(0,3) + 1       
    new_box = [xrand, yrand, box_size, box_size, box_speed]
    return new_box

def update_objects():
    global bi, boxes, objects, paused, initialized
    new_objects = []
    for box in objects:        
        box[bi['x']] = box[bi['x']] - box[bi['speed']]
        if box[0] + box[2] > 0:
            new_objects.append(box)
        else:
            new_objects.append(create_box())
            new_objects.append(create_box())
    objects = list(new_objects)    
    
    for box in objects:
        box_rect = Rect((box[bi['x']], box[bi['y']]), (box[bi['width']], box[bi['height']]))
        if alien.colliderect(box_rect):
            alien.image = 'alien_hurt'
            initialized = False
            paused = True
            clock.schedule(restart, 1.0)            
            
def restart():
    global paused, objects, TIMER
    alien.image = 'alien'
    del objects[:]
    paused = False    
    TIMER = 0
    
def update():
    global initialized, paused, TIMER

    if paused == False:        
        if initialized == False:
            initialized = True
            initialize_objects()
        TIMER += 1
        
        if keyboard[keys.UP]:
            if alien.y > 50:
                alien.y -= 2
        elif alien.y < 320:
            alien.y += 3
        if keyboard[keys.LEFT] and alien.left > 0:
            alien.x -= 2
        if keyboard[keys.RIGHT] and alien.right < WIDTH:
            alien.x += 2
        update_objects()
    
    