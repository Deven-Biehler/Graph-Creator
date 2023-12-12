import pygame
from include import *
from vertex import Vertex
import math

class Edge:
    def __init__(self, name, start_vertex, end_vertex):
        self.name = name
        self._start_vertex = start_vertex
        self._end_vertex = end_vertex
        self.color = BLUE
        self.width = 2
        self.isLoop = False
    
    def draw(self, screen, mouse_pos=None, draw_arrow=DIRECTED_MODE):
        if self.isLoop:
            control_point = (60, 60)
            self._draw_curved_line(screen, self.color, self._start_vertex.position, control_point)
            if draw_arrow:
                arrow_pos = [
                    (self._start_vertex.position[0] + 10 + VERTEX_RADIUS, self._end_vertex.position[1] + 5),
                    (self._start_vertex.position[0] + VERTEX_RADIUS, self._end_vertex.position[1]),
                    (self._start_vertex.position[0] + 10 + VERTEX_RADIUS, self._end_vertex.position[1] - 5)
                ]
                pygame.draw.polygon(screen, self.color, arrow_pos)
        else:
            if self._end_vertex is None:
                if mouse_pos is not None:
                    pygame.draw.line(screen, self.color, self._start_vertex.position, mouse_pos, self.width)
                    if draw_arrow:
                        arrow_pos = self._calculate_arrow_position(self._start_vertex.position, mouse_pos)
                        pygame.draw.polygon(screen, self.color, arrow_pos)
            else:
                pygame.draw.line(screen, self.color, self._start_vertex.position, self._end_vertex.position, self.width)
                if draw_arrow:
                    arrow_pos = self._calculate_arrow_position(self._start_vertex.position, self._end_vertex.position)
                    pygame.draw.polygon(screen, self.color, arrow_pos)

    def _calculate_arrow_position(self, start_pos, end_pos):
        arrow_length = 10
        arrow_angle = 0.4
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        angle = math.atan2(dy, dx)
        arrow_pos = [
            (end_pos[0] - arrow_length * math.cos(angle - arrow_angle), end_pos[1] - arrow_length * math.sin(angle - arrow_angle)),
            (end_pos[0], end_pos[1]),
            (end_pos[0] - arrow_length * math.cos(angle + arrow_angle), end_pos[1] - arrow_length * math.sin(angle + arrow_angle))
        ]
        return arrow_pos
    
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
        
    def is_clicked(self, x, y):
        if self._end_vertex is None:
            return False
        
        start_x, start_y = self._start_vertex.position
        end_x, end_y = self._end_vertex.position
        
        # Calculate the distance between the click position and the line segment
        distance = abs((end_y - start_y) * x - (end_x - start_x) * y + end_x * start_y - end_y * start_x) / math.sqrt((end_y - start_y) ** 2 + (end_x - start_x) ** 2)
        
        # Check if the distance is within a threshold (e.g., 5 pixels)
        if distance <= 5:
            return True
        else:
            return False
    
    def set_start_vertex(self, vertex):
        self._start_vertex = vertex
        vertex.attached_edges.append(self)
    
    def set_end_vertex(self, vertex):
        self._end_vertex = vertex

    def get_start_vertex(self):
        return self._start_vertex
    
    def get_end_vertex(self):
        return self._end_vertex
    
    def _draw_curved_line(self, surface, color, start, control_point):
        if control_point[0] > 0 and control_point[1] > 0:
            pygame.draw.arc(surface, color, [start[0], start[1], control_point[0], control_point[1]], 5.3*math.pi/6, 2*math.pi/3.3)
        


