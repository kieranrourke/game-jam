"""Ball class for space basketball"""

__date__ = '3/5/22'
__version__ = 'V0.6.1'
__author__ = 'Nucleus team'

import pygame
import math

class Ball(pygame.sprite.Sprite):
    ##Eventually, should not need planets as a field
    def __init__(self, game: 'Game', sheet: 'SpriteSheet', planets: ['Planet'], 
                 ini_x: int, ini_y: int, 
                 size: int = 32) -> None: 
        """ Initiates a ball object with initial speed or acceleration, 
        initial pos based on params.
        """
        #Superclass constructor
        pygame.sprite.Sprite.__init__(self)
        #size of 1 frame on the sheet
        #for varying ball size, might complicate spritesheet loads?
        SIZE = 32 
        
        #Color constant (Remove later)
        self._ORANGE = (250,131,32)
        
        #Initialise sprite sheet variables
        self._sheet = sheet
        self._SHEET_OFFSETS = [(0,0),(0,SIZE)]
        self.image = self._sheet.image_at((self._SHEET_OFFSETS[0]), 
                                          (SIZE, SIZE)) 
        self._cur_offset = 0 #might remove later
        
        #Hitbox attributes. Mask prefered
        self.rect = (SIZE, SIZE)
        self._radius = SIZE/2
        self.mask = pygame.mask.from_surface(self.image)
        
        #set initial pos, spd, accel
        self._pos = pygame.Vector2(ini_x,ini_y)
        self._spd = pygame.Vector2(0,0)
        self._accel = pygame.Vector2(0,0)
        
        #Set max spd/accel (absolute val. Set high to "uncap")
        self._MAX_SPD = 3.5
        self._MAX_ACCEL  = 1
        
        #Store planets
        self._planets = planets
        #Store game screen
        self._game = game
    
    ##Might move to spaceJam class soon
    def groupcollide_mask(group1: 'SpriteGroup', 
                          group2: 'SpriteGroup') -> 'pygame.Sprite_dict':
        """Find all sprites that collide between two groups using their masks.
        Does not remove sprites from their groups.
        """
        #I wonder if collide_mask call should be converted to a bool statement
        return pygame.sprite.groupcollide(self, group, False, False, 
                                        pygame.sprite.collide_mask)
    
    def _radial_edge(self, direction: 'pygame.Vector2'):
        """Returns a point on the edge of the ball's radius
        going in a given normalized direction (length of 1)."""
        #Starts from center, displaces by the radius in the given direction
        return Vector2(self._pos.x+ self._radius*direction.x,
                       self._pos.y+ self._radius*direction.y)
    
    def rebound(self, collision: Tuple[int, int]) -> None:
        """Bounces ball back from collision point with amortised speed.
        Speed depends on mass difference between objects (UNIMPLEMENTED). 
        Currently purely elastic."""
        #Amortization factor, remove later
        AMORTIZE_FAC = 1.5
        #Vector sub finds direction between 2 points (col -> pos)
        col_vector = pygame.Vector2(collision)
        col_dir = self._pos - col_vector
        
        #TODO: Change to amortize depending on mass later
        col_mag = self._pos.mag / AMORTIZE_FAC
        #Normalize vector 
        col_dir = col_dir.normalize
        #Create spd vector using magnitude and direction. 
        col_spd = pygame.Vector2(col_mag * col_dir.x, col_mag * col_dir.y)
        
        #Set current spd to resultant collision spd
        self._set_spd(col_spd)
    
    ##Might move to spaceJam class
    def _sum_acceleration(ball: 'Ball', planets: ['Planet']) -> 'pygame.Vector2':
        """ Returns the sum of the accelerations exerted on the ball by
        each planet in the level.
        """
        total_accel = pygame.Vector2() #0,0
    
        for planet in planets:
            total_accel += planet.accel_applied(ball.get_pos(), ball.get_mass())
        
        return total_accel
    
    def _set_accel(self, new_accel: 'pygame.Vector2'):
        """Sets acceleration within bounds defined by _MAX_ACCEL.
        """
        #0->x, 1 ->y. Sets for both cartesian coordinates
        for i in range(0,2):
            if new_accel[i] < -self._MAX_ACCEL:
                #below -max, set to -max
                self._accel[i] = -self._MAX_ACCEL
            elif new_accel[i] > self._MAX_ACCEL:
                #Above max, set to max
                self._accel[i] = self._MAX_ACCEL
            else:
                #Within bounds, can set to given val
                self._accel[i] = new_accel[i]
        
    def _set_spd(self, new_spd: 'pygame.Vector2'):
        """Sets speed within bounds defined by _MAX_SPD.
        """    
        #0->x, 1 ->y. Sets for both cartesian coordinates
        for i in range(0,2):
            if new_spd[i] < -self._MAX_SPD:
                #below -max, set to -max
                self._spd[i] = -self._MAX_SPD
            elif new_spd[i] > self._MAX_SPD:
                #Above max, set to max
                self._spd[i] = self._MAX_SPD
            else:
                #Within bounds, can set to given val
                self._spd[i] = new_spd[i]     
                
    def _set_pos(self, new_pos: 'pygame.Vector2'):
        """Unsure if we'll bind it in the window, or if we'll cause a reset. 
        TBD if we need this, keeping this here to remember it."""
        raise NotImplementedError("_set_pos is not implemented yet")
    
    def _update_pos(self, accel:'pygame.Vector2') -> None:
        """ Updates position based on speed of the ball (affected by planets). 
        Should be called on each game tick. 
        """   
        #Update accel (sum of forces) -> update spd -> update position
        self._set_accel(accel)
        self._set_spd(self._spd + self._accel)
        self._pos += self._spd
    
    def _draw(self) -> None:
        """Draws the ball on the screen. Should be called on each game tick.
        """
        ##With a few modifications, can use this to have the ball be an img
        #self.game.screen.blit(self.image, (self.x_pos, self.y_pos))        
        pygame.draw.circle(self._game.screen, self._ORANGE, self._pos, self._radius)
        
    def update(self) -> None:
        """ Updates the ball's state and displays it. 
        Should be called each game tick.
        """
        self._update_pos(self._sum_acceleration(self._planets))
        #TODO: Add a sprite sheet updater
        self._draw()
        
    def get_mass(self) -> int:
        """ Returns the mass of the ball.
        """
        return math.pi * math.pow((self._radius/2), 2)
    
    def get_pos(self) -> 'pygame.Vector2':
        """ Returns the current position of the ball as a 2D vector.
        """
        return self._pos    
    
    def get_pos_tup(self) -> tuple[int, int]:
        """ Returns the current position of the ball as a tuple 
        in the form (x, y). Might remove later.
        """
        return (self._pos.x, self._pos.y)