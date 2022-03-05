import pygame
from planets import Planet
from game import Game

class Net:
    
    def __init__(self, game, hgt: int, planet: Planet, direction: str):
        
        self.game = game
        self._rim = Rim(white, 50, 20)
        self._netmesh = NetMesh(white, 50,20)
        self._bboard = Backboard(white, 50, 50)
        self.image = pygame.sprite.Group.add( 
            self._rim,
            self._netmesh,
            self._bboard
        )         
        self.height = hgt
        if direction == 'NORTH':
            self.direction = 'NORTH'
            self.x = planet.x_pos
            self.y = planet.y_pos - (planet.y_size / 2)
        
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        
    
    class Rim:
        
        def __init__(self, color, width, height):
            pygame.sprite.Sprite.__init(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
        
        
    class NetMesh:
        
        def __init(self, color, width, height):
            pygame.sprite.Sprite.__init(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()            
            
    class Backboard:
        
        def __init__(self, color, width, height):
            pygame.sprite.Sprite.__init(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()            
            