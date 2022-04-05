"""Ball class for space basketball"""

__date__ = '3/5/22'
__version__ = 'V0.7'
__author__ = 'Nucleus team'

import pygame
import math

class Ball(pygame.sprite.Sprite):
    ##Eventually, should not need planets as a field
    def __init__(self, game: 'Game', sheet: 'SpriteSheet', 
                 ini_x: int, ini_y: int, util_folder_path, 
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
        #FIXME: Could possibly automate this array creation
        self._SHEET_OFFSETS = [(0,0),
                               (self._SIZE,0), 
                               (self._SIZE*2,0),
                               (0,self._SIZE),
                               (self._SIZE,self._SIZE), 
                               (self._SIZE*2,self._SIZE),
                               (0,self._SIZE*2),
                               (self._SIZE,self._SIZE*2)]
        self._cur_offset = 0
        self.image = self._sheet.image_at(pygame.Rect(
                          self._SHEET_OFFSETS[self._cur_offset], 
                          (self._SIZE, self._SIZE)))
        #Store animation fields
        self._ANIM_SPEED = 35 #Number of ticks between animations
        self._anim_tick = 0
        
        #set initial pos, spd, accel
        self._pos = pygame.Vector2(ini_x,ini_y)
        self._spd = pygame.Vector2(0,0)
        self._accel = pygame.Vector2(0,0)
        
        #Hitbox attributes. Mask prefered
        self.rect = pygame.Rect(tuple(self._pos), (self._SIZE, self._SIZE))
        self.radius = self._SIZE/2   
        
        #Set max spd/accel (absolute val. Set high to "uncap")
        self._MAX_SPD = 10
        self._MAX_ACCEL  = 1
        self._MIN_SPD_MAG  = 1 #Goes to 0 if below this spd
        #Does not have mvmnt initially
        self._stopped = True 
        
        #Store game screen
        self._game = game

        #Music
        self.util_folder_path = util_folder_path

        try:
            self.wall_hit_sound = pygame.mixer.Sound(self.util_folder_path+'wall_hit.wav')
            self.wall_hit_sound.set_volume(0.2)
            self.score_sound = pygame.mixer.Sound(self.util_folder_path+'score_sound.mp3')
            self.score_sound.set_volume(0.2)
        except pygame.error:
            self.wall_hit_sound = None
            self.score_sound = None
    
    ##Collision logic
    def _collide_circle(self, other):
        #print("Col check")
        return pygame.sprite.collide_circle(self, other)

    def _collide_rect(self, other):
        #print("Col check")
        return pygame.sprite.collide_rect(self, other)    
    
    #Highly cohesive rn
    def _check_collisions(self, planets: ['Planet'], net: 'Net') -> None:
        """"""
        #Hitbox update
        self.rect = pygame.Rect(tuple(self._pos), (self._SIZE, self._SIZE))
        
        #check planet collision:
        for planet in planets:
            if self._collide_circle(planet):
                self.rebound(planet)
                #Set spped to 0 if below min spd threshold
                if self._spd.magnitude() < self._MIN_SPD_MAG:
                    self.stop()                
        
        #check net collision TODO:
        for solid in net.get_solids():
            if self._collide_rect(solid):
                self.rebound(solid)

    
    def _set_amortization(self, other_mass: float) -> float:
        #For max amort: 
        #self mass needs to be MAX*CORREC times smaller than other
        #> MIN when self_mass > 
        BASE_AMORT = 1.2 #ball >= planet
        MAX_AMORT = 2 #vall << planet
        AMORT_CORRECTION = 3
        
        self_mass = self.get_mass()
        
        mass_factor = other_mass/(AMORT_CORRECTION*self_mass)
        
        if mass_factor <= BASE_AMORT:
            return BASE_AMORT
        
        return min(MAX_AMORT, mass_factor)
    
    def rebound(self, collision: 'pygame.Sprite') -> None:
        """Bounces ball back from collision point with amortised speed.
        Speed depends on mass difference between objects.
        """
        #Amortization factor, bigger it is, less speed on rebound (based on mass)
        amortize_factor = self._set_amortization(collision.get_mass())
        #Vector sub finds direction between 2 points (col -> pos)
        col_dir = (self.get_center() - collision.get_center()).normalize() #unit vec
        
        col_mag = self._spd.magnitude() / amortize_factor
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
            total_accel += planet.accel_applied(ball.get_center(), 
                                                ball.get_mass())
        
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
        if self._stopped:
            self._spd = pygame.Vector2(0,0)
        else:
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
        pass

    ##Updating methods
    def _update_pos(self, planets: ['Planet'], net) -> bool:
        """ Updates position based on speed of the ball (affected by planets). 
        Should be called on each game tick. 
        """   
        #Update accel (sum of forces) -> update spd -> update position
        self._set_accel(self._sum_acceleration(planets))
        self._set_spd(self._spd + self._accel)
        #Collision check overrides speed on rebounds: Could be useful to set to 0 later.
        scored = self._check_collisions(planets, net)
        self._pos += self._spd
        #Check if in net after any rebounds
        return self._collide_rect(net.get_mesh())
    
    def _update_image(self) -> None:
        """Update image of the sprite depending on 
        the sprite's annimation speed. Anim. spd. depends on ball spd(TODO)
        """
        if self._stopped != True:
            #Update sprite_sheet_location depending on anim_speed:
            #TODO: could make anim_speed depend on object speed somehow?
            self._anim_tick += 1
            if self._anim_tick == self._ANIM_SPEED:
                self._cur_offset += 1
                #Wrap back to first sprite at end of spritesheet
                if self._cur_offset == len(self._SHEET_OFFSETS):
                    self._cur_offset = 0              
                #Update image from spritesheet:
                self.image = self._sheet.image_at(pygame.Rect(
                                  self._SHEET_OFFSETS[self._cur_offset], 
                                  (self._SIZE, self._SIZE)))    
                
                self._anim_tick = 0    
        
    
    def _draw(self) -> None:
        """Draws the ball on the screen. Should be called on each game tick.
        """
        self._update_image()
       
        #Draw new sprite at new current loc
        self._game.screen.blit(self.image, (self._pos.x, 
                                            self._pos.y))   
        #pygame.draw.circle(self._game.screen, (255,255,255), 
                           #self.get_center(), self.radius)        
    
    def update(self, planets, net) -> bool:
        """ Updates the ball's state and displays it. 
        Should be called each game tick.
        """
        scored = self._update_pos(planets, net) 
        self._draw()
        if scored and self.score_sound is not None:
            self.score_sound.play()
        return scored
        
    ##Accessors    
    def get_mass(self) -> int:
        """ Returns the mass of the ball.
        """
        return math.pi * math.pow((self.radius), 2)   
    
    def get_pos(self) -> 'pygame.Vector2':
        """ Returns the current position of the ball as a 2D vector.
        """
        return self._pos    
    
    def get_pos_tup(self) -> tuple[int, int]:
        """ Returns the current position of the ball as a tuple 
        in the form (x, y). Might remove later.
        """
        return (self._pos.x, self._pos.y)
    
    def get_center(self) -> 'pygame.Vector2':
        """Returns the center of the image
        Returns:
            Vector2: center of the image in 2D vector format [x,y]
        """
        width, height = self.image.get_size()
        return pygame.Vector2(self._pos.x + width / 2, 
                              self._pos.y +  height / 2)   
    def is_stopped(self):
        return self._stopped    
    
    ##Mutators
    def stop(self):
        """Stops the ball's movement, and animation"""
        self._stopped = True
        
    def place_ball(self, x:int, y:int):
        """Places the ball in the level, initially with no motion"""
        self.stop()
        self._pos = pygame.Vector2(x, y)
    
    def shoot(self, ini_spd: 'pygame.Vector2'):
        """Shoots the ball by giving it an initial speed"""
        self._spd = ini_spd
        self._stopped = False
    
    def is_collision(self):
        if self._pos.x>self._game.xBound-self._SIZE:
           self.collision() 
        elif self._pos.x< self._SIZE:
           self.collision() 
        elif self._pos.y < self._SIZE:
           self.collision(vertical=True) 
        elif self._pos.y > self._game.yBound - self._SIZE:
           self.collision(vertical=True) 
    
    def collision(self, vertical=False):
        if self.wall_hit_sound is not None:
            self.wall_hit_sound.play()
        if vertical:
            self._spd = pygame.Vector2(self._spd[0], -self._spd[1])
        else:
            self._spd = pygame.Vector2(-self._spd[0], self._spd[1])