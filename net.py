import pygame
from planets import Planet
from game import Game

class Net:
    
    def __init__(self, game, hgt: int, planet: Planet, direction: str, image):
        
        self.game = game
        self.image = pygame.transform.scale(image, (hgt, hgt))
        self.height = hgt
        if direction == 'NORTH':
            self.direction = 'NORTH'
            self.x = planet.x_pos
            self.y = planet.y_pos - (planet.y_size / 2)
        
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
    
    