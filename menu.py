import pygame
from game import Button


class Menu():
    def __init__(self, game) -> None:
        self.game = game
        self.background = self.game.background
        # Text to display 
        self.font1 = pygame.font.Font('freesansbold.ttf', 65)
        self.font2 = pygame.font.Font('freesansbold.ttf', 30)

        self.text1 = "Click to Start" 
        self.text2 = "If you find a Level Impossible Click Reset Game"

    def display_loop(self):
        while self.game.inMenu:
            self.game.setMisc()
            self.game.checkEvents()
            self.display_message()
            if self.game.UP_MOUSE_POS:
               self.start_game() 
            self.game.resetKeys()
            pygame.display.update()
    
    def start_game(self):
        self.game.inMenu = False
        self.game.running = True
        pass

    def display_message(self):
        self.xPos = 150
        self.yPos = self.game.yBound/2 -200

        text1 = self.font1.render(self.text1, True, (192,192,192)) 
        text2 = self.font2.render(self.text2, True, (96,96,96))

        self.game.draw(text1, self.xPos,self.yPos)
        self.game.draw(text2, self.xPos-100, self.yPos+150)