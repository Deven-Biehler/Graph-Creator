import pygame
import sys
from commands import Commands
from include import *
from edge import Edge
from vertex import Vertex

# Initialize Pygame
pygame.init()

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
pygame.display.set_caption("Graph Theorist's Sketchpad")

# Vertex information
vertices = []
selected_vertices = []
attached_vertex = None

# Edge information
edges = []  # list of Edge objects
drawing_line = False

# Game Modes
# Modes:
# vertex mode: key(Q)
# edge mode: key(W)
# move mode: key(E)
# delete mode: key(D)
game_mode = "vertex"

# Define colors for the modes
mode_colors = {
    "vertex": GREEN,
    "edge": YELLOW,
    "move": ORANGE,
    "delete": RED
}

options = {
    "directed": False,
}

# Sidebar information
sidebar_rect = pygame.Rect(WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
sidebar_font = pygame.font.SysFont(None, 20)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_mode == "vertex":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get definition of vertex
                position, color = Commands.define_vertex(event)
                # Create a new Vertex object
                vertex = Vertex(position, color)
                # Add vertex object to collection
                vertices.append(vertex)
        
        if game_mode == "edge":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get position of cursor
                x, y = event.pos

                # Check each vertex
                for vertex in vertices:
                    # If cursor is over this vertex
                    if vertex.is_clicked(x, y):
                        # Append the reference of the vertex to the selected vertex list
                        selected_vertices.append(vertex)
                        # if there are already 2 selected vertices
                        if len(selected_vertices) >= 2:
                            # Define an edge
                            edges[-1].set_end_vertex(selected_vertices[1])
                            edges[-1].get_start_vertex().set_color(RED)

                            # If the new edge does not already exist
                            if edge not in edges:
                                # Add new edge
                                edges.append(edge)

                            # Reset the selected vertex list
                            selected_vertices = []

                            # Reset the drawing_line user tag
                            drawing_line = False

                        # If this is the first selected vertex
                        elif len(selected_vertices) == 1:
                            if drawing_line:
                                edge.set_end_vertex(vertex)
                            else:
                                # Begin a preview of the new line
                                vertex = selected_vertices[0]
                                edge = Edge(vertex, None)
                                edge.set_start_vertex(vertex)
                                edges.append(edge)

                                # Start the drawing line user tag
                                drawing_line = True

        elif game_mode == "move":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for vertex in vertices:
                    if vertex.is_clicked(x, y):
                        attached_vertex = vertex
            elif event.type == pygame.MOUSEBUTTONUP:
                attached_vertex = None

        elif game_mode == "delete":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for vertex in vertices:
                    if vertex.is_clicked(x, y):
                        # Remove the vertex from the collection
                        vertices.remove(vertex)
                        # Remove any edges connected to the vertex
                        edges = [edge for edge in edges if edge.get_start_vertex() != vertex and edge.get_end_vertex() != vertex]
                        # Clear the selected vertices list if the deleted vertex was selected
                        if vertex in selected_vertices:
                            selected_vertices.remove(vertex)
                        break

        if event.type == pygame.MOUSEMOTION:
            if game_mode == "edge":
                if drawing_line:
                    edge = edges[-1]
            elif game_mode == "move":
                if attached_vertex is not None:
                    attached_vertex.set_position(event.pos)

        elif event.type == pygame.KEYDOWN and not drawing_line:
            if event.key == pygame.K_q:
                game_mode = "vertex"
            elif event.key == pygame.K_w:
                game_mode = "edge"
            elif event.key == pygame.K_e:
                game_mode = "move"
            elif event.key == pygame.K_d:
                game_mode = "delete"
            elif event.key == pygame.K_c:
                options["directed"] = not options["directed"]

    # Clear the screen
    screen.fill(WHITE)

    # Draw vertices
    for vertex in vertices:
        if vertex in selected_vertices:
            vertex.color = BLUE
            vertex.draw(screen)
        else:
            vertex.draw(screen)

    # Draw edges
    for edge in edges:
        if options["directed"]:
            draw_arrow=True
        else:
            draw_arrow=False
        edge.draw(screen, mouse_pos=pygame.mouse.get_pos(), draw_arrow=draw_arrow)
    

    # Draw mode indicator
    mode_indicator_rect = pygame.Rect(10, 10, 100, 30)
    pygame.draw.rect(screen, mode_colors[game_mode], mode_indicator_rect)
    mode_indicator_text = pygame.font.SysFont(None, 20).render(game_mode.capitalize(), True, BLACK)
    screen.blit(mode_indicator_text, (15, 15))


    # Draw sidebar
    pygame.draw.rect(screen, SIDEBAR_COLOR, sidebar_rect)
    sidebar_text = sidebar_font.render("Number of Vertices: {}".format(len(vertices)), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 10))
    sidebar_text = sidebar_font.render("Number of Edges: {}".format(len(edges)), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 40))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()