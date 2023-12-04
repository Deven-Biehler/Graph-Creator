import pygame
from include import *

class Vertex:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.radius = VERTEX_RADIUS
        self.selected = False
        self.attached = False
        self.attached_edge = None
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
    
    def update(self, screen):
        self.draw(screen)
    
    def __repr__(self):
        return f"Vertex({self.position}, {self.color})"
    
    def __str__(self):
        return f"Vertex({self.position}, {self.color})"
    
    def __eq__(self, other):
        if self.position == other.position:
            return True
        else:
            return False
    
    def is_clicked(self, x, y):
        vx, vy = self.position
        if vx - self.radius <= x <= vx + self.radius:
            if vy - self.radius <= y <= vy + self.radius:
                return True
        else:
            return False
    
    def set_position(self, position):
        self.position = position
    
    def get_position(self):
        return self.position
    
    def set_color(self, color):
        self.color = color