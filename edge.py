import pygame
from include import *
from vertex import Vertex

class Edge:
    def __init__(self, start_vertex, end_vertex):
        self._start_vertex = start_vertex
        self._end_vertex = end_vertex
        self.color = BLUE
        self.width = 2
    
    def draw(self, screen, mouse_pos=None):
        if self._end_vertex is None:
            if mouse_pos is not None:
                pygame.draw.line(screen, self.color, self._start_vertex.position, mouse_pos, self.width)
        else:
            pygame.draw.line(screen, self.color, self._start_vertex.position, self._end_vertex.position, self.width)
    
    def update(self, screen):
        self.draw(screen)
    
    def __repr__(self):
        return f"Edge({self._start_vertex}, {self._end_vertex})"
    
    def __str__(self):
        return f"Edge({self._start_vertex}, {self._end_vertex})"
    
    def __eq__(self, other):
        if self._start_vertex == other._start_vertex and self._end_vertex == other._end_vertex:
            return True
        elif self._start_vertex == other._end_vertex and self._end_vertex == other._start_vertex:
            return True
        else:
            return False
    
    def set_start_vertex(self, vertex):
        self._start_vertex = vertex
    
    def set_end_vertex(self, vertex):
        self._end_vertex = vertex

    def get_start_vertex(self):
        return self._start_vertex
    
    def get_end_vertex(self):
        return self._end_vertex
