import pygame
from planets import Planet
from game import Game      
    
class Rim(pygame.sprite.Sprite) :
    
    def __init__(self, color, width, height, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
    
    
class NetMesh(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()            
        
class Backboard(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()         
        
class Pole(pygame.sprite.Sprite): 
    
    def __init__(self, color, width, height, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

class Net(pygame.sprite.Group):
    
    def __init__(self, game, hgt: int, planet: Planet, direction: str):
        
        self.game = game
        self._rim = Rim((255,255,255), 50, 20, 350, 400)
        self._netmesh = NetMesh((255,255,255), 50, 20, 400, 450)
        self._bboard = Backboard((255,255,255), 50, 50, 480, 500)
        self._pole = Pole((255,255,255), 10, hgt, 500, 450)
        sprites = self._rim, self._netmesh, self._bboard, self._pole
        self.image = pygame.sprite.Group(sprites)
        
        
        if direction == 'NORTH':
            self.direction = 'NORTH'
            self.x = planet.x_pos
            self.y = planet.y_pos - (planet.y_size / 2)
        
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))