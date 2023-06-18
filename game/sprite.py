import pygame as pg
from math import *
import os
from collections import deque

from .const import *

class Sprite:
    def __init__(self, game, path = "resources/sprites/static_sprites/candlebra.png", pos=[7,7], scale=0.75, shift=0.25):
        self.game = game
        self.pos = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x,self.dist, self.norm_dist = 0,0,0,0,1,1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
    
    def get_sprite_projection(self):
        proj = ((RESOLUTION[0]//2) / tan(FOV/2)) / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        
        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = (self.screen_x - proj_width//2, RESOLUTION[1]//2 - proj_height//2 + height_shift)

        self.game.raycaster.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        player = self.game.player
        dx = self.pos[0] - player.pos[0]
        dy = self.pos[1] - player.pos[1]
        self.dx, self.dy = dx, dy
        self.theta = atan2(dy,dx)

        delta_angle = self.theta - player.angle
        if (dx > 0 and player.angle > pi) or (dx < 0 and dy < 0):
            delta_angle += 2 * pi
        
        delta_rays = delta_angle / (FOV / (RESOLUTION[0]//2))
        self.screen_x = (RESOLUTION[0]//4 + delta_rays) * 2

        self.dist = hypot(dx, dy)
        self.norm_dist = self.dist * cos(delta_angle)
        if -self.IMAGE_WIDTH//2 < self.screen_x < (RESOLUTION[0] + self.IMAGE_WIDTH//2) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()

class AnimatedSprite(Sprite):
    def __init__(self, game, path = "resources/sprites/animated_sprites/fire/0.png", pos=[7,7], scale=0.75, shift=0.25, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if(self.animation_trigger):
            images.rotate(-1)
            self.image = images[0]


    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True
    
    def get_images(self, path):
        images = deque()
        for file_name in sorted(os.listdir(path)):
            if os.path.isfile(os.path.join(path, file_name)):
                print(os.path.join(path, file_name))
                img = pg.image.load(os.path.join(path, file_name)).convert_alpha()
                images.append(img)
        return images