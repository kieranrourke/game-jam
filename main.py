import pygame
from game import Game
import pathlib
import pdb
from ball import Ball
from planets import Planet


def game_loop(game):
    while game.running:
        game.setMisc()
        
        game.checkEvents()
        game.running = False if game.QUITKEY else True
        
        ##update objects at each tick to draw + update states
        #for planet in planets:
            #planet.update()
        ball.update()
        update_display(game)

def update_display(game):
    game.resetKeys()
    pygame.display.update() #No param means whole window updates


if __name__ == "__main__":
    util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Utils/'
    game = Game(
        xBound=800,
        yBound=800,
        caption="Space Jam",
        icon=pygame.image.load(util_folder_path+"icon.png"),
        background=pygame.image.load(util_folder_path+"background.jpeg")
    )
    
    planet_img = pygame.image.load(util_folder_path+"Planet.png")
    planets = [Planet(planet_img, game, 10, 10, 100, 100)]
    ball = Ball(game, planets, 40,40)
    
    game_loop(game)    
    
    