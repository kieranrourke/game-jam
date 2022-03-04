"""Ball class for space basketball"""

__date__ = '3/4/22'
__version__ = 'V0.3'
__author__ = 'Alexandre Marques + Cade'

import pygame

class Ball:
    def __init__(self, ini_x: int, ini_y: int, size: int = 20) -> None: 
        """ Iniitiates a ball object with a size (also indicates mass). 
        No initial speed or acceleration, initial pos based on params.
        """
        #set size (Deafult 20)
        self._radius = size
        #set initial pos
        self._pos = pygame.Vector2(ini_x,ini_y)
        #set initial spd/accel to 0
        self._spd = pygame.Vector2(0,0)
        self._accel = pygame.Vector2(0,0)
        
    ##TODO: Add str, repr 
        
    def _update_spd(self) -> None:
        """ Updates speed based on current acceleration. 
        Should be called after acceleration calculations are done.
        """
        self._spd += self._accel
    
    def _sum_acceleration(self, planets: ['Planet']) -> 'pygame.Vector2':
        """ Returns the sum of the accelerations exerted on the ball by
        each planet in the level.
        """
        total_accel = Vector2() #0,0

        for planet in planets:
            #FIXME: Planet function name TBD
            total_accel += planet.force_applied(self.get_pos_tup(),
                                              self.get_mass())
        
        return total_accel
    
    def _update_vel(self, planets: ['Planet']) -> None:
        """ Updates velocity based on gravitational pull of other objects. 
        Should be called before each time the ball is moved.
        """
        #Updates accelaration
        self._accel += self.sum_accelerations(planets)
        _update_spd()
        
    def update_pos(self, planets: ['Planet']) -> None:
        """ Updates position based on speed of the ball (affected by planets). 
        Should be called on each game tick while ball is in the air.
        """        
        _update_vel()
        self._pos += self._pos 
        
    def get_mass() -> int:
        """ Returns the mass of the ball.
        """
        return self._radius
    
    def get_pos() -> 'pygame.Vector2':
        """ Returns the current position of the ball as a 2D vector.
        """
        return self._pos    
    
    def get_pos_tup() -> tuple[int, int]:
        """ Returns the current position of the ball as a tuple 
        in the form (x, y).
        """
        return (self._pos.x, self._pos.y)