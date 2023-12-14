import pygame
from include import *

class Vertex:
    def __init__(self, name, position, color):
        self.name = name
        self.label = ""
        self.position = position
        self.color = color
        self.radius = VERTEX_RADIUS
        self.selected = False
        self.attached = False
        self.attached_edges = []

    def draw(self, screen):
        if self.selected:
            pygame.draw.circle(screen, BLACK, self.position, self.radius + 2)
            pygame.draw.circle(screen, self.color, self.position, self.radius)
        else:
            pygame.draw.circle(screen, self.color, self.position, self.radius)
        
        font = pygame.font.Font(None, 20)
        label_text = font.render(self.label, True, BLACK)
        label_position = (self.position[0] - self.radius, self.position[1] - self.radius - 20)
        screen.blit(label_text, label_position)
    
    def update(self, screen):
        self.draw(screen)
    
    def __repr__(self):
        return f"Vertex({self.position}, {self.color})"
    
    def __str__(self):
        return f"Vertex({self.position}, {self.color})"
    
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