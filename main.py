import pygame
from game import Game
from planets import Planet
from net import Net
import pathlib
import random
import os
import pdb


class SpaceJam:
    def __init__(self, game) -> None:
        self.game = game
        self.planets = []
        self.ball = None
        self.level = 10
        self.util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Utils/'

    
    def game_loop(self):
        self.create_level(self.level)
        while self.game.running:
            self.game.setMisc()
            self.game.checkEvents()
            self.game.running = False if self.game.QUITKEY else True
            self.update_display() 
        
    
    
    def create_level(self, level):
        self.planets = []
        minx = 0  #Offset to stop a lot of planets from spawning together
        for i in range(level):
            x_position = random.randint(minx, i*100) 
            if i % 2 == 0:
                y_position = random.randint(100, self.game.yBound/2-100)
            else:
                y_position = random.randint(self.game.yBound/2-100, self.game.yBound-100) 


            planet_image = pygame.image.load(self.util_folder_path+'/planets/'+random.choice(os.listdir(self.util_folder_path+'/planets/')))  #Randomly picks a planet image
            
            if minx < self.game.xBound - 100:  #Change the 100 to a non hardcoded value 
                minx+=50
            else:
                minx=0
            
            self.planets.append(Planet(
                game=self.game,
                image=planet_image,
                x_size=100,
                y_size=100,
                x_pos=x_position,
                y_pos=y_position
            ))

    
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
        pass
    
    def update_display(self):
        self.game.resetKeys()
        self.update_planets()
        self.update_ball()
        pygame.display.update()


def game_loop(game, planet,net):
    while game.running:
        game.setMisc()
        game.checkEvents()
        game.running = False if game.QUITKEY else True
        planet.draw_planet()
        net.draw()
        
        update_display(game)

def update_display(game):
    game.resetKeys()
    pygame.display.update()
    
if __name__ == "__main__":
    util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Utils/'
    g1 = Game(
        xBound=800,
        yBound=800,
        caption="Space Jam",
        icon=pygame.image.load(util_folder_path+"icon.png"),
        background=pygame.image.load(util_folder_path+"background.jpeg")
    )
    spacejam = SpaceJam(game)
    spacejam.game_loop()
    
    net = Net(
        game = g1,
        hgt=100,
        planet=p1,
        direction='NORTH',
        image=pygame.image.load(util_folder_path+"net.png")
    )
    
    
    game_loop(g1, p1, net)
    
    
