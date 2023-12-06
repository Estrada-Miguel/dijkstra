import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definir grafo y nodos como variables globales
grafo = None
nodos = None
canvas = None  # Agregar variable para el widget de lienzo

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
    ruta_edges = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
    nx.draw_networkx_edges(grafo, pos, edgelist=ruta_edges, edge_color='r', width=2, ax=ax)

# Función llamada cuando se presiona el botón "Buscar Ruta"
def on_button_click():
    inicio = entry_inicio.get().upper()
    fin = entry_fin.get().upper()

    try:
        if grafo is None:
            raise ValueError("No has ingresado ninguna matriz")

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

# Función llamada cuando se presiona el botón "Crear Matriz" al inicio
def crear_matriz():
    try:
        global nodos, grafo, canvas
        # Solicitar al usuario el tamaño de la matriz
        tamano = simpledialog.askinteger("Tamaño de la Matriz", "Ingrese el tamaño de la matriz (número de filas y columnas, mínimo 2):", minvalue=2)

        if tamano is not None:  # Verificar si el usuario canceló la operación
            # Crear una nueva ventana para ingresar los valores de la matriz
            ventana_matriz = tk.Toplevel(root)
            ventana_matriz.title("Ingresar Matriz")

            # Agregar mensaje informativo
            mensaje_label = ttk.Label(ventana_matriz, text="Ingrese cada uno de los datos de la matriz (Solo números)")
            mensaje_label.grid(row=0, columnspan=tamano, pady=10)

            # Crear matriz de entrada
            matriz_entrada = []
            for i in range(tamano):
                fila = []
                for j in range(tamano):
                    entry = ttk.Entry(ventana_matriz, validate='key', validatecommand=(root.register(validate_numeric_input), '%P'))
                    entry.grid(row=i + 1, column=j, padx=5, pady=5)
                    fila.append(entry)
                matriz_entrada.append(fila)

            # Agregar el botón "Aceptar" para procesar la matriz ingresada
            button_aceptar = ttk.Button(ventana_matriz, text="Aceptar", command=lambda: procesar_matriz(matriz_entrada, tamano, ventana_matriz))
            button_aceptar.grid(row=tamano + 1, column=0, pady=10)

            # Agregar el botón "Cancelar" para cancelar la operación
            button_cancelar = ttk.Button(ventana_matriz, text="Cancelar", command=ventana_matriz.destroy)
            button_cancelar.grid(row=tamano + 1, column=1, pady=10)

            # Definir nodos
            nodos = [str(i) for i in range(1, tamano + 1)]

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Función para procesar la matriz ingresada por el usuario
def procesar_matriz(matriz_entrada, tamano, ventana_matriz):
    try:
        global nodos, grafo, canvas
        # Obtener los valores de la matriz ingresada
        matriz_valores = []
        for i in range(tamano):
            fila = []
            for j in range(tamano):
                valor = float(matriz_entrada[i][j].get())
                fila.append(valor)
            matriz_valores.append(fila)

        # Generar el grafo con la matriz ingresada
        grafo_nuevo = generar_grafo(matriz_valores, nodos)

        # Si ya hay un grafo en la interfaz, limpiarlo antes de dibujar el nuevo
        if grafo is not None and canvas is not None:
            canvas.get_tk_widget().destroy()

        # Actualizar el grafo global
        grafo = grafo_nuevo

        # Dibujar el grafo en la interfaz principal
        fig, ax = plt.subplots(figsize=(8, 6))
        dibujar_grafo(grafo, ax)

        # Incorporar la figura en la ventana principal
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        # Cerrar la ventana de ingreso de datos de la matriz
        ventana_matriz.destroy()

    except ValueError as e:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos en todas las celdas de la matriz")

# Función para validar la entrada como número
def validate_numeric_input(value):
    if value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
        return True
    elif value == "":
        return True
    else:
        return False

# Interfaz principal
root = tk.Tk()
root.title("Ruta Más Corta")

# Botón para crear la matriz al inicio
button_crear_matriz = ttk.Button(root, text="Crear Matriz", command=crear_matriz)
button_crear_matriz.pack(pady=10)

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
