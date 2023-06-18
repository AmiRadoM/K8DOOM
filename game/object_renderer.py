import pygame as pg

from .const import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.wall_textures = self.load_wall_textures()
        self.sky_texture = self.get_texture("resources/textures/sky.png", (RESOLUTION[0], RESOLUTION[1]//2))
        self.sky_offset = 0
        self.blood_texture = self.get_texture('resources/textures/blood_screen.png', RESOLUTION)
        self.blood_screen = False

        self.digit_size = 90
        self.digit_images = [pg.transform.scale(self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2),[self.digit_size / 4] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
    
    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_blood()

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.game.screen.blit(self.digits[char], (i * self.digit_size/4, 0))
        self.game.screen.blit(self.digits['10'], ((i+1) * self.digit_size/4, 0))

    def player_damage(self):
        self.blood_screen = True
    
    def draw_blood(self):
        if(self.blood_screen):
            self.game.screen.blit(self.blood_texture, (0,0))
            self.blood_screen = False
    
    def draw_background(self):
        # Sky
        self.sky_offset = (((self.game.player.angle / pi) % 2)/2) * RESOLUTION[0]
        self.game.screen.blit(self.sky_texture, (-self.sky_offset, 0))
        self.game.screen.blit(self.sky_texture, (-self.sky_offset + RESOLUTION[0], 0))
        #Floor
        pg.draw.rect(self.game.screen, pg.Color(25,25,25), (0, RESOLUTION[1]//2, RESOLUTION[0], RESOLUTION[1]))
    
    def render_game_objects(self):
        list_objects = sorted(self.game.raycaster.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.game.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return{
            1: self.get_texture('resources/textures/wall1.png')
        }