"""Ball class for space basketball"""

__date__ = '3/4/22'
__version__ = 'V0.1'
__author__ = 'Alexandre Marques + Cade'

import pygame

class Ball:
    def __init__(self, ini_x: int, ini_y: int): 
        """ Iniitiates a ball object with a size (also indicates mass). 
        No initial speed or acceleration, initial pos based on params.
        """
        #set initial pos
        self._pos = pygame.Vector2(ini_x,ini_y)
        #set initial spd/accel to 0
        self._spd = pygame.Vector2(0,0)
        self._accel = pygame.Vector2(0,0)
        
    def _update_spd(self) -> None:
        """ Updates speed based on current acceleration. 
        Should be called after acceleration calculations are done.
        """
        self._spd += self._accel
    
    def _update_vel(self, planets: ['Planet']) -> None:
        """ Updates velocity based on gravitational pull of other objects. 
        Should be called before each time the ball is moved.
        """
        #Insert acceleration update logic here
        _update_spd()
        
    def update_pos(self, planets: ['Planet']) -> None:
        """ Updates position based on speed of the ball (affected by planets). 
        Should be called on each game tick while ball is in the air.
        """        
        _update_vel()
        self._pos += self._pos 