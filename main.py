import networkx as nx
import matplotlib.pyplot as plt
from modelos.vertice import Vertice

from modelos.grafo import Grafo

# === Crear y poblar el grafo ===

g = Grafo()

def generateBasicGraph():
    g.add_edge('A', 'B', 2)
    g.add_edge('B', 'C', 3)
    g.add_edge('C', 'D', 1)
    g.add_edge('D', 'E', 4)
    g.add_edge('E', 'F', 2)
    g.add_edge('B', 'G', 5)
    g.add_edge('G', 'H', 2)
    g.add_edge('D', 'B', 1)  # Ejemplo de arista hacia atrás


def generateAdvancedGraph():
    # Conexiones principales (una especie de “espina dorsal”)
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 8)
    g.add_edge('C', 'E', 10)
    g.add_edge('D', 'E', 2)
    g.add_edge('D', 'F', 6)
    g.add_edge('E', 'F', 2)
    g.add_edge('F', 'G', 3)

    # Caminos alternativos y retornos
    g.add_edge('B', 'C', 1)     # Atajo entre B y C
    g.add_edge('E', 'B', 3)     # Retorno hacia B
    g.add_edge('F', 'C', 4)     # Retorno medio
    g.add_edge('G', 'H', 1)
    g.add_edge('H', 'I', 2)
    g.add_edge('I', 'J', 4)
    g.add_edge('H', 'F', 1)     # Retroalimentación hacia F
    g.add_edge('J', 'G', 2)     # Cierre de ciclo G-H-I-J-G

    # Camino largo con costo bajo
    g.add_edge('A', 'I', 15)

    # Camino alternativo con peso más alto
    g.add_edge('C', 'H', 12)

def generateClassExampleGraph_Mar_Jue():
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'E', 8)
    g.add_edge('A', 'F', 4)
    g.add_edge('B', 'C', 3)
    g.add_edge('B', 'D', 8)
    g.add_edge('C', 'G', 1)
    g.add_edge('D', 'G', 7)
    g.add_edge('E', 'F', 12)
    g.add_edge('F', 'A', 4)
    g.add_edge('F', 'D', 2)
    g.add_edge('G', 'H', 6)
    g.add_edge('H', 'F', 5)

def generateClassExampleGraph_Jue_Vie():
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'D', 5)
    g.add_edge('B', 'D', 4)
    g.add_edge('B', 'F', -1)
    g.add_edge('B', 'C', 4)
    g.add_edge('C', 'B', 4)
    g.add_edge('C', 'D', 5)
    g.add_edge('C', 'E', 8)
    g.add_edge('D', 'A', 5)
    g.add_edge('D', 'C', 5)
    g.add_edge('D', 'E', 1)
    g.add_edge('E', 'C', 8)
    g.add_edge('F', 'C', 7)

#generateBasicGraph()
#generateAdvancedGraph()
#generateClassExampleGraph_Jue_Vie()
generateClassExampleGraph_Mar_Jue()

# === Convertir a networkx para visualizar ===

G_nx = nx.DiGraph()  # Usa DiGraph para grafo dirigido (puedes usar nx.Graph() si no lo es)

for v_id, vertex in g.lista_vertices.items():
    for neighbor, weight in vertex.get_connections().items():
        G_nx.add_edge(v_id, neighbor, weight=weight)

# === Dibujar el grafo ===

pos = nx.spring_layout(G_nx, seed=42)
edge_labels = nx.get_edge_attributes(G_nx, 'weight')

plt.figure(figsize=(8, 6))
nx.draw(G_nx, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=12, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=edge_labels, font_color='red')
plt.title("Visualización del Grafo con NetworkX", fontsize=14)
plt.show()