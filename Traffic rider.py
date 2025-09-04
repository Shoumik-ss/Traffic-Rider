from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import os



camera_position = (0, 500, 500)
fovY = 120
grid_length = 100          
grid_size = 14              




playerPos = [0, 0, 0]       
playerAngle = 0            
camMode = "third"
gameStatus = False          


pickups = []                
rocks = []                
numRocks = 2


life = 3                 
score = 0
coins = 0
fuel = 100.0                
distance_covered = 0.0

minBoundary = -grid_size * grid_length // 2
maxBoundary = grid_size * grid_length // 2


boost = False


lanes = [-120, 0, 120]      
lane_index = 1              
base_speed = 1.0           
speed = base_speed
difficulty = 1.0
paused = False
started = False           
day_timer = 0.0             
DAY_CYCLE_SECONDS = 10.0    


SHOW_MILESTONE_EVERY = 0.1   
POPUP_DURATION = 1.2        
popup_timer = 0.0            
next_milestone = SHOW_MILESTONE_EVERY
last_milestone = 0.0        



def draw_text(x, y, text, font = GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def drawFloor(GRID_SIZE):
    
    glBegin(GL_QUADS)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            
            glColor3f(0.12, 0.12, 0.12)
            x = (i - GRID_SIZE // 2) * grid_length
            y = (j - GRID_SIZE // 2) * grid_length
            glVertex3f(x, y, 0)
            glVertex3f(x + grid_length, y, 0)
            glVertex3f(x + grid_length, y + grid_length, 0)
            glVertex3f(x, y + grid_length, 0)
    glEnd()

    
    glColor3f(1.0, 1.0, 0.3)
    for lx in lanes[:-1]:
        x = (lx + lanes[lanes.index(lx)+1]) / 2.0
        glBegin(GL_LINES)
        for j in range(-GRID_SIZE//2, GRID_SIZE//2):
            if j % 2 == 0:
                glVertex3f(x, j * grid_length, 1)
                glVertex3f(x, j * grid_length + grid_length*0.6, 1)
        glEnd()

def drawWalls():
    
    wall_ref = grid_length * grid_size // 2
    wallHeight = 30
    
    glColor3f(0.7, 0.5, 0.95)
    glBegin(GL_QUADS)
    glVertex3f(lanes[0] - 80, -wall_ref, 0)
    glVertex3f(lanes[0] - 80, wall_ref, 0)
    glVertex3f(lanes[0] - 80, wall_ref, wallHeight)
    glVertex3f(lanes[0] - 80, -wall_ref, wallHeight)
    glEnd()
   
    glBegin(GL_QUADS)
    glVertex3f(lanes[-1] + 80, -wall_ref, 0)
    glVertex3f(lanes[-1] + 80, wall_ref, 0)
    glVertex3f(lanes[-1] + 80, wall_ref, wallHeight)
    glVertex3f(lanes[-1] + 80, -wall_ref, wallHeight)
    glEnd()


fallen = False   

def drawBikeWithRider():
    
    glPushMatrix()
    
    playerPos[0] = lanes[lane_index]
    playerPos[1] = -250
    playerPos[2] = 0
    glTranslatef(*playerPos)

    if fallen:
        glRotatef(90, 0, 1, 0)

    
    glColor3f(0.2, 0.2, 0.8)
    glPushMatrix()
    glScalef(1.2, 2.5, 0.2)
    glutSolidCube(20)
    glPopMatrix()

    glColor3f(0,0,0)
    glPushMatrix()
    glTranslatef(0, 22, -5)
    glRotatef(90, 0,1,0)
    gluCylinder(gluNewQuadric(), 8, 8, 4, 20, 2)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, -22, -5)
    glRotatef(90, 0,1,0)
    gluCylinder(gluNewQuadric(), 8, 8, 4, 20, 2)
    glPopMatrix()

    
    glColor3f(0.7,0.7,0.7)
    glPushMatrix()
    glTranslatef(0, 26, 10)
    glScalef(0.3, 2.0, 0.3)
    glutSolidCube(12)
    glPopMatrix()

    
    glColor3f(0.3,0.3,0.3)
    glPushMatrix()
    glTranslatef(0, -5, 10)
    glScalef(1.0, 0.5, 0.3)
    glutSolidCube(18)
    glPopMatrix()

   
    glColor3f(1,0.8,0.6)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glScalef(0.5, 1.2, 1.0)
    glutSolidCube(15)
    glPopMatrix()

   
    glColor3f(1,0.8,0.6)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 8, 16, 16)
    glPopMatrix()

    
    glColor3f(1,0.8,0.6)
    glPushMatrix()
    glTranslatef(10, 5, 30)
    glScalef(0.3, 1.0, 0.3)
    glutSolidCube(12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-10, 5, 30)
    glScalef(0.3, 1.0, 0.3)
    glutSolidCube(12)
    glPopMatrix()


    glColor3f(0,0,1)
    glPushMatrix()
    glTranslatef(5, -10, 10)
    glScalef(0.3, 1.2, 0.3)
    glutSolidCube(12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-5, -10, 10)
    glScalef(0.3, 1.2, 0.3)
    glutSolidCube(12)
    glPopMatrix()

    glPopMatrix()

def drawPickups():
    for i in pickups:
        glPushMatrix()
        glTranslatef(*i['pickup_pos'])
        
        if i.get('type') == 'fuel':
            glColor3f(1, 0, 0) 
            glPushMatrix()
            glScalef(0.8, 1.2, 1.0)  
            glutSolidCube(15)        
            glPopMatrix()

           
            glColor3f(0.8, 0.8, 0.8)  
            glPushMatrix()
            glTranslatef(0, 0, 10)   
            glScalef(0.3, 0.8, 0.2)
            glutSolidCube(15)
            glPopMatrix()

        else:
            glColor3f(1, 0.84, 0)  
            gluSphere(gluNewQuadric(), 9, 12, 12)
        glPopMatrix()


def drawTrafficOrObstacles(e):
    glPushMatrix()
    glTranslatef(*e['rock_pos'])
    if e.get('kind') == 'rock':
        glColor3f(0.5, 0.5, 0.5)
        glScalef(1.0, 1.0, 0.8)
        glutSolidCube(40)
    glPopMatrix()

def generateRockPosition():
    
    lane = random.choice(lanes)
    y = random.randint(300, 1200)
    return {
        'rock_pos': [lane, y, 0],
        'scale': 1.0,
        'scale_dir': 0.0,
        'kind': "rock",
        'collide': False
    }


for n in range(numRocks):
    rocks.append(generateRockPosition())


def mouseListener(button, state, x, y):
    global camMode, paused, started, gameStatus
    
    y = 600 - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        if 10 <= x <= 90 and 520 <= y <= 590:
            
            if started and not gameStatus:
                paused = not paused
        elif 100 <= x <= 180 and 520 <= y <= 590:
            
            if started:
                do_restart()
        elif 190 <= x <= 270 and 520 <= y <= 590:
        
            os._exit(0)
        elif 280 <= x <= 360 and 520 <= y <= 590:
            
            camMode = "first" if camMode == "third" else "third"
        else:
          
            if not started:
                started = True
                paused = False
                gameStatus = False

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not gameStatus:
        
        camMode = "first" if camMode == "third" else "third"
        glutPostRedisplay()

def keyboardListener(key, x, y):
    global camMode, boost, paused, started, fuel
    
    if key == b'p':
        if started and not gameStatus:
            paused = not paused
    if key == b'c':
        
        boost = not boost
        fuel += fuel   
    if key == b'r':
        do_restart()
    if key == b'\x1b':  
        os._exit(0)

def specialKeyListener(key, x, y):
    global lane_index, speed
    if not started or paused or gameStatus:
        return
    if key == GLUT_KEY_RIGHT:
        lane_index = min(lane_index + 1, len(lanes)-1)
    if key == GLUT_KEY_LEFT:
        lane_index = max(lane_index - 1, 0)
    if key == GLUT_KEY_UP:
        speed += 1.5
    if key == GLUT_KEY_DOWN:
        speed = max(4.0, speed - 1.5)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camMode == "third":
        x = lanes[lane_index]
        y = -450
        z = 220
        gluLookAt(x, y, z, x, y+200, 0, 0, 0, 1)
    else:
        
        x = lanes[lane_index]
        y = -220
        z = 40
        gluLookAt(x, y, z, x, y+200, z, 0, 0, 1)

def checkCollision():
    global life, gameStatus, rocks
    if gameStatus or not started or paused:
        return
    if boost:   
        return
    px, py, pz = lanes[lane_index], -250, 0
    new_list = []
    for e in rocks:
        ex, ey, ez = e["rock_pos"]
        hit = abs(px - ex) < 30 and abs(py - ey) < 40
        if hit:
            life -= 1
            if life <= 0:
                game_over()
                return
            new_list.append(generateRockPosition())
        else:
            new_list.append(e)
    rocks[:] = new_list


def movePickup():
    if not started or paused or gameStatus:
        return
    global pickups
    b = 0
    while b < len(pickups):
        item = pickups[b]
        item['pickup_pos'][1] -= speed * difficulty * 0.9
        x, y, z = item['pickup_pos']
        if y < -700:
            pickups.pop(b)
        else:
            b += 1

def collect_pickups():
    global pickups, coins, fuel
    if not started or paused or gameStatus:
        return
    px, py, pz = lanes[lane_index], -250, 0
    keep = []
    for i in pickups:
        bx, by, bz = i['pickup_pos']
        if abs(px - bx) < 28 and abs(py - by) < 28:
            if i.get('type') == 'fuel':
                fuel = min(100.0, fuel + 35.0)
            else:
                coins += 1
        else:
            keep.append(i)
    pickups[:] = keep

def boost_mode():
    global speed
    if boost and started and not paused and not gameStatus:
        speed = min(base_speed * 2.2, speed + 0.4)
    else:
        target = base_speed + (difficulty - 1.0) * 3.0
        if speed > target:
            speed -= 0.2
        else:
            speed += 0.05

def spawn_coins_and_fuel():
    if random.random() < 0.005:
        lane = random.choice(lanes)
        y = random.randint(350, 900)
        pickups.append({'pickup_pos':[lane, y, 5], 'dir':(0,-1), 'type':'coin'})
    if random.random() < 0.0009:
        lane = random.choice(lanes)
        y = random.randint(450, 1000)
        pickups.append({'pickup_pos':[lane, y, 5], 'dir':(0,-1), 'type':'fuel'})

def progress_day_night(dt):
    global day_timer
    day_timer = (day_timer + dt) % (2*DAY_CYCLE_SECONDS)
    if day_timer < DAY_CYCLE_SECONDS:
        t = day_timer / DAY_CYCLE_SECONDS
        r = 0.25 + 0.2 * t
        g = 0.45 + 0.25 * t
        b = 0.8  + 0.15 * t
    else:
        t = (day_timer - DAY_CYCLE_SECONDS) / DAY_CYCLE_SECONDS
        r = 0.45 - 0.3 * t
        g = 0.7  - 0.45 * t
        b = 0.95 - 0.55 * t
    glClearColor(r, g, b, 1.0)

def do_restart():
    global pickups, rocks, boost, camMode, score, life, gameStatus
    global playerPos, playerAngle, coins, fuel, speed, distance_covered, difficulty
    global paused, started, last_milestone, popup_timer, next_milestone  # NEW
    global fallen
    pickups.clear()
    rocks.clear()
    for _ in range(numRocks):
        rocks.append(generateRockPosition())
    boost = False
    camMode = "third"
    score = 0
    coins = 0
    fuel = 100.0
    distance_covered = 0.0
    difficulty = 1.0
    speed = base_speed
    life = 3
    gameStatus = False
    playerPos[:] = [0, 0, 0]
    playerAngle = 0
    paused = False
    started = True
    last_milestone = 0.0
    popup_timer = 0.0          
    next_milestone = SHOW_MILESTONE_EVERY  
    fallen = False 
    glutPostRedisplay()

def game_over():
    global gameStatus, rocks, pickups, fallen
    gameStatus = True
    fallen = True   
    rocks.clear()
    pickups.clear()
import time

prev_time = None

def idle():
    global rocks, distance_covered, score, difficulty, fuel, prev_time
    global last_milestone, popup_timer, next_milestone  
    t = time.perf_counter()
    if prev_time is None:
        prev_time = t
    dt = max(0.0, min(0.05, t - prev_time))
    prev_time = t

    if not started or paused or gameStatus:
        boost_mode()       
        glutPostRedisplay()
        return
    progress_day_night(dt)

    world_speed = speed * difficulty
    for e in rocks:
        e['rock_pos'][1] -= world_speed
   
    rocks[:] = [e for e in rocks if e['rock_pos'][1] > -700] + \
               [generateRockPosition() for _ in range(max(0, numRocks - len(rocks)))]

    spawn_coins_and_fuel()
    movePickup()
    collect_pickups()
    checkCollision()
    fuel -= 6.0 * dt * (1.5 if boost else 1.0)
    if fuel <= 0:
        fuel = 0
        game_over()
    distance_covered += world_speed * dt * 0.02  # scaling
    score = int(distance_covered * 100)
    difficulty = 1.0 + distance_covered * 0.002
    boost_mode()
    if distance_covered >= next_milestone:
        popup_timer = POPUP_DURATION
        last_milestone = next_milestone
        next_milestone += SHOW_MILESTONE_EVERY
    if popup_timer > 0:
        popup_timer -= dt
        if popup_timer < 0:
            popup_timer = 0
    glutPostRedisplay()


def drawTree(x, y):
    
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(0.55, 0.27, 0.07)
    glPushMatrix()
    glScalef(1, 1, 8)
    glutSolidCube(5)
    glPopMatrix()
    glColor3f(0.0, 0.6, 0.0)
    glTranslatef(0, 0, 25)
    glutSolidSphere(12, 12, 12)
    glTranslatef(5, 0, 5)
    glutSolidSphere(10, 12, 12)
    glTranslatef(-10, 0, 0)
    glutSolidSphere(10, 12, 12)
    glPopMatrix()

def drawBuilding(x, y, floors=3):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(0.5, 0.5, 0.7)
    glScalef(20, 20, floors * 15)
    glutSolidCube(4)
    glPopMatrix()

def drawCloud(x, y, z=120):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 1, 1)
    glutSolidSphere(12, 12, 12)
    glTranslatef(8, 3, 0)
    glutSolidSphere(10, 12, 12)
    glTranslatef(-16, 0, 0)
    glutSolidSphere(10, 12, 12)
    glPopMatrix()

def drawScenery():
    for j in range(-5, 12):
        drawTree(lanes[0] - 150, j * 100)
        drawTree(lanes[-1] + 150, j * 100)

    for j in range(-3, 8):
        drawBuilding(lanes[0] - 250, j * 300, floors=random.randint(2,5))
        drawBuilding(lanes[-1] + 250, j * 300, floors=random.randint(2,5))

    for j in range(-2, 5):
        drawCloud(-200, j * 250, 200)
        drawCloud(220, j * 250, 220)



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 600)
    setupCamera()

    drawFloor(grid_size)
    drawScenery()
    drawWalls()
    drawBikeWithRider()
    for e in rocks:
        drawTrafficOrObstacles(e)
    drawPickups()

    draw_text(15, 560, "[Pause]")
    draw_text(105, 560, "[Restart]")
    draw_text(195, 560, "[Exit]")
    draw_text(285, 560, "[Cam]")

    if popup_timer > 0.0:
        if last_milestone < 1.0:
            txt = f" Milestone: {int(last_milestone * 100)} cm!"
        else:
            txt = f" Milestone: {last_milestone:.1f} m!"
        draw_text(360, 560, txt)

    if not gameStatus:
        draw_text(10, 460, f"Coins: {coins}")
        draw_text(10, 440, f"Score: {score}")
        draw_text(10, 420, f"Lives: {life}")
        draw_text(760, 500, f"Fuel: {int(fuel)}%")
    if not started:
        draw_text(320, 360, "TRAFFIC RIDER")
        draw_text(290, 320, "Click to Play")
    elif paused and not gameStatus:
        draw_text(440, 360, "PAUSED")
        draw_text(320, 320, "Click [Pause] or press 'P' to resume")
    elif gameStatus:
        draw_text(400, 400, "GAME OVER")
        draw_text(360, 370, f"Your Score: {score}   Coins: {coins}")
        draw_text(330, 120, "Press 'R' or click [Restart] to play again")

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 600)
    glutInitWindowPosition(250, 0)
    glutCreateWindow(b"Traffic Rider - OpenGL")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 0.0)
    glFogf(GL_FOG_END, 1000.0)
    glClearColor(0.3, 0.6, 0.9, 1.0)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()