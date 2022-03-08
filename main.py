import pygame
import pathlib
from Game.spacejam import SpaceJam
from Game.game import Game 




if __name__ == "__main__":
    util_folder_path = str(pathlib.Path(__file__).parent.absolute()) +'/Game/Utils/'
    game = Game(
        xBound=800,
        yBound=800,
        caption="Space Jam",
        icon=pygame.image.load(util_folder_path+"icon.png"),
        background=pygame.image.load(util_folder_path+"space.png")
    )
    spacejam = SpaceJam(game)
    spacejam.start_game()