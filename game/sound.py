import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = "resources/sound/"
        self.shotgun = pg.mixer.Sound(self.path + "shotgun.wav")
        self.shotgun.set_volume(0.5)
        self.player_pain = pg.mixer.Sound(self.path + "player_pain.wav")
        self.player_pain.set_volume(0.5)
        self.theme = pg.mixer.Sound(self.path + "theme.mp3")
        self.theme.set_volume(0.5)
    
    def create_sound(self, path, volume = 0.7):
        sound =  pg.mixer.Sound(path)
        sound.set_volume(volume)
        return sound