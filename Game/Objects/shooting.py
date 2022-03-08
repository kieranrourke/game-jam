import pygame
import math

class Shooting:
    def __init__(self, game, power_bar, arrow) -> None:
        self.game = game
        self.down_pos = tuple()
        self.up_pos = tuple()
        self.power_bar = power_bar 
        self.power_bar_copy = power_bar.copy()
        self.up_arrow = pygame.transform.rotate(arrow, 90)
        self.down_arrow = pygame.transform.rotate(arrow, -90)
        self.arrow = arrow
        self.arrow_copy = arrow.copy()
        self.distance = 0
        self.arrow_x_pos = 100
        self.arrow_y_pos = 100
        self.visible = False
        self._SENS = 0.05

    def calculate_force(self) -> 'pygame.Vector2':
        # The direction  of the shot is the norm of clicked_down - clicked_up  
        try:
            shot_vec = (pygame.Vector2(self.down_pos) - pygame.Vector2(self.up_pos))
        except ValueError:
            return pygame.Vector2(0,0)

        
        #Click with no movement should not shoot
        if shot_vec.magnitude() != 0:
            shot_dir = shot_vec.normalize()
            #Higher sensitiy means more power
            shot_mag = shot_vec.magnitude() * self._SENS
            return pygame.Vector2(shot_dir.x * shot_mag, shot_dir.y * shot_mag)
        else: 
            #No initial spd
            return pygame.Vector2(0,0)

    def set_down_pos(self, pos:tuple, ball_pos:tuple):
        self.down_pos = pos
        self.arrow_x_pos = ball_pos[0] 
        self.arrow_y_pos = ball_pos[1]
        self.visible = True

    def set_up_pos(self, pos:tuple):
        self.up_pos= pos
        self.calculate_force()
        self.visible = False
        
    def draw_arrow(self):
        self.game.draw(self.arrow_copy, self.arrow_x_pos, self.arrow_y_pos)

    def draw_progress_bar(self, x, y):
        self.game.draw(self.power_bar_copy, x, y) 

    def update_arrow(self):
        self.up_pos = self.game.MOUSE_POS
        self.distance = math.sqrt((self.down_pos[0] - self.up_pos[0])**2 + (self.down_pos[1] - self.up_pos[1])**2)
        direction_vector = pygame.math.Vector2(self.down_pos[0]-self.up_pos[0], self.down_pos[1]-self.up_pos[1])

        if direction_vector[1] != 0:
            angle = math.atan(direction_vector[0]/direction_vector[1])
        else:
            angle = 90 if direction_vector[0] > 0 else -90
            return

        if direction_vector[1] > 0:
            self.arrow_copy = pygame.transform.rotate(self.down_arrow, math.degrees(angle))
        else:
            self.arrow_copy = pygame.transform.rotate(self.up_arrow, math.degrees(angle))

        self.arrow.get_size()
        self.draw_arrow()

    def update_progress_bar(self):
        self.power_bar_copy = pygame.transform.scale(self.power_bar, (10, int(self.distance/2)))
        if self.arrow_x_pos > 150:
            self.draw_progress_bar(self.arrow_x_pos-100, self.arrow_y_pos)
        else:
            self.draw_progress_bar(self.arrow_x_pos+200,self.arrow_y_pos)

