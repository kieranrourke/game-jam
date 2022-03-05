"""Ball class for space basketball"""

__date__ = '3/5/22'
__version__ = 'V0.6.2'
__author__ = 'Nucleus team'

import pygame
import math

class Ball(pygame.sprite.Sprite):
    ##Eventually, should not need planets as a field
    def __init__(self, game: 'Game', sheet: 'SpriteSheet', 
                 ini_x: int, ini_y: int, 
                 size: int = 32) -> None: 
        """ Initiates a ball object with initial speed or acceleration, 
        initial pos based on params.
        """
        #Superclass constructor
        pygame.sprite.Sprite.__init__(self)
        #size of 1 frame on the sheet
        #for varying ball size, might complicate spritesheet loads?
        self._SIZE = 32 
        
        #Initialise sprite sheet variables
        self._sheet = sheet
        self._SHEET_OFFSETS = [(0,0),(0,SIZE)]
        self.image = self._sheet.image_at(pygame.Rect(self._SHEET_OFFSETS[0], 
                                          (self._SIZE, self._SIZE)))
        self._cur_offset = 0 #might remove later
        
        #set initial pos, spd, accel
        self._pos = pygame.Vector2(ini_x,ini_y)
        self._spd = pygame.Vector2(0,0)
        self._accel = pygame.Vector2(0,0)
        
        #Hitbox attributes. Mask prefered
        self.rect = pygame.Rect(tuple(self._pos), (self._SIZE, self._SIZE))
        self._radius = self._SIZE/2
        self.mask = pygame.mask.from_surface(self.image)        
        
        #Set max spd/accel (absolute val. Set high to "uncap")
        self._MAX_SPD = 0.5
        self._MAX_ACCEL  = 0.05
        self._MIN_ACCEL  = 0.1 #UNIMPLEMENTED
        
        #Store game screen
        self._game = game
    
    ##Collision logic
    #Highly cohesive rn
    def _check_collisions(self, planets: ['Planet'], net: 'Net') -> None:
        """"""
        return
    
    #Might move to spaceJam class later
    def spritecollideany_mask(ball: 'Ball', 
                          group: 'SpriteGroup') -> 'Sprite':
        """Find all sprites that collide between two groups using their masks.
        Does not remove sprites from their groups.
        """
        #I wonder if collide_mask call should be converted to a bool statement
        return pygame.sprite.spritecollideany(ball, group, 
                                          pygame.sprite.collide_mask)

    def _radial_edge(self, direction: 'pygame.Vector2'):
        """Returns a point on the edge of the ball's radius
        going in a given normalized direction (length of 1)."""
        #Starts from center, displaces by the radius in the given direction
        return Vector2(self._pos.x+ self._radius*direction.x,
                       self._pos.y+ self._radius*direction.y)
    
    def rebound(self, collision: 'Sprite') -> None:
        """Bounces ball back from collision point with amortised speed.
        Speed depends on mass difference between objects (UNIMPLEMENTED). 
        Currently purely elastic."""
        #Amortization factor, remove later
        AMORTIZE_FAC = 1.5
        #Vector sub finds direction between 2 points (col -> pos)
        col_origin = pygame.Vector2(collision.get_pos())
        col_dir = self._pos - col_vector
        
        #TODO: Change to amortize depending on mass later
        col_mag = self._pos.mag / AMORTIZE_FAC
        #Normalize vector 
        col_dir = col_dir.normalize
        #Create spd vector using magnitude and direction. 
        col_spd = pygame.Vector2(col_mag * col_dir.x, col_mag * col_dir.y)
        
        #Set current spd to resultant collision spd
        self._set_spd(col_spd)
    
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

    ##Updating methods
    def _update_pos(self, planets: ['Planet']) -> None:
        """ Updates position based on speed of the ball (affected by planets). 
        Should be called on each game tick. 
        """   
        self._check_collisions(planets, net)
        #Update accel (sum of forces) -> update spd -> update position
        self._set_accel(self._sum_acceleration(planets))
        self._set_spd(self._spd + self._accel)
        self._pos += self._spd
    
    def _draw(self) -> None:
        """Draws the ball on the screen. Should be called on each game tick.
        """
        #Draws image centered on pos vector
        self._game.screen.blit(self.image, (self._pos.x -self._SIZE/2, 
                                            self._pos.y-self._SIZE/2))        
        
    def _update_mask(self):
        """Idk if this function needs to exit"""
        #overlap(s, offset)
    
    def update(self, planets, net) -> None:
        """ Updates the ball's state and displays it. 
        Should be called each game tick.
        """

        self._update_pos(planets)
        self._update_mask()       
        self._draw()
        
        ##Shows hitbox for debug
        #self.show_intended_mask() #DEBUG
        self.show_mask()        #DEBUG
        
    ##Accessors    
    def get_mass(self) -> int:
        """ Returns the mass of the ball.
        """
        return math.pi * math.pow((self._radius), 2)   
    
    def get_pos(self) -> 'pygame.Vector2':
        """ Returns the current position of the ball as a 2D vector.
        """
        return self._pos    
    
    def get_pos_tup(self) -> tuple[int, int]:
        """ Returns the current position of the ball as a tuple 
        in the form (x, y). Might remove later.
        """
        return (self._pos.x, self._pos.y)
    
    def get_img_center(self) -> 'pygame.Vector2':
        """Returns the center of the image
        Returns:
            Vector2: center of the image in 2D vector format [x,y]
        """
        width, height = self.image.get_size()
        return pygame.Vector2(self._pos.x + width / 2, 
                              self._pos.y +  height / 2)   
    
    ##Debug functions
    def show_intended_mask(self) -> None:
        #draw circle draws around the center of img. (shows hitbox)
        x_center, y_center = tuple(self.get_img_center())
        #Draws in black
        pygame.draw.circle(self._game.screen, (0,0,0), 
                           (x_center, y_center), self._SIZE)  

    def show_mask(self) -> None:
        #draw circle draws around the center of img. (shows hitbox)
        #Draws in white
        self.mask.to_surface(self._game.screen)       

