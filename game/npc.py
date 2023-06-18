from .sprite import *
import random

class NPC(AnimatedSprite):
    def __init__(self, game, path="resources/sprites/npc/soldier/0.png", pos=[14,14], scale=0.6, shift=0.38, animation_time=90):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.idle_images = self.get_images(self.path + "/idle")
        self.walk_images = self.get_images(self.path + "/walk")
        self.attack_images = self.get_images(self.path + "/attack")
        self.pain_images = self.get_images(self.path + "/pain")
        self.death_images = self.get_images(self.path + "/death")

        self.attack_sound = game.sound.create_sound(self.path + "/sound/attack.wav")
        self.death_sound = game.sound.create_sound(self.path + "/sound/death.wav")
        self.pain_sound = game.sound.create_sound(self.path + "/sound/pain.wav")

        self.attack_dist = 1.5
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        
        self.alive = True
        self.pain = False
        self.raycast_value = False
        self.player_search_trigger = False

        self.frame_counter = 0
    
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.behavior()
    
    def move(self):
        next_pos = self.game.pathfinder.get_path((int(self.pos[0]),int(self.pos[1])), (int(self.game.player.pos[0]), int(self.game.player.pos[1])))
        next_x, next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:
            angle = atan2(next_y + 0.5 - self.pos[1], next_x + 0.5 - self.pos[0])
            dx = cos(angle) * self.speed
            dy = sin(angle) * self.speed
            self.collision(dx, dy)
    
    def attack(self):
        if self.animation_trigger:
            self.attack_sound.play()
            if random.random() < self.accuracy:
                print(f"-{self.attack_damage}")
                self.game.player.get_damage(self.attack_damage)
    
    def collision(self, dx, dy):
        # simple check before movement if inside wall, if not than move
        if not (int(self.pos[0] + dx * self.size), int(self.pos[1])) in self.game.map.world_map:
            self.pos[0] += dx
        if not (int(self.pos[0]), int(self.pos[1] + dy * self.size)) in self.game.map.world_map:
            self.pos[1] += dy

    def animate_death(self):
        if not self.alive:
            if self.animation_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1


    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
    
    def check_hit_npc(self):
        if self.raycast_value and self.game.player.shot:
            if RESOLUTION[0]//2 - self.sprite_half_width < self.screen_x < RESOLUTION[0]//2 + self.sprite_half_width:
                self.pain_sound.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()
    
    def check_health(self):
        if(self.health <= 0):
            self.alive = False
            self.death_sound.play()

    def behavior(self):
        if self.alive:
            self.raycast_value = self.raycast_player_npc()
            self.check_hit_npc()
            if self.pain:
                self.animate_pain()
            elif self.raycast_value:
                if(self.dist <= self.attack_dist):
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.move()
                self.player_search_trigger = True
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.move()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()
    
    def raycast_player_npc(self):
        wall_dist_vert, wall_dist_hor = 0, 0
        player_dist_vert, player_dist_hor = 0, 0

        px = self.game.player.pos[0]
        py = self.game.player.pos[1]
        i_px = int(px)
        i_py = int(py)

        if([int(self.pos[0]),int(self.pos[1])] == [i_px, i_py]):
            return True


        #angle of first ray and making sure it's not 0
        ray_angle = self.theta
        ray_angle = 0.00001 if ray_angle == 0 else ray_angle

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
            if tile_hor == (int(self.pos[0]),int(self.pos[1])):
                player_dist_hor = depth_hor
                break
            #check if tile is wall
            if(tile_hor in self.game.map.world_map):
                wall_dist_hor = depth_hor   
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
            if tile_vert == (int(self.pos[0]),int(self.pos[1])):
                player_dist_vert = depth_vert
                break
            #check if tile is wall
            if(tile_vert in self.game.map.world_map):
                wall_dist_vert = depth_vert
                break
            
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_vert, player_dist_hor)
        wall_dist = max(wall_dist_vert, wall_dist_hor)

        return 0 < player_dist < wall_dist or not wall_dist
