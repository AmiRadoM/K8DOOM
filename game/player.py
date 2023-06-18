import pygame as pg
from math import *

from .const import *

class Player:
    def __init__(self, game):
        self.game = game
        self.pos = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.shot = False
    
    def single_fire(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT] and not self.shot and not self.game.weapon.reloading:
            self.game.sound.shotgun.play()
            self.shot = True
            self.game.weapon.reloading = True
    
    def get_damage(self, damage):
        self.health -= damage
        if(self.health <= 0):
            # self.pos = PLAYER_POS
            self.health = 100
        self.game.sound.player_pain.play()
        self.game.object_renderer.player_damage()
    
    def move(self):
        # simple trigonometry to calculate vectors to add to position of player on movement
        delta_x = 0
        delta_y = 0

        sin_speed = sin(self.angle) * PLAYER_SPEED * self.game.delta_time
        cos_speed = cos(self.angle) * PLAYER_SPEED * self.game.delta_time

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            delta_x += cos_speed
            delta_y += sin_speed
        if keys[pg.K_s]:
            delta_x -= cos_speed
            delta_y -= sin_speed
        if keys[pg.K_a]:
            delta_x += sin_speed
            delta_y -= cos_speed
        if keys[pg.K_d]:
            delta_x -= sin_speed
            delta_y += cos_speed

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        
        self.collision(delta_x, delta_y)
        self.angle %= pi * 2

    def collision(self, dx, dy):
        # simple check before movement if inside wall, if not than move
        scale = PLAYER_SIZE / (self.game.delta_time + 0.000001)
        if not (int(self.pos[0] + dx * scale), int(self.pos[1])) in self.game.map.world_map:
            self.pos[0] += dx
        if not (int(self.pos[0]), int(self.pos[1] + dy * scale)) in self.game.map.world_map:
            self.pos[1] += dy
    
    def draw(self):
        pg.draw.line(self.game.screen, pg.Color(200,255,0), ((self.pos[0] + 1) * 11, (self.pos[1] + 1) * 11),
                    ((self.pos[0] + RESOLUTION[0] * cos(self.angle) + 1) * 11,
                     (self.pos[1] + RESOLUTION[0] * sin(self.angle) + 1) * 11), 1)
        pg.draw.circle(self.game.screen, pg.Color(0,255,0), ((self.pos[0] + 1) * 11, (self.pos[1] + 1) * 11), 4)
