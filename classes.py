# Constants for the window size
WIDTH, HEIGHT = 800, 600
VERTEX_RADIUS = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Commands:
    def add_edge():
        x, y = event.pos
        for i, vertex in enumerate(vertices):
            vx, vy = vertex
            if vx - VERTEX_RADIUS <= x <= vx + VERTEX_RADIUS:
                if vy - VERTEX_RADIUS <= y <= vy + VERTEX_RADIUS:
                    selected_vertecies.append(i)
                    if len(selected_vertecies) >= 2:
                        first_vertex = vertices[selected_vertecies[0]]
                        second_vertex = vertices[selected_vertecies[1]]
                        edge = [first_vertex, second_vertex]
                        if edge not in edges:
                            edges.append(edge)
                        selected_vertecies = []
                        return False
                    elif len(selected_vertecies) == 1:
                        edge_preview[0] = (vx, vy)
                        return True
                    
    def define_vertex(event):
        # Get position of cursor
        x, y = event.pos
        # If cursor position is in the screen dimensions
        if 0 <= x <= WIDTH and 0 <= y <= WIDTH:
            # Add a new vertex at the mouse click position
            return [x, y], RED
