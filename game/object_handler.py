from .sprite import *
from .npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprites_path = "resources/sprites/npc/"
        self.static_sprites_path = "resources/sprites/static_sprites/"
        self.animated_sprites_path = "resources/sprites/animated_sprites/"
        self.npc_positions = {}

        self.add_sprite(Sprite(self.game))
        self.add_sprite(AnimatedSprite(self.game, pos=[7,8]))

        # self.add_npc(NPC(game))
        # self.add_npc(NPC(game, path="resources/sprites/npc/imp/0.png", pos=[9,14]))
        # self.add_npc(NPC(game, path="resources/sprites/npc/caco_demon/0.png", pos=[1,1]))
    
    def update(self):
        self.npc_positions = {(int(npc.pos[0]), int(npc.pos[1])) for npc in self.npc_list if npc.alive}
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()
    
    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)