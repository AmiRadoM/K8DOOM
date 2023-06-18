import pygame as pg

from .const import *
from .player import *
from .map import *
from .object_renderer import *
from .raycast import *
from .sprite import *
from .object_handler import *
from .weapon import *
from .sound import *
from .pathfinder import *

class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode([r * WINDOW_SCALE for r in RESOLUTION])
        self.screen = pg.Surface(RESOLUTION)
        self.delta_time = 0
        self.clock = pg.time.Clock()

        self.sound = Sound(self)
        self.player = Player(self)
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycaster = RayCaster(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinder = PathFinder(self)
    
    def events(self):
        # check if player closes the window (mainly)
        for e in pg.event.get():
            if(e.type == pg.QUIT):
                pg.quit()
                quit()
    
    def update(self):
        self.screen.fill(pg.Color(50,0,0))

        # math + logic functions
        self.player.move()
        self.player.single_fire()
        self.raycaster.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)

    def draw(self):
        # draw functions
        self.object_renderer.draw()
        self.weapon.draw()
        # self.player.draw()
        # self.map.draw()

        transformed_screen = pg.transform.scale(self.screen, [r * WINDOW_SCALE for r in RESOLUTION])
        self.window.blit(transformed_screen, (0,0))

    def run(self):
        # game loop
        while(True):
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()