import matplotlib.pyplot as plt
import networkx as nx
import time

# Grafo ejemplo: nodos y pesos
graph_edges = [
    ('A', 'B', 4),
    ('A', 'C', 3),
    ('B', 'C', 1),
    ('B', 'D', 2),
    ('C', 'D', 4),
    ('D', 'E', 2),
    ('E', 'F', 6)
]

# Función para inicializar y mostrar el grafo con colores
def draw_graph(G, pos, selected_edges, title):
    plt.clf()
    edge_colors = ['blue' if (u, v) in selected_edges or (v, u) in selected_edges else 'gray' for u, v in G.edges()]
    
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color=edge_colors, node_size=1000, width=2)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(title)
    plt.pause(1)

# Algoritmo de Kruskal: mínimo o máximo
def kruskal(graph_edges, modo='min'):
    print(f"--- Ejecutando Kruskal ({'mínimo' if modo == 'min' else 'máximo'}) ---")

    # Crear grafo completo
    G = nx.Graph()
    G.add_weighted_edges_from(graph_edges)
    pos = nx.spring_layout(G)

    # Inicializar estructuras para el algoritmo
    parent = {}
    rank = {}

    # Funciones internas para conjuntos disjuntos
    def find(node):
        # Encuentra la raíz del conjunto con compresión de caminos
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(u, v):
        # Une dos conjuntos usando union by rank
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                if rank[root_u] == rank[root_v]:
                    rank[root_u] += 1

    # Inicializar conjuntos disjuntos
    for edge in graph_edges:
        u, v, _ = edge
        parent[u] = u
        parent[v] = v
        rank[u] = 0
        rank[v] = 0

    # Ordenar aristas (ascendente o descendente según el modo)
    sorted_edges = sorted(graph_edges, key=lambda x: x[2], reverse=(modo == 'max'))

    mst = []  # Árbol de expansión
    total_cost = 0

    draw_graph(G, pos, mst, "Inicio - Kruskal")

    for u, v, weight in sorted_edges:
        if find(u) != find(v):  # Si no forman un ciclo
            union(u, v)
            mst.append((u, v))
            total_cost += weight
            print(f"✔️ Agregado ({u}-{v}) con peso {weight}")
            draw_graph(G, pos, mst, f"Agregado ({u}-{v}) peso {weight}")
        else:
            print(f"❌ Ignorado ({u}-{v}) para evitar ciclo")

    print(f"\nCosto total del árbol {'mínimo' if modo == 'min' else 'máximo'}: {total_cost}")
    draw_graph(G, pos, mst, f"Árbol {'mínimo' if modo == 'min' else 'máximo'} completo")
    plt.show()

# Ejecutar ambos árboles
kruskal(graph_edges, modo='min')  # Árbol de mínimo costo
time.sleep(2)
kruskal(graph_edges, modo='max')  # Árbol de máximo costo