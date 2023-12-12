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

def add_vertex(position, color):
    # Get definition of vertex
    position, color = Commands.define_vertex(event)
    create_vertex(position, color)

def create_vertex(position, color):
    # Create a new Vertex object
    vertex = Vertex(len(vertices), position, color)
    # Add vertex object to collection
    vertices.append(vertex)

def add_edge(event):
    x, y = event.pos
    # Check each vertex for a click
    for vertex in vertices:
        if vertex.is_clicked(x, y):
            # Append the reference of the vertex to the selected vertex list
            selected_vertices.append(vertex)
            vertex.selected = True
            # if there are already 2 selected vertices
            if len(selected_vertices) >= 2:
                # Define an edge
                edges[-1].set_end_vertex(selected_vertices[1])
                edges[-1].get_start_vertex().set_color(RED)

                # Reset the selected vertex list
                while selected_vertices != []:
                    selected_vertices.pop().selected = False

            # If this is the first selected vertex
            elif len(selected_vertices) == 1:
                if is_drawing_line():
                    edge.set_end_vertex(vertex)
                else:
                    create_edge(selected_vertices[0], None)


def create_edge(start_vertex, end_vertex):
    edge = Edge(len(edges), start_vertex, end_vertex)
    edges.append(edge)


def is_drawing_line():
    if len(edges) == 0:
        return False
    if edges[-1].get_end_vertex() is None:
        return True
    else:
        return False

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
                add_vertex(event.pos, BLACK)
        
        if game_mode == "edge":
            if event.type == pygame.MOUSEBUTTONDOWN:
                add_edge(event)

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

        if event.type == pygame.MOUSEMOTION:
            if game_mode == "edge":
                if is_drawing_line():
                    edge = edges[-1]
            elif game_mode == "move":
                if attached_vertex is not None:
                    attached_vertex.set_position(event.pos)

        elif event.type == pygame.KEYDOWN and not is_drawing_line():
            if event.key == pygame.K_q:
                game_mode = "vertex"
            elif event.key == pygame.K_w:
                game_mode = "edge"
            elif event.key == pygame.K_e:
                game_mode = "move"
            elif event.key == pygame.K_d:
                game_mode = "delete"
            elif event.key == pygame.K_c:
                DIRECTED_MODE = not DIRECTED_MODE

    # Clear the screen
    screen.fill(WHITE)

    # Draw vertices
    for vertex in vertices:
        vertex.update(screen)


    # Draw edges
    for edge in edges:
        edge.draw(screen, mouse_pos=pygame.mouse.get_pos(), draw_arrow=DIRECTED_MODE)
    

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