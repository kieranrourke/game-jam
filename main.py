import pygame
from game import Game
from planets import Planet
from net import Net
import pathlib
import pdb


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
    
    p1 = Planet(
        image=pygame.image.load(util_folder_path+"planet.png"),
        game = g1,
        x_size=150,
        y_size=150,
        x_pos=400,
        y_pos=400
    )
    
    net = Net(
        game = g1,
        hgt=100,
        planet=p1,
        direction='NORTH'
    )
    # image=pygame.image.load(util_folder_path+"net.png")
    
    
    game_loop(g1, p1, net)
    
    