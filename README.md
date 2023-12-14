The provided code is a Python script using the Pygame library to create a simple graph theory sketchpad. The sketchpad allows users to interactively create and manipulate vertices and edges in a graph. Here's a narrative explaining the features and how the routines are implemented:
Pygame Initialization and Window Creation:
The script begins by importing necessary modules, including Pygame, and initializing it. A window is created using pygame.display.set_mode(), and its caption is set. The window size is determined by constants like WIDTH, SIDEBAR_WIDTH, and HEIGHT.
## Graph Representation:
Vertices and edges are represented using the Vertex and Edge classes. Vertices have positions, colors, and labels, while edges have start and end vertices.
## Game Modes:
There are different modes in which the sketchpad operates:

Vertex Mode (Q): Allows the user to add vertices to the graph.
Edge Mode (W): Enables the user to add edges between vertices.
Move Mode (E): Allows for moving vertices around.
Delete Mode (D): Enables the deletion of vertices and edges.
Edit Mode (R): Allows the user to edit vertex labels and colors.
## Graph Algorithms:
The script implements several graph algorithms:

Bipartite Check (is_bipartite function):
The is_bipartite function determines whether the graph is bipartite. It utilizes a depth-first search (DFS) approach to traverse the graph, assigning colors to vertices and checking for conflicts. The function initializes a color dictionary to store the color of each vertex. It then iterates through the edges and performs DFS on unvisited vertices.
This function ensures that adjacent vertices in the graph are assigned different colors. If a conflict is encountered during the DFS traversal, the graph is not bipartite, and the function returns False. Otherwise, it returns True.

Bridges Detection (find_bridges function):
The find_bridges function identifies bridges in the graph using Tarjan's algorithm. It utilizes DFS to assign discovery and low values to vertices and identifies bridges based on the comparison of these values.
The find_bridges function keeps track of discovered and low values for each vertex during the DFS traversal. It identifies edges where the low value of the adjacent vertex is greater than the discovery value of the current vertex, indicating a bridge.

Connected Components (detect_components function):
The detect_components function finds connected components in the graph using DFS. It iterates through edges, performs DFS from unvisited vertices, and adds the discovered components to a list.
The detect_components function uses DFS to traverse the graph, identifying connected components by adding vertices to sets. The discovered components are then appended to the components list.

These graph algorithms provide insights into the properties and structure of the graph, enriching the user's understanding of its characteristics.
## Vertex and Edge Manipulation:
Vertex Addition:
In the vertex mode (activated by pressing the 'Q' key), users can add vertices to the graph by clicking on the Pygame window. The add_vertex() function is triggered upon a mouse click event, and it calls the create_vertex() function, passing the mouse position and a default color (BLACK) as arguments.

The create_vertex() function instantiates a new Vertex object with a unique identifier, given position, and color. This vertex is then appended to the vertices list, forming a collection of all vertices in the graph.

Edge Addition:
In the edge mode (activated by pressing the 'W' key), users can add edges between existing vertices by clicking on them. The add_edge() function handles this interaction. It checks if the user has clicked on a vertex and, if so, either starts a new edge or completes the currently drawing edge.

If a vertex is clicked and no edge is currently being drawn, a new edge is initiated using the create_edge() function, with the clicked vertex as the starting point.

The create_edge() function creates a new Edge object, assigns it a unique identifier, and appends it to the edges list.

Vertex and Edge Removal:
In the delete mode (activated by pressing the 'D' key), users can remove vertices and edges by clicking on them. The remove_vertex() function removes a selected vertex and all edges connected to it.
The remove_edge() function removes a specified edge from the edges list.
In the edit mode (activated by pressing the 'R' key), users can edit the labels and colors of vertices. The edit_mode() function checks if a vertex is clicked, and if so, prompts the user for a new label and color.
## Drawing and Display:
The main game loop continuously listens for user input, updates the display, and handles events such as mouse clicks and key presses. The display includes drawing vertices, edges, and a sidebar with information about the graph's properties.
## Sidebar Information:
The sidebar displays information about the graph, including the number of vertices and edges, directed mode, total degrees, total components, total bridges, and whether the graph is bipartite.
This information comes directly from the graph algorithms.
## Additional Notes:
DIRECTED_MODE is a global variable that toggles between directed and undirected edge modes.
The script uses recursive depth-first search for various graph algorithms.
Overall, this script serves as an interactive tool for graph theory exploration, allowing users to visualize and manipulate graphs while providing information about their properties.
