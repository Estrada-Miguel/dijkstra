import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Función para verificar si una matriz es simétrica
def es_matriz_simetrica(matriz):
    return all(matriz[i][j] == matriz[j][i] for i in range(len(matriz)) for j in range(len(matriz[0])))


# Función para generar un grafo a partir de una matriz y nodos
def generar_grafo(matriz, nodos):
    G = nx.Graph()
    simetrica = es_matriz_simetrica(matriz)
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            # Solo agregar aristas si la matriz es simétrica o si i < j
            if matriz[i][j] != 0 and (simetrica or i < j):
                G.add_edge(nodos[i], nodos[j], weight=matriz[i][j])
    return G


# Función para dibujar el grafo
def dibujar_grafo(grafo, ax):
    pos = nx.spring_layout(grafo, seed=42)
    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_nodes(grafo, pos, node_size=700, ax=ax)
    nx.draw_networkx_edges(grafo, pos, ax=ax)
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels, ax=ax)
    nx.draw_networkx_labels(grafo, pos, font_size=10, ax=ax)


# Función para encontrar la ruta más corta en el grafo
def encontrar_ruta_mas_corta(grafo, inicio, fin):
    if inicio not in grafo.nodes or fin not in grafo.nodes:
        raise ValueError("Alguno de los nodos escritos no se encuentra en el grafo")

    try:
        return nx.shortest_path(grafo, source=inicio, target=fin, weight='weight')
    except nx.NetworkXNoPath:
        raise ValueError("No hay ruta entre los nodos especificados")


# Función para dibujar la ruta más corta en el grafo
def dibujar_ruta_mas_corta(grafo, ruta, ax):
    pos = nx.spring_layout(grafo, seed=42)
    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_nodes(grafo, pos, node_size=700, ax=ax)
    nx.draw_networkx_edges(grafo, pos, ax=ax)
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels, ax=ax)
    nx.draw_networkx_labels(grafo, pos, font_size=10, ax=ax)
    ruta_edges = [(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)]
    nx.draw_networkx_edges(grafo, pos, edgelist=ruta_edges, edge_color='r', width=2, ax=ax)


# Función llamada cuando se presiona el botón "Buscar Ruta"
def on_button_click():
    inicio = entry_inicio.get().upper()
    fin = entry_fin.get().upper()

    try:
        ruta_corta = encontrar_ruta_mas_corta(grafo, inicio, fin)

        # Crear una nueva ventana para el grafo con la ruta más corta
        ventana_ruta_corta = tk.Toplevel(root)
        ventana_ruta_corta.title("Ruta Más Corta")

        fig, ax = plt.subplots(figsize=(8, 6))
        dibujar_ruta_mas_corta(grafo, ruta_corta, ax)

        # Incorporar la figura en la nueva ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana_ruta_corta)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        # Agregar el botón "Salir" en la nueva ventana
        button_salir = ttk.Button(ventana_ruta_corta, text="Salir", command=ventana_ruta_corta.destroy)
        button_salir.pack()

    except ValueError as e:
        messagebox.showerror("Error", str(e))


# Función llamada cuando se presiona el botón "Salir" en la interfaz principal
def salir():
    mensaje_despedida = "Muchas gracias por usar nuestro servicio"
    messagebox.showinfo("Despedida", mensaje_despedida)
    root.destroy()


# Nueva matriz de adyacencia del grafo
matriz = [
    [0, 6, 2, 3, 4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 3, 0, 7, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 6, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 2, 6, 1, 0],
    [0, 0, 0, 0, 0, 2, 0, 3, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 2, 0, 1, 0, 8, 0, 9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

nodos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Generar el grafo
grafo = generar_grafo(matriz, nodos)

# Crear la interfaz principal
root = tk.Tk()
root.title("Ruta Más Corta")

# Dibujar el primer grafo en la interfaz principal
fig, ax = plt.subplots(figsize=(8, 6))
dibujar_grafo(grafo, ax)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Interfaz para ingresar el inicio y fin de la ruta más corta
frame_entrada = ttk.Frame(root)
frame_entrada.pack(pady=10)

label_inicio = ttk.Label(frame_entrada, text="Inicio:")
label_inicio.grid(row=0, column=0, padx=10)

entry_inicio = ttk.Entry(frame_entrada)
entry_inicio.grid(row=0, column=1, padx=10)

label_fin = ttk.Label(frame_entrada, text="Fin:")
label_fin.grid(row=0, column=2, padx=10)

entry_fin = ttk.Entry(frame_entrada)
entry_fin.grid(row=0, column=3, padx=10)

# Botón para buscar la ruta más corta
button_encontrar_ruta = ttk.Button(frame_entrada, text="Buscar Ruta", command=on_button_click)
button_encontrar_ruta.grid(row=0, column=4, padx=10)

# Botón para salir
button_salir = ttk.Button(frame_entrada, text="Salir", command=salir)
button_salir.grid(row=0, column=5, padx=10)

root.mainloop()