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
# edit mode: key(R)
game_mode = "vertex"

# Define colors for the modes
mode_colors = {
    "vertex": GREEN,
    "edge": YELLOW,
    "move": ORANGE,
    "delete": RED,
    "edit": BLUE
}

def is_bipartite(edges):
    color = {}  # Dictionary to store the color of each vertex

    def dfs(vertex, parent, visited):
        nonlocal color
        visited.add(vertex)

        for edge in edges:
            if edge.get_start_vertex() == vertex or edge.get_end_vertex() == vertex:
                neighbor = edge.get_end_vertex() if edge.get_start_vertex() == vertex else edge.get_start_vertex()
                if neighbor not in visited:
                    color[neighbor] = 1 - color[vertex]  # Assign a different color to the neighbor
                    if not dfs(neighbor, vertex, visited):
                        return False
                elif neighbor != parent and color[neighbor] == color[vertex]:
                    return False

        return True

    for edge in edges:
        start_vertex = edge.get_start_vertex()
        end_vertex = edge.get_end_vertex()

        if start_vertex not in color:
            color[start_vertex] = 0  # Assign color 0 to the start vertex
            if not dfs(start_vertex, None, set()):
                return False

        if end_vertex not in color:
            color[end_vertex] = 0  # Assign color 0 to the end vertex
            if not dfs(end_vertex, None, set()):
                return False

    return True


def find_bridges(edges):
    bridges = []

    def dfs(vertex, parent, visited, disc, low):
        nonlocal bridges
        visited.add(vertex)
        disc[vertex] = dfs.time
        low[vertex] = dfs.time
        dfs.time += 1

        for edge in edges:
            if edge.get_start_vertex() == vertex or edge.get_end_vertex() == vertex:
                neighbor = edge.get_end_vertex() if edge.get_start_vertex() == vertex else edge.get_start_vertex()
                if neighbor not in visited:
                    dfs(neighbor, vertex, visited, disc, low)
                    low[vertex] = min(low[vertex], low[neighbor])
                    if low[neighbor] > disc[vertex]:
                        bridges.append(edge)
                elif neighbor != parent:
                    low[vertex] = min(low[vertex], disc[neighbor])

    dfs.time = 0
    visited = set()
    disc = {}
    low = {}

    for edge in edges:
        start_vertex = edge.get_start_vertex()
        end_vertex = edge.get_end_vertex()

        if start_vertex not in visited:
            dfs(start_vertex, None, visited, disc, low)

        if end_vertex not in visited:
            dfs(end_vertex, None, visited, disc, low)

    return bridges


def detect_components():
    visited = set()  # Set to keep track of visited vertices
    components = []  # List to store the components

    for edge in edges:
        start_vertex = edge.get_start_vertex()
        end_vertex = edge.get_end_vertex()

        # Perform depth-first search from each unvisited vertex
        if start_vertex not in visited:
            component = set()  # Set to store the vertices in the component
            dfs(start_vertex, visited, component)
            components.append(component)

        # Perform depth-first search from each unvisited vertex
        if end_vertex not in visited:
            component = set()  # Set to store the vertices in the component
            dfs(end_vertex, visited, component)
            components.append(component)

    return components

def dfs(vertex, visited, component):
    visited.add(vertex)
    component.add(vertex)

    for edge in edges:
        if edge.get_start_vertex() == vertex:
            neighbor = edge.get_end_vertex()
            if neighbor not in visited:
                dfs(neighbor, visited, component)
        elif edge.get_end_vertex() == vertex:
            neighbor = edge.get_start_vertex()
            if neighbor not in visited:
                dfs(neighbor, visited, component)


def add_loops():
    for edge in edges:
        if edge.get_start_vertex() == edge.get_end_vertex():
            edge.isLoop = True

def add_vertex(position, color):
    # Get definition of vertex
    position, color = Commands.define_vertex(event)
    create_vertex(position, color)

def create_vertex(position, color):
    # Create a new Vertex object
    vertex = Vertex(len(vertices), position, color)
    # Add vertex object to collection
    vertices.append(vertex)

def remove_vertex(vertex):
    vertices.remove(vertex)
    # Remove any edges connected to the vertex
    for edge in vertex.attached_edges:
        remove_edge(edge)

def add_edge(event):
    x, y = event.pos
    # Check each vertex for a click
    for vertex in vertices:
        if vertex.is_clicked(x, y):
            # Finishing line
            if is_drawing_line():
                # set the final edge
                edges[-1].set_end_vertex(vertex)
                edges[-1].get_start_vertex().set_color(RED)

            # If this is the first selected vertex
            elif not is_drawing_line():
                create_edge(vertex, None)
                    

def create_edge(start_vertex, end_vertex):
    edge = Edge(len(edges), start_vertex, end_vertex)
    edges.append(edge)

def remove_edge(edge):
    edges.remove(edge)


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
sidebar_small_font = pygame.font.SysFont(None, 15)

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
                        remove_vertex(vertex)
                        break
                for edge in edges:
                    if edge.is_clicked(x, y):
                        remove_edge(edge)
                        break
        
        elif game_mode == "edit":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for vertex in vertices:
                    if vertex.is_clicked(x, y):
                        vertex.label = input("Enter a label for this vertex: ")
                        vertex.color = input("Enter a color for this vertex: ")

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
            elif event.key == pygame.K_r:
                game_mode = "edit"

    add_loops()

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

    # Clear previous information about verticies
    for vertex in vertices:
        vertex.attached = False
        vertex.attached_edges = []

    # Add information to verticies
    for edge in edges:
        edge.get_start_vertex().attached = True
        if edge.get_end_vertex() is not None:
            edge.get_end_vertex().attached = True
        edge.get_start_vertex().attached_edges.append(edge)
        if edge.get_end_vertex() is not None:
            edge.get_end_vertex().attached_edges.append(edge)
    

    # Gather Information for the sidebar

    # Draw sidebar
    pygame.draw.rect(screen, SIDEBAR_COLOR, sidebar_rect)
    sidebar_text = sidebar_font.render("Number of Vertices: {}".format(len(vertices)), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 10))
    sidebar_text = sidebar_font.render("Number of Edges: {}".format(len(edges)), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 40))
    sidebar_text = sidebar_font.render("Directed Mode: {}".format(DIRECTED_MODE), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 70))
    sidebar_text = sidebar_font.render("Total Degrees: {}".format(len(edges)*2), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 100))
    sidebar_text = sidebar_font.render("Total Components: {}".format(len(detect_components())), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 130))
    sidebar_text = sidebar_font.render("Total Bridges: {}".format(len(find_bridges(edges))), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 160))
    sidebar_text = sidebar_font.render("Bipartite: {}".format(is_bipartite(edges)), True, BLACK)
    screen.blit(sidebar_text, (WIDTH + 10, 190))

    for i, vertex in enumerate(vertices):
        degrees = len(vertex.attached_edges)
        sidebar_text = sidebar_small_font.render("Vertex {}, {}: Degrees: {}".format(vertex.name, vertex.label, degrees), True, BLACK)
        screen.blit(sidebar_text, (WIDTH + 10, 220 + (i * 10)))


    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()