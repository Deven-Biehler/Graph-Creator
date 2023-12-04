import pygame
import sys
from classes import Commands
from classes import WIDTH, HEIGHT, VERTEX_RADIUS, WHITE, BLACK, BLUE

# Initialize Pygame
pygame.init()

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Theorist's Sketchpad")

# Vertex information
vertices = []
vertex_colors = []
selected_vertecies = []
attached_vertex = None

# Edge information
edges = [] # list of [start_pose, end_pose]
edge_preview = [(), ()]
drawing_line = False
EDGE_WIDTH = 2

# Game Modes
# Modes:
# vertex mode: key(Q)
# edge mode: key(W)
# move mode: key(E)
game_mode = "vertex"

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode == "vertex":
                # Get defenition of vertex
                position, color = Commands.define_vertex(event)
                # Add vertex defentitions to collection
                vertices.append(position)
                vertex_colors.append(color)
                
            if game_mode == "edge":
                # Get position of cursor
                x, y = event.pos

                # Check each vertex
                for i, vertex in enumerate(vertices):
                    # unpack coordinants of vertex
                    vx, vy = vertex

                    # If cursor is over this vertex
                    if vx - VERTEX_RADIUS <= x <= vx + VERTEX_RADIUS:
                        if vy - VERTEX_RADIUS <= y <= vy + VERTEX_RADIUS:
                            # Append the index of the vertex to the selected vertex list
                            selected_vertecies.append(i)
                            # if there is already 2 selected vertecies
                            if len(selected_vertecies) >= 2:
                                # Define an edge
                                first_vertex = vertices[selected_vertecies[0]]
                                second_vertex = vertices[selected_vertecies[1]]
                                edge = [first_vertex, second_vertex]
                                
                                # If the new edge does not already exist
                                if edge not in edges:
                                    # Add new edge
                                    edges.append(edge)
                                
                                # reset the selected vertex list
                                selected_vertecies = []
                                
                                # Reset the drawing_line user tag
                                drawing_line = False

                            # If this is the first selected vertex
                            elif len(selected_vertecies) == 1:
                                # Begin a preview of the new line
                                edge_preview[0] = (vx, vy)
                                
                                # Start the drawing line user tag
                                drawing_line = True
            if game_mode == "move":
                x, y = event.pos
                for i, vertex in enumerate(vertices):
                    vx, vy = vertex
                    if vx - VERTEX_RADIUS <= x <= vx + VERTEX_RADIUS:
                        if vy - VERTEX_RADIUS <= y <= vy + VERTEX_RADIUS:
                            if attached_vertex == None:
                                attached_vertex = vertex
                            else:
                                attached_vertex = None


        elif event.type == pygame.MOUSEMOTION:
            if game_mode == "edge":
                edge_preview[1] = event.pos
            if game_mode == "mode":
                if attached_vertex != None:
                    x, y = event.pose
                    attached_vertex[0] = x
                    attached_vertex[1] = y

        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_mode = "vertex"
            if event.key == pygame.K_w:
                game_mode = "edge"
            if event.key == pygame.K_e:
                game_mode = "move"

            

    # Clear the screen
    screen.fill(WHITE)

    # Draw vertices
    for i, vertex in enumerate(vertices):
        x, y = vertex
        if i in selected_vertecies:
            pygame.draw.circle(screen, BLUE, (x, y), VERTEX_RADIUS)
        else:
            pygame.draw.circle(screen, vertex_colors[i], (x, y), VERTEX_RADIUS)

    # Draw line preview
    if drawing_line:
        pygame.draw.line(screen, BLACK, edge_preview[0], edge_preview[1], EDGE_WIDTH)
    for i, edge in enumerate(edges):
        pygame.draw.line(screen, BLACK, edge[0], edge[1], EDGE_WIDTH)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()