import pygame
from planets import Planet
from game import Game      
    
class Rim(pygame.sprite.Sprite):
    
    def __init__(self, game, color, width, height, x_pos, y_pos) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
    def _draw(self)-> None:
        self.game.screen.blit(self.image, (self.x_pos, self.y_pos))    
    
    
class NetMesh(pygame.sprite.Sprite):
    
    def __init__(self, game, color, width, height, x_pos, y_pos)-> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()      
        
    def _draw(self)-> None:
        self.game.screen.blit(self.image, (self.x_pos, self.y_pos))    
        
class Backboard(pygame.sprite.Sprite):
    
    def __init__(self, game, color, width, height, x_pos, y_pos)-> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()    
        
    def _draw(self)-> None:
        self.game.screen.blit(self.image, (self.x_pos, self.y_pos))
        
class Pole(pygame.sprite.Sprite): 
    
    def __init__(self, game, color, width, height, x_pos, y_pos)-> None:
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
    def _draw(self)-> None:
        self.game.screen.blit(self.image, (self.x_pos, self.y_pos))    

class Net(pygame.sprite.Group):
    
    def __init__(self, game, hgt: int, planet: Planet, direction: str)-> None:
        #Attributes
        self.game = game
        self.planet = planet
        self.direction = direction
        
        # Size constants for each net 
        POLE_WIDTH = 14
        POLE_HEIGHT = hgt
        
        BBOARD_WIDTH = 48
        BBOARD_HEIGHT = 60        
        
        RIM_WIDTH = 64
        RIM_HEIGHT = 20   
        
        MESH_WIDTH = 48
        MESH_HEIGHT = 20        
        
        POLE_POS_X = self.planet.get_pos().x + (self.planet.get_size() / 2)
        POLE_POS_Y = self.planet.get_pos().y - POLE_HEIGHT
        
        BBOARD_POS_X = POLE_POS_X - 5
        BBOARD_POS_Y = POLE_POS_Y - BBOARD_HEIGHT + 5
        
        RIM_POS_X = BBOARD_POS_X + BBOARD_WIDTH - 5
        RIM_POS_Y = BBOARD_POS_Y + BBOARD_HEIGHT - RIM_HEIGHT - 5
        
        MESH_POS_X = RIM_POS_X + ( (RIM_WIDTH - MESH_WIDTH) / 2)
        MESH_POS_Y = RIM_POS_Y + ( (RIM_HEIGHT - MESH_HEIGHT) / 2)
        
        
        
        # Net group
        
        self._pole = Pole(self.game, (255,255,255), POLE_WIDTH, POLE_HEIGHT, POLE_POS_X, POLE_POS_Y)
        
        self._bboard = Backboard(self.game, (0,0,255), BBOARD_WIDTH , BBOARD_HEIGHT, BBOARD_POS_X, BBOARD_POS_Y)
        
        self._rim = Rim(self.game, (255,0,0), RIM_WIDTH, RIM_HEIGHT, RIM_POS_X, RIM_POS_Y)
        
        self._netmesh = NetMesh(self.game, (0,255,0),  MESH_WIDTH, MESH_HEIGHT, MESH_POS_X, MESH_POS_Y)
        
        
        
        sprites = self._pole, self._bboard, self._rim, self._netmesh
        self.image = pygame.sprite.Group(sprites)
        
        
        
    def _draw(self)-> None:
        
        for sprite in self.image:
            sprite._draw()
        
        
    def update(self)-> None:
        self._draw()
    
    def get_solids(self) -> 'pygame.Group':
        return pygame.sprite.Group(self._rim, self._bboard, self._pole)
    
    def get_mesh(self) -> 'pygame.Sprite':
        return self._netmesh
    
