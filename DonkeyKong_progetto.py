import g2d
import actor
import random

# Definizione delle costanti

SCREEN_WIDTH = 224
SCREEN_HEIGHT = 256
GRAVITY = 1
JUMP_VELOCITY = -15
PLATFORM_HEIGHT = 8
MARIO_WIDTH = 11
MARIO_HEIGHT = 15
BACKGROUND_IMAGE = r"C:\Users\franc\Desktop\Donkey-Kong\donkey-kong-bg.png"
CHARACTER_IMAGE = r"C:\Users\franc\Desktop\Donkey-Kong\donkey-kong.png"
ELEMENTS_FILE = r"C:/Users/franc/Desktop/Donkey-Kong/dk_elements.txt"

g2d.init_canvas((SCREEN_WIDTH, SCREEN_HEIGHT), 3)

class Platform(actor.Actor):
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def pos(self):
        return (self._x, self._y)
    
    def size(self):
        return (self._width, self._height) 

class Ladder(actor.Actor):
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def pos(self):
        return (self._x, self._y)
    
    def size(self):
        return (self._width, self._height)


class Mario(actor.Actor):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False

    def size(self):
        return (MARIO_WIDTH, MARIO_HEIGHT)
    
    def pos(self):
        return (self._x, self._y)

    def jump(self):
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (197, 3), (12, 16))
        if not self.is_jumping and (self._y == SCREEN_HEIGHT - MARIO_HEIGHT or self._y == SCREEN_HEIGHT - MARIO_HEIGHT - 1):
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True  # Set jumping flag


    #the problem here is that collisions are detected at the end of key pressing and this is problematic to check


    def update(self, dir):

        if dir=="Right":
            self.velocity_x = 5
            self._x += self.velocity_x
            if self._x >= SCREEN_WIDTH - MARIO_WIDTH:
                self.velocity_x = 0
                self._x = SCREEN_WIDTH - MARIO_WIDTH
        elif dir=="Left":
            self.velocity_x = -5
            self._x += self.velocity_x
            if self._x <= 0:
                self.velocity_x = 0
                self._x = 0
        elif dir=="Up":
            if not self.is_jumping:
                self.velocity_y += GRAVITY
                self._y += self.velocity_y
                if self._y > SCREEN_HEIGHT - MARIO_HEIGHT:
                    self._y = SCREEN_HEIGHT - MARIO_HEIGHT
            else:
                # If jumping, update the position until reaching the peak
                self.velocity_y += GRAVITY
                self._y += self.velocity_y
                if self.velocity_y >= 0:
                    self.is_jumping = False
        elif dir=="platform_collision":
            if self.is_jumping:
                self.velocity_x = 0
                self.velocity_y = 0
                self._y = self._y + 2
            else:
                self.velocity_x = 0
                self.velocity_y = 0
                self._y = self._y - 2
        elif dir=="ladder_collision":
            g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (126, 23), (12, 16))
            self.velocity_x = 0
            self.velocity_y = 0
            self._y = self._y - 3
        elif dir=="ladder_collision_down":
            g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (126, 23), (12, 16))
            self.velocity_x = 0
            self.velocity_y = 0
            self._y = self._y + 3

    def drawLeft(self):
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (136, 3), (12, 16)),
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (115, 3), (12, 16)),
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (94, 3), (12, 16))
        

    def drawRight(self):
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (158, 3), (12, 16))
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (176, 3), (12, 16))
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (197, 3), (12, 16))

class Barrels(actor.Actor):
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._w = width
        self.velocity_x = 3
        self.on_platform = False
        self._dy = 0
        self._height = height

    def fall(self):
        self._dy += GRAVITY
        self._y += self._dy

    def update(self):
        
        if not self.on_platform:
            self._y -= 1
            self._x += self.velocity_x
            if self._x < 0 or self._x + self._w > SCREEN_WIDTH:
                self.velocity_x = -self.velocity_x
                self._y+=16


    def draw(self):
        g2d.draw_image_clip(CHARACTER_IMAGE, (self._x, self._y), (66, 258), (12, 10))
        
    def pos(self):
        return self._x, self._y
    
    def size(self):
        return self._w, self._height
        

class DonkeyKongArena(actor.Arena):
    def __init__(self):
        self._background = g2d.load_image(BACKGROUND_IMAGE)
        self.mario = Mario(44, 232)
        self.barrels = [Barrels(random.randint(0, SCREEN_WIDTH - 14), 73, 10, 5) for _ in range(5)]
        self.platforms = []
        self.ladders = []
        self.load_elements_from_file()

    def load_elements_from_file(self):
        with open(ELEMENTS_FILE, 'r') as file:
            elements_info = [line.strip().split() for line in file]
    
        for info in elements_info:
            element_type = info[0]
            if element_type.lower() == 'platform':
                x, y, width, height = map(int, info[1:])
                platform = Platform(x, y, width, height)
                self.platforms.append(platform)
            elif element_type.lower() == 'ladder':
                x, y, width, height = map(int, info[1:])
                ladder = Ladder(x, y, width, height)
                self.ladders.append(ladder)

    def tick(self):
        g2d.draw_image(self._background, (0, 0))
        self.mario.drawRight()
        

        # check if the player want to move to the right
        if "ArrowRight" in g2d.current_keys():
            self.mario.update("Right")
            self.mario.drawRight()

        # check if the player want to move to the left
        if "ArrowLeft" in g2d.current_keys():
            self.mario.update("Left")
            self.mario.drawLeft()
           
        # check if the player want to jump
        if "ArrowUp" in g2d.current_keys():
            self.mario.update("Up")
            self.mario.jump()

            #control if the jump is toward left or right and put the right sprite in the animation
            if "ArrowLeft" in g2d.current_keys():
                g2d.draw_image_clip(CHARACTER_IMAGE, (self.mario._x, self.mario._y), (94, 3), (12, 16))
            
        # checking every tick if a platform is colliding with Mario and updating his position
        for platform in self.platforms:
            if self.check_collision(self.mario, platform):
                self.mario.update("platform_collision")
        
        # checking every tick if a ladder is colliding with Mario and updating his position, this function only works if the
        # player click "ARROW UP", otherwise Mario keeps walking
        for ladder in self.ladders:
            if self.check_collision(self.mario, ladder) and "ArrowUp" in g2d.current_keys():
                self.mario.update("ladder_collision")
            elif self.check_collision(self.mario, ladder) and "ArrowDown" in g2d.current_keys():
                self.mario.update("ladder_collision_down")
        

        # updating barrels positions and """""sprites"""""
        for barrel in self.barrels:
            barrel.fall()

            for platform in self.platforms:
                if self.check_collision(barrel, platform):
                    platform.on_platform = True
                    barrel._dy = 0  # Stop falling when colliding with a platform
            barrel.update()
            if self.check_collision(self.mario, barrel):
                g2d.alert("GAME OVER")
                exit()
            barrel.draw()

        
    def game_loop(self):
        g2d.game_loop(self.tick)


arena = DonkeyKongArena()
#g2d.play_audio("donkeykong.ogg", loop=True) #playing donkey kong theme
g2d.main_loop(arena.tick)