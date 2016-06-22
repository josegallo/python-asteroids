# ASTEROIDS: 2 PLAYERS
# To be played directly in http://www.codeskulptor.org/
import simplegui
import math
import random

# Game class
class Game:
    def __init__(self, width, height, lives, time, started = False):
        self.name = "Asteroids"
        self.width = 800
        self.height = 600
        self.score = 0
#        self.lives = 3
        self.time = 0
        self.started = False
        self.rock_group = set([])
        self.missile_group = set([])
        self.explosion_group = set ([])
    def re_start(self):
        asteroids.started = False
        asteroids.rock_group = set([])
        ship_thrust_sound.pause()
        for p in group_of_players:
            soundtrack.rewind()  
            p.vel = [0,0]
            if p.player == 2:
                p.pos = [asteroids.width* 2/3,asteroids.height * 1/2]
            if p.player == 1:
                p.pos = [asteroids.width* 1/3,asteroids.height * 1/2]
            p.thrust = False            
            p.angle = 0
            p.angle_vel = 0

asteroids = Game ( "Asteroids", 800, 600, 3, 0)      

# Information class
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
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)

#asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info, player):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.player = player
        self.lives = 3
        self.score = 0
        self.from_player = 0
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % asteroids.width
        self.pos[1] = (self.pos[1] + self.vel[1]) % asteroids.height

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):

        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        a_missile.from_player = self.player
        asteroids.missile_group.add(a_missile)

    def keys_down(self, key):
        if self.player == 2:
            if asteroids.started:
                if key == simplegui.KEY_MAP['left']:
                    self.decrement_angle_vel()
                elif key == simplegui.KEY_MAP['right']:
                    self.increment_angle_vel()
                elif key == simplegui.KEY_MAP['up']:
                    self.set_thrust(True)
                elif key == simplegui.KEY_MAP['space']:
                    self.shoot()
        if self.player == 1:
            if asteroids.started:
                if key == simplegui.KEY_MAP['a']:
                    self.decrement_angle_vel()
                elif key == simplegui.KEY_MAP['s']:
                    self.increment_angle_vel()
                elif key == simplegui.KEY_MAP['w']:
                    self.set_thrust(True)
                elif key == simplegui.KEY_MAP['e']:
                    self.shoot()
    def keys_up(self, key):
        if self.player == 2:
            if asteroids.started:
                if key == simplegui.KEY_MAP['left']:
                    self.increment_angle_vel()
                elif key == simplegui.KEY_MAP['right']:
                    self.decrement_angle_vel()
                elif key == simplegui.KEY_MAP['up']:
                    self.set_thrust(False)
        if self.player == 1:
            if asteroids.started:
                if key == simplegui.KEY_MAP['a']:
                    self.increment_angle_vel()
                elif key == simplegui.KEY_MAP['s']:
                    self.decrement_angle_vel()
                elif key == simplegui.KEY_MAP['w']:
                    self.set_thrust(False)        
    
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
        self.from_player = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        if self.animated:
            if self.age <= self.lifespan:
                canvas.draw_image(self.image, (self.age * self.image_center[0], self.image_center[1]),
                                  self.image_size, self.pos, self.image_size, self.angle)                

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % asteroids.width
        self.pos[1] = (self.pos[1] + self.vel[1]) % asteroids.height
        
        # age 
        self.age +=1
        if self.age > self.lifespan:
            return  True
        else: 
            return  False                 
    
    def collide(self, other_object):
        if dist (self.pos, other_object.pos) < self.radius + other_object.radius:
            return True
        else: 
            return False
        # if problems try with methods get_position and get_radius
        
  
        
# key handlers to control ship   
def keydown(key):
    my_ship.keys_down(key)
    my_ship_2.keys_down(key)

        
def keyup(key):
    my_ship.keys_up(key)
    my_ship_2.keys_up(key)
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    soundtrack.play()
    for p in group_of_players: 
        p.lives = 3
        p.score = 0
    center = [asteroids.width / 2, asteroids.height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not asteroids.started) and inwidth and inheight:
        asteroids.started = True

def draw(canvas):
    
    # animiate background
    asteroids.time += 1
    wtime = (asteroids.time / 4) % asteroids.width
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [asteroids.width / 2, asteroids.height / 2], [asteroids.width , asteroids.height])
    canvas.draw_image(debris_image, center, size, (wtime - asteroids.width / 2, asteroids.height / 2), [asteroids.width , asteroids.height])
    canvas.draw_image(debris_image, center, size, (wtime + asteroids.width / 2, asteroids.height / 2), [asteroids.width , asteroids.height])

    # draw UI
       

    canvas.draw_text("Lives", [50 , 50], 22, "White")
    canvas.draw_text(str(my_ship.lives), [50 , 80], 22, "White")
    canvas.draw_text("Lives", [50 +  600 , 50], 22, "White")
    canvas.draw_text(str(my_ship_2.lives), [50 +  600, 80], 22, "White")
    canvas.draw_text("Score", [50 , 110], 22, "White")
    canvas.draw_text("Score", [50 + 600, 110], 22, "White")
    canvas.draw_text(str(my_ship.score), [50 , 140], 22, "White")
    canvas.draw_text(str(my_ship_2.score), [50 + 600, 140], 22, "White")

    # draw ships 
    for p in group_of_players:
        p.draw(canvas) 
        p.update()

    # spawn rocks
    rock_spawner()
    
    # draw rocks in canvas
    process_sprite_group(asteroids.rock_group, canvas)
    
    # draw missile group in canvas
    process_sprite_group(asteroids.missile_group, canvas)

    # draw explosions in canvas
    process_sprite_group(asteroids.explosion_group, canvas)
    
    # collitions among rocks and missiles:
    group_group_collide(asteroids.missile_group, asteroids.rock_group)

    # collides ship and rocks
    for p in group_of_players:
        group_collide(asteroids.rock_group, p)
    
    # collides missiles with ships
    group_collide(asteroids.missile_group, my_ship)
    group_collide(asteroids.missile_group, my_ship_2)

    # draw splash screen if not started
    if not asteroids.started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [asteroids.width / 2, asteroids.height / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    if asteroids.started: 
        if len(asteroids.rock_group) <12:
            if asteroids.time % 100 == 0:
                rock_pos = [random.randrange(0, asteroids.width), random.randrange(0, asteroids.height)]
                rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
                rock_avel = random.random() * .2 - .1
                url = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/"
                url_asteroid_1 = url + "asteroid_blue.png"
                url_asteroid_2 = url + "asteroid_brown.png"
                url_asteroid_3 = url + "asteroid_blend.png"
                urls = [url_asteroid_1, url_asteroid_2, url_asteroid_3]
                print str(random.choice(urls))
                asteroid_image = simplegui.load_image(str(random.choice(urls)))
                new_set = []
                print "new pos", new_set
                for p in group_of_players:
                    if (dist(rock_pos, p.pos) > p.radius + asteroid_info.radius):
                        new_set.append (True)
                    else: 
                        new_set.append(False)
                    print new_set
#                for n in new_set:
                if new_set[len(new_set)-1] == True and new_set[0] == True:
                    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)    
                    asteroids.rock_group.add(a_rock)        


def proper_dist (rock,group_of_players):
    dists = set ([])
    for p in group_of_players:
        if dist(rock,p) > rock.radius + p.radius:
            dists.add(dist(rock,p))
    pass
    
    
# generate groups of sprites: ex rocks                
def process_sprite_group(group, canvas):
    set_remove_sprites = set ([])
    if asteroids.started:
        for o in group: 
            o.update()
            o.draw(canvas)
            if o.update():
                set_remove_sprites.add(o)                
            group.difference_update(set_remove_sprites)
                                            
# collition groups with object: ex, rocks with ship


def group_collide (set_objects, other_object):    
    set_remove_objects = set ([])
    for obj in set_objects:
        if obj.collide (other_object):
            set_remove_objects.add(obj)
            if other_object.from_player == 1:
                my_ship.score +=1
            if other_object.from_player == 2: 
                my_ship_2.score +=1
            if obj.from_player == 1: 
                my_ship.score +=1
            if obj.from_player == 2:
                my_ship_2.score +=1
            explosion_sound.play()
            explosion = Sprite (obj.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            asteroids.explosion_group.add(explosion)
            if other_object in group_of_players:
                explosion = Sprite (other_object.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
                asteroids.explosion_group.add(explosion)
                other_object.lives -=1
                explosion_sound.play()
                if other_object.lives <= 0:
                    asteroids.re_start()
            set_objects.difference_update(set_remove_objects)
            return True

def group_group_collide (group1, group2):
    for obj in group1:
        if group_collide(group2,obj):
            group1.discard(obj)

# initialize frame
frame = simplegui.create_frame(asteroids.name, asteroids.width, asteroids.height)

# initialize ship 
my_ship = Ship([asteroids.width * 1/ 3, asteroids.height / 2], [0, 0], 0, ship_image, ship_info, 1)
my_ship_2 = Ship([asteroids.width * 2/ 3, asteroids.height / 2], [0, 0], 0, ship_image, ship_info, 2)
group_of_players = ([my_ship, my_ship_2])
# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

# get things rolling

frame.start()
