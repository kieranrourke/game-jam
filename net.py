import pygame
from planets import Planet
from game import Game      

class rectSprite(pygame.sprite.Sprite):
    def __init__(self, game, color, width, height, x_pos, y_pos) -> None:
        pygame.sprite.Sprite.__init__(self)    
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        #Only defines size, places hitbox top left
        self.rect = self.image.get_rect()
        #Moves box at image loc
        self.rect.x = x_pos
        self.rect.y = y_pos
    
    def _draw(self)-> None:
        self.game.screen.blit(self.image, (self.x_pos, self.y_pos))   

    def get_center(self) -> 'pygame.Vector2':
        return pygame.Vector2(self.rect.center)        

class Net():

    def __init__(self, game, hgt: int, planet: Planet, direction: str)-> None:
        #Attributes
        self.game = game
        self.planet = planet
        self.direction = direction

        # Size constants for each net 
        if planet.get_pos()[0] < self.game.xBound/2:
            POLE_WIDTH = 14
            POLE_HEIGHT = hgt

            BBOARD_WIDTH = 48
            BBOARD_HEIGHT = 60        


            RIM_WIDTH = 8 #(64-48) /2
            RIM_HEIGHT = 20   

            MESH_WIDTH = 48
            MESH_HEIGHT = 20        

            POLE_POS_X = self.planet.get_pos().x + (self.planet.get_size() / 2)
            POLE_POS_Y = self.planet.get_pos().y - POLE_HEIGHT

            BBOARD_POS_X = POLE_POS_X - 5
            BBOARD_POS_Y = POLE_POS_Y - BBOARD_HEIGHT + 5
            
            #Rim is actually 2 small rectangles on edge of mesh
            RIM_POS_X_1 = BBOARD_POS_X + BBOARD_WIDTH - 5
            RIM_POS_X_2 = BBOARD_POS_X + BBOARD_WIDTH - 5 + MESH_WIDTH + RIM_WIDTH
            RIM_POS_Y = BBOARD_POS_Y + BBOARD_HEIGHT - RIM_HEIGHT - 5

            MESH_POS_X = RIM_POS_X_1 + RIM_WIDTH 
            MESH_POS_Y = RIM_POS_Y 

        else:
            POLE_WIDTH = 14
            POLE_HEIGHT = hgt

            BBOARD_WIDTH = 48
            BBOARD_HEIGHT = 60        

            RIM_WIDTH = 8 #(64-48) /2
            RIM_HEIGHT = 20   

            MESH_WIDTH = 48
            MESH_HEIGHT = 20        

            POLE_POS_X = self.planet.get_pos().x + (self.planet.get_size() / 2)
            POLE_POS_Y = self.planet.get_pos().y - POLE_HEIGHT

            BBOARD_POS_X = POLE_POS_X - 20
            BBOARD_POS_Y = POLE_POS_Y - BBOARD_HEIGHT + 5
            
            #Rim is actually 2 small rectangles on edge of mesh
            RIM_POS_X_1 = BBOARD_POS_X-RIM_WIDTH 
            RIM_POS_X_2 = BBOARD_POS_X - MESH_WIDTH - RIM_WIDTH - RIM_WIDTH+7
            RIM_POS_Y = BBOARD_POS_Y + BBOARD_HEIGHT - RIM_HEIGHT - 5


            MESH_POS_X = RIM_POS_X_1 - RIM_WIDTH - MESH_WIDTH +7
            MESH_POS_Y = RIM_POS_Y


        # Net group

        self._pole = rectSprite(self.game, (255,255,255), 
                                POLE_WIDTH, POLE_HEIGHT, POLE_POS_X, POLE_POS_Y)

        self._bboard = rectSprite(self.game, (0,0,255), BBOARD_WIDTH , 
                                  BBOARD_HEIGHT, BBOARD_POS_X, BBOARD_POS_Y)

        self._rim1 = rectSprite(self.game, (255,0,0), RIM_WIDTH, 
                               RIM_HEIGHT, RIM_POS_X_1, RIM_POS_Y)
        self._rim2 = rectSprite(self.game, (255,0,0), RIM_WIDTH, 
                               RIM_HEIGHT, RIM_POS_X_2, RIM_POS_Y)        

        self._netmesh = rectSprite(self.game, (0,255,0),  MESH_WIDTH, 
                                   MESH_HEIGHT, MESH_POS_X, MESH_POS_Y)

        self._solids = pygame.sprite.Group(self._pole, self._bboard, 
                                           self._rim1, self._rim2)
        
        self.image = pygame.sprite.Group(self._netmesh, self._solids)



    def _draw(self)-> None:

        for sprite in self.image:
            sprite._draw()


    def update(self)-> None:
        self._draw()

    def get_solids(self) -> 'pygame.Group':
        return self._solids

    def get_mesh(self) -> 'pygame.Sprite':
        return self._netmesh

