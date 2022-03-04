import pygame
from game import Game
import pathlib
import pdb


def game_loop(game):
    while game.running:
        game.setMisc()
        game.checkEvents()
        game.running = False if game.QUITKEY else True
        update_display(game)

def update_display(game):
    game.resetKeys()
    pygame.display.update()


if __name__ == "__main__":
    util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Utils/'
    game = Game(
        xBound=800,
        yBound=800,
        caption="Space Jam",
        icon=pygame.image.load(util_folder_path+"icon.png"),
        background=pygame.image.load(util_folder_path+"background.jpeg")
    )
    game_loop(game)    
