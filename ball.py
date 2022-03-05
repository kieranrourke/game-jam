"""Ball class for space basketball"""

__date__ = '3/4/22'
__version__ = 'V0.4'
__author__ = 'Nucleus team'

import pygame

class Ball:
    def __init__(self, game: 'Game', planets: ['Planet'], ini_x: int, 
                 ini_y: int, size: int = 20) -> None: 
        """ Iniitiates a ball object with a size (also indicates mass). 
        No initial speed or acceleration, initial pos based on params.
        """
        #Color constant
        self._ORANGE = (250,131,32)
        #set size (Deafult 20)
        self._radius = size
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
        
        
        self.update()
        
    ##TODO: Add str, repr 
        
    ##Ideally, this is in a higher level class, like game/main
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
        self._draw()
        
    def get_mass(self) -> int:
        """ Returns the mass of the ball.
        """
        return self._radius
    
    def get_pos(self) -> 'pygame.Vector2':
        """ Returns the current position of the ball as a 2D vector.
        """
        return self._pos    
    
    def get_pos_tup(self) -> tuple[int, int]:
        """ Returns the current position of the ball as a tuple 
        in the form (x, y). Might remove later.
        """
        return (self._pos.x, self._pos.y)