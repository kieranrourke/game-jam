import pygame
from game import Game
from planets import Planet
from net import Net
from ball import Ball
from shooting import Shooting

import pathlib
import random
import os
import pdb
from spriteSheet import SpriteSheet 
import time #For debug slowing down


class SpaceJam:
    def __init__(self, game) -> None:
        self.game = game
        self.planets = []
        self.ball = None
        self.net = None
        self.level = 8 #has to be 8?
        self.util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Utils/'
        self.shooter = Shooting(
            game,
            power_bar= pygame.transform.scale(pygame.image.load(self.util_folder_path+'arrow.png'),(2, 100)),
            arrow = pygame.transform.scale(pygame.image.load(self.util_folder_path+'real_arrow.png'), (100,100))
        )
        #PLACE BALL, store in sprite group
        ball_sheet = SpriteSheet(self.util_folder_path+'ball_sheet.png')
        self.ball = Ball(game, ball_sheet, 0,0,)


    def game_loop(self):
        self.create_level(self.level)
        while self.game.running:
            self.game.setMisc()
            self.game.checkEvents()
            if self.game.UP_MOUSE_POS:
                self.shooter.set_up_pos(self.game.UP_MOUSE_POS) 
            elif self.game.DOWN_MOUSE_POS:
                self.shooter.set_down_pos(self.game.DOWN_MOUSE_POS, self.ball._pos) 

            self.game.running = False if self.game.QUITKEY else True
            self.update_display() 
            self.game.clock.tick(60)
    
    def create_planet(self, planet: int, x_position, y_position):
        """Chooses a planet size to create from the predifined planets, 
        at the given position. Valid planet sizes are 1, 2, or 3. 
        invalid inputs default to 3"""
        #Create planet types, increase in size with number:
        
        if planet == 1: #smallest planet, size/image hardcoded
            planet_image = pygame.image.load(self.util_folder_path+
                                             '/planets/planet_32.png')
            SIZE = 32
            
        elif planet == 2:
            planet_image = pygame.image.load(self.util_folder_path+
                                             '/planets/planet_64.png')
            SIZE = 64  
            
        else:
            planet_image = pygame.image.load(self.util_folder_path+
                                             '/planets/planet_128.png')
            SIZE = 128
            
        return Planet(self.game, planet_image, SIZE, x_position, y_position) 
        
    def create_level(self, level):
        #PLACE PLANETS, store in sprite group
        self.planets = []
        minx = 0  #Offset to stop a lot of planets from spawning together
        inc = self.game.xBound/level
        #print(inc)
        for i in range(level):
            x_position = random.randint(minx, i*100) 
            if i % 2 == 0:
                y_position = random.randint(100, self.game.yBound/2-100)
            else:
                y_position = random.randint(self.game.yBound/2-100, self.game.yBound-100) 

            planet_image = pygame.image.load(self.util_folder_path+'/planets/'+random.choice(os.listdir(self.util_folder_path+'/planets/')))  #Randomly picks a planet image
            
            if minx < self.game.xBound - 100:  #Change the 100 to a non hardcoded value 
                minx+=inc
            else:
                minx=0
            
            ##Uses simple planet models atm
#             self.planets.append(self.create_planet(random.randint(1, 3), 
#                                               x_position, y_position))
            self.planets.append(Planet(
                game=self.game,
                image=planet_image,
                size = 100,
                x_pos=x_position,
                y_pos=y_position
            ))
            
                
        #PLACE NET
        self.net = Net(game, 75, self.planets[0], 'NORTH')
        
    def clear_level(self):
        pass

    def finish_level(self):
        """Called when a user finishes a level
        """
        self.clear_level()
    
    def update_planets(self):
        for planet in self.planets:
            planet.draw_planet()
    
    def update_ball(self):
        #Uses planets for acceleration
        scored = self.ball.update(self.planets, self.net)
        
    def update_net(self):
        self.net.update() 
  
    def update_shooter(self):
        if self.shooter.visible:
            self.shooter.update_arrow()
            self.shooter.update_progress_bar()

    def update_display(self):
        self.game.resetKeys()
        self.update_net()
        self.update_ball() #Order matters, determines foreground/background
        self.update_planets()
        self.update_shooter()
        pygame.display.update()
    
if __name__ == "__main__":
    util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Utils/'
    game = Game(
        xBound=800,
        yBound=800,
        caption="Space Jam",
        icon=pygame.image.load(util_folder_path+"icon.png"),
        background=pygame.image.load(util_folder_path+"space.png")
    )
    spacejam = SpaceJam(game)
    spacejam.game_loop()
