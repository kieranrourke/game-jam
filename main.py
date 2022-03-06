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
        self.net = None 
        self.level = 3 
        self.util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Utils/'
        self.shooter = Shooting(
            game,
            power_bar= pygame.transform.scale(pygame.image.load(self.util_folder_path+'arrow.png'),(2, 100)),
            arrow = pygame.transform.scale(pygame.image.load(self.util_folder_path+'real_arrow.png'), (100,100))
        )
        #Initialize ball
        ball_sheet = SpriteSheet(self.util_folder_path+'ball_sheet.png')
        self.ball = Ball(game, ball_sheet, 0,0,)        
        self.ball_ini_x = 0
        self.ball_ini_y = 0
        self.is_shot = False
        self.MAX_SHOT_TIME = 30
       
        
    def reset_ball(self):
        """Places ball at its initial position in the level"""
        self.is_shot = False
        self.ball.stop()
        self.ball.place_ball(self.ball_ini_x, self.ball_ini_y)

    def start_game(self):
        self.create_level(self.level)
        self.ball.stop()
        self.ball_ini_x = random.randint(self.game.xBound/2-100, 
                                         self.game.xBound/2+100)
        self.ball_ini_y = random.randint(self.game.yBound/2-100, 
                                         self.game.yBound/2+100)
        self.ball.place_ball(self.ball_ini_x, self.ball_ini_y)
        self.game_loop()

    def game_loop(self):
        while self.game.running:
            self.game.setMisc()
            self.game.checkEvents()
            #Can only use shooter when ball is still
            if self.is_shot == False:
                if self.game.UP_MOUSE_POS:
                    self.shooter.set_up_pos(self.game.UP_MOUSE_POS) 
                    self.shoot()
                elif self.game.DOWN_MOUSE_POS:
                    self.shooter.set_down_pos(self.game.DOWN_MOUSE_POS, self.ball._pos) 
            #Reset on ball stop?
            elif self.game.SPACEKEY:
                self.reset_ball()

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
        inc = int(self.game.xBound/level)
        for i in range(level):
            x_position = random.randint(minx, minx+100)
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
        self.net = Net(game, 75, self.planets[random.randint(0, len(self.planets)-1)], 'NORTH')
        
    def clear_level(self):
        self.planets = []
        self.ball.stop()

    def finish_level(self):
        """Called when a user finishes a level
        """
        self.clear_level()
    
    def update_planets(self):
        for planet in self.planets:
            planet.draw_planet()
    
    def shoot(self):
        """Shoots the ball using the shooter"""
        shot_force = self.shooter.calculate_force()
        if shot_force.magnitude() > 0:
            self.ball.shoot(shot_force)
            self.is_shot = True
                
    
    def update_ball(self) -> bool:
        """updates ball and tracks if player has scored

        Returns:
            bool: _description_
        """

        #Uses planets for acceleration
        if self.ball.update(self.planets, self.net):
            self.finish_level()
        
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
    spacejam.start_game()