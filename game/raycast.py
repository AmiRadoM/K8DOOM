import pygame as pg
from math import *

from .const import *

class RayCaster:
    def __init__(self, game):
        self.game = game
        self.raycasting_results = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.raycasting_results):
            depth, proj_height, texture, offset = values
            
            if proj_height < RESOLUTION[1]:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - 2), 0, 2, TEXTURE_SIZE
                )

                wall_column = pg.transform.scale(wall_column, (2, proj_height))
                wall_pos = (ray * 2, RESOLUTION[1]//2 - proj_height//2)

            else:
                texture_height = TEXTURE_SIZE * RESOLUTION[1] / proj_height

                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - 2), TEXTURE_SIZE//2 - texture_height//2, 2, texture_height
                )

                wall_column = pg.transform.scale(wall_column, (2, RESOLUTION[1]))
                wall_pos = (ray * 2, 0)


            self.objects_to_render.append((depth, wall_column, wall_pos))

    # to learn how this function works you should go to: https://www.youtube.com/watch?v=ECqUrT7IdqQ
    def raycast(self):
        self.raycasting_results = []
        px = self.game.player.pos[0]
        py = self.game.player.pos[1]
        i_px = int(px)
        i_py = int(py)

        #angle of first ray and making sure it's not 0
        ray_angle = self.game.player.angle - FOV / 2
        ray_angle = 0.00001 if ray_angle == 0 else ray_angle

        for i in range(RESOLUTION[0]//2):
            sin_angle = sin(ray_angle)
            cos_angle = cos(ray_angle)

            #horizontal
            y_hor, dy = (i_py + 1, 1) if sin_angle > 0 else (i_py - 0.00001, -1)

            depth_hor = (y_hor - py) / sin_angle
            x_hor = px + depth_hor * cos_angle

            delta_depth = dy / sin_angle
            dx = delta_depth * cos_angle

            for j in range(DEPTH):
                tile_hor = int(x_hor), int(y_hor)

                #check if tile is wall
                if(tile_hor in self.game.map.world_map):
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            #vertical
            x_vert, dx = (i_px + 1, 1) if cos_angle > 0 else (i_px - 0.00001, -1)

            depth_vert = (x_vert - px) / cos_angle
            y_vert = py + depth_vert * sin_angle

            delta_depth = dx / cos_angle
            dy = delta_depth * sin_angle

            for j in range(DEPTH):
                tile_vert = int(x_vert), int(y_vert)

                #check if tile is wall
                if(tile_vert in self.game.map.world_map):
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            #depth 
            if(depth_vert < depth_hor):
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_angle > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = x_hor if sin_angle > 0 else (1 - x_hor)

            #remove fisheye
            depth *= cos(self.game.player.angle - ray_angle)

            #projection
            projection_height = ((RESOLUTION[0] // 2) / tan(FOV / 2)) / (depth + 0.00001)

            # Texture less projection
            # color = pg.Color([255 / (1 + depth ** 5 * 0.00001)] * 3)
            # pg.draw.rect(self.game.screen, color, (i * 2, RESOLUTION[1] // 2 - projection_height /2, 2, projection_height))

            # Texture Projection
            self.raycasting_results.append((depth, projection_height, texture, offset))

            ray_angle += FOV / (RESOLUTION[0]//2)
    
    def update(self):
        self.raycast()
        self.get_objects_to_render()