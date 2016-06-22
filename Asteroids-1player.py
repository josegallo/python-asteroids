#ASTERIODS: 1 PLAYER
# To be played directly in http://www.codeskulptor.org/


import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
acc = [0,0]
vel = [0,0]
rocks = set([])
missiles = set([]) 
explotions = set([]) 
started = False
span_rock = 24
explostion_index = 0
rock_out_ship = False

# class for ImageInfo:
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
#nebula_info = ImageInfo([400, 300], [800, 600])
nebula_info = ImageInfo([512, 384], [1024, 768])
#nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")
nebula_image = simplegui.load_image("http://fondopc.com/wp-content/uploads/2009/10/104692universo1.jpg")
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_info_2 = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 250)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.3)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.1)

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def wrap(p):    
        if p[0] < 0:
            p[0] = WIDTH
        
        if p[0] > WIDTH:
            p[0] = 0

        if p[1] <= 0:
            p[1] = HEIGHT
        
        if p[1] > HEIGHT:
            p[1] = 0

class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = ship_image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.press = False
        self.pos_mis = [0,0]
        self.forward = [0,0]
        self.pos_exploted = [0,0]
        
    def keydown(self, key):
        global acc, vel
        r = math.radians(3)   
        if key == simplegui.KEY_MAP["right"]:
            self.angle_vel = r
        if key == simplegui.KEY_MAP["left"]:
            self.angle_vel = -r
        elif key == simplegui.KEY_MAP["up"]:
            self.thrust = True
            ship_thrust_sound.play()
            self.image_center = ship_info_2.get_center()            
        if key == simplegui.KEY_MAP["space"]:
            if started: 
                acc = (self.forward[0], self.forward[1])          
                self.shoot()
                        

    def keyup(self, key):         

        if key == simplegui.KEY_MAP["up"]:
            self.thrust = False
            ship_thrust_sound.rewind()
            self.image_center = ship_info.get_center()
        elif key == simplegui.KEY_MAP["right"] or key == simplegui.KEY_MAP["left"]:
            self.angle_vel = 0   
               
    def update(self):        
        
        self.angle += self.angle_vel
        
        # Position update
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        wrap(self.pos)
            
        # Velocity update - acceleration in direction of forward vector
        
        self.forward = angle_to_vector(self.angle)
        
        #Friction udpate 
        c = 0.05
        self.vel[0] *= (1 - c) 
        self.vel[1] *= (1 - c)
        
        #Thrust update - acceleration in direction of forward vector

        if self.thrust:
            self.vel[0] += self.forward[0] 
            self.vel[1] += self.forward[1]  

        for i in range(2):
            self.pos_mis [i] = self.pos[i] + angle_to_vector(self.angle)[i] * self.image_center[i]
            
#        print self.pos_mis[0], self.pos_mis[1]
        
    def shoot (self):
        forward = angle_to_vector(self.angle)
        pos_misille = (self.pos_mis [0], self.pos_mis[1])        
        vel_misille = (self.vel[0] + 10 * forward[0] , self.vel[1]  + 10 * forward[1])                 
        new_missile = Sprite(pos_misille, vel_misille, self.angle, 0, missile_image, missile_info, missile_sound)
        missiles.add(new_missile)
        
#   collide ship with rocks        
    def collide (self, other_sprite):
        global lives
        if dist(self.pos, other_sprite.pos) < self.radius + other_sprite.radius:
            self.pos_exploted[0] = self.pos[0]
            self.pos_exploted[1] = self.pos[1]
            e = (self.pos_exploted[0], self.pos_exploted[1])
            explotions.add(e)
            self.pos_exploted[0] = other_sprite.pos[0]
            self.pos_exploted[1] = other_sprite.pos[1]
            e = (self.pos_exploted[0], self.pos_exploted[1])
            explotions.add(e)
            return True
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, 
                          ship_info.get_size(), self.pos,
                          ship_info.get_size(), self.angle)    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.pos_exploted = [0,0]
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update_rock(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        wrap(self.pos)

    def update_missile(self):
        self.pos[0] +=  self.vel[0] 
        self.pos[1] +=  self.vel[1]  
    
    def missile_age(self):
        self.lifespan -=1
        
    def rock_spawner_s(self):

        p_x = random.randint(0, WIDTH)
        p_y = random.randint(0, HEIGHT)
#        print p_x, p_y
        if dist(my_ship.pos, (p_x,p_y)) > my_ship.radius + self.radius:
            self.pos[0] = p_x
            self.pos[1] = p_y               
            self.vel[0] = 1 * random.random () * random.randint(-1,1)
            self.vel[1] = .5 * random.random () * random.randint(-1,1)
            self.angle_vel = math.radians(random.randint (0, 5)) 
            rock_baby = Sprite((p_x,p_y), [self.vel[0], self.vel[1]], 
                               0, self.angle_vel, asteroid_image,
                               asteroid_info)


#   collide missiles and rocks        
    def collide(self, other_sprite):
        global explotions
        if dist(self.pos, other_sprite.pos) < self.radius + other_sprite.radius:
            self.pos_exploted[0] = self.pos[0]
            self.pos_exploted[1] = self.pos[1]
            e = (self.pos_exploted[0], self.pos_exploted[1])
            explotions.add(e)
            return True
            
def draw(canvas):
    global time, score, span_rock, explotions 
    global explosion_index, lives, started, rock_out_ship
    global rocky_baby
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())        
    
    # spawn rocks          
    if len(rocks) < 12:
        r = Sprite([WIDTH, HEIGHT], [0.2, 0.05], 0, 0.005, asteroid_image, asteroid_info)
        r.rock_spawner_s()
        rocks.add(r)
       
    # collitions rock and ships, rocks and missiles:
    if started:
        for r in rocks:
            rocks_remove = set([])
            missiles_remove = set([])
            r.draw(canvas)
            r.update_rock() 
            my_ship.collide(r)
            if my_ship.collide(r):
                lives -=1
                rocks_remove.add(r)
                explosion_sound.play()

            for m in missiles:
                m.missile_age()                    
                if r.collide(m) or m.lifespan == 0:                    
                    rocks_remove.add(r)
                    missiles_remove.add(m)
                    explosion_sound.play()
                    score +=1
            rocks.difference_update(rocks_remove)
            missiles.difference_update(missiles_remove)
        for m in missiles: 
            m.draw(canvas)
            m.update_missile()
    if lives == 0:
        soundtrack.rewind()
        started = False
        my_ship.pos = [WIDTH/2, HEIGHT/2]
        
    # explotions 
    for e in explotions:
        
        explosion_index = (time % (24*1.3))//1
        current_explosion_center =  [explosion_info.center[0] 
                                     + explosion_index * explosion_info.size[0],
                                     explosion_info.center[1]]            
        canvas.draw_image(explosion_image, current_explosion_center, 
                              explosion_info.size, (e[0],e[1])
                              , asteroid_info.size)
        if explosion_index == 23:
            explotions.remove(e)
            # print explotions
            
    # score and lifes
    canvas.draw_text("Score  " + str(score), [2.60 * WIDTH / 3, 0.25 * HEIGHT / 3], 25, "white")
    canvas.draw_text("Lives  " + str(lives), [0.10 * WIDTH / 3, 0.25 * HEIGHT / 3], 25, "white")

def keydown(key):
    my_ship.keydown(key)

def keyup(key):    
    my_ship.keyup(key)
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
        lives = 3
        score = 0
        
#Choose a velocity, position, and angular velocity randomly for the rock
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)    


# register handlers
frame.set_draw_handler(draw)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.set_mouseclick_handler(click)

# get things rolling

frame.start()
