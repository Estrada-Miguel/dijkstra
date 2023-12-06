from tkinter import *
from tkinter import messagebox
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


def on_button_click(rootr, entI, entF, grafo):
    inicio = entI.get().upper()
    fin = entF.get().upper()
    ruta_corta = encontrar_ruta_mas_corta(grafo, inicio, fin)

    # Crear una nueva ventana para el grafo con la ruta más corta
    ventana_ruta_corta = Toplevel(rootr)
    ventana_ruta_corta.title("Ruta Más Corta")

    fig, ax = plt.subplots(figsize=(8, 6))
    dibujar_ruta_mas_corta(grafo, ruta_corta, ax)

    # Incorporar la figura en la nueva ventana
    canvas = FigureCanvasTkAgg(fig, master=ventana_ruta_corta)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Agregar el botón "Salir" en la nueva ventana
    button_salir = Button(ventana_ruta_corta, text="Salir", command=ventana_ruta_corta.destroy)
    button_salir.pack()

def dibujar_grafo(grafo, ax):
    pos = nx.spring_layout(grafo, seed=42)
    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_nodes(grafo, pos, node_size=400, ax=ax)
    nx.draw_networkx_edges(grafo, pos, ax=ax)
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels, ax=ax)
    nx.draw_networkx_labels(grafo, pos, font_size=10, ax=ax)


def check_weight():
    for rows in range(len(all_entries)):
        for columns in range(len(all_entries[rows])):
            if all_entries[rows][columns].get().isdigit():
                if int(all_entries[rows][columns].get()) != 0:
                    if all_entries[columns][rows].get().isdigit():
                        if (int(all_entries[rows][columns].get()) == int(all_entries[columns][rows].get())) | (int(all_entries[columns][rows].get()) == 0):
                            continue
                        else:
                            textBox.config(state=NORMAL)
                            textBox.insert('1.0', "No se puede insertar dos diferentes distancias entre Nodos" + "\n")
                            textBox.config(state=DISABLED)
                            return False
            else:
                textBox.config(state=NORMAL)
                textBox.insert('1.0', "No es un digito valido, escriba un entero positivo" + "\n")
                textBox.config(state=DISABLED)
                return False
    return True


def generar_grafo(matriz, nodos):
    if check_weight():
        textBox.config(state=NORMAL)
        textBox.insert('1.0', "Grafo generado" + "\n")
        textBox.config(state=DISABLED)
        asignar_matriz()
        grafo = nx.DiGraph()
        simetrica = es_matriz_simetrica(matriz)
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                # Solo agregar aristas si la matriz es simétrica o si i < j
                if matriz[i][j] != 0:
                    grafo.add_edge(nodos[i], nodos[j], weight=matriz[i][j])
        newWindow = Toplevel(root)
        newWindow.title("Grafo")
        fig, ax = plt.subplots(figsize=(8, 6))
        dibujar_grafo(grafo, ax)
        canvas = FigureCanvasTkAgg(fig, master=newWindow)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        # Interfaz para ingresar el inicio y fin de la ruta más corta
        frame_entrada = Frame(newWindow)
        frame_entrada.pack(pady=10)

        label_inicio = Label(frame_entrada, text="Inicio:")
        label_inicio.grid(row=0, column=0, padx=10)

        entry_inicio = Entry(frame_entrada)
        entry_inicio.grid(row=0, column=1, padx=10)

        label_fin = Label(frame_entrada, text="Fin:")
        label_fin.grid(row=0, column=2, padx=10)

        entry_fin = Entry(frame_entrada)
        entry_fin.grid(row=0, column=3, padx=10)

        # Botón para buscar la ruta más corta
        button_encontrar_ruta = Button(frame_entrada, text="Buscar Ruta",
                                       command=lambda: on_button_click(newWindow, entry_inicio, entry_fin, grafo))
        button_encontrar_ruta.grid(row=0, column=4, padx=10)

        # Botón para salir
        button_salir = Button(frame_entrada, text="Salir", command=lambda: salir(newWindow))
        button_salir.grid(row=0, column=5, padx=10)

        newWindow.mainloop()
    else:
        print("Datos no validos en la matriz")



def salir(rootr):
    rootr.destroy()
    rootr.quit()


def es_matriz_simetrica(matriz):
    return all(matriz[i][j] == matriz[j][i] for i in range(len(matriz)) for j in range(len(matriz[0])))


def agregar_nodo():
    global lastLabel
    if (lastLabel + 1) - 91 != 0:
        lastLabel += 1
        nodos.append(chr(lastLabel))
        matriz.append([])
        all_entries.append([])
        all_labels.append([])
        # =============================== #
        nlabeltextV = Entry(root, width=2)
        nlabeltextV.insert(0, chr(lastLabel))
        nlabeltextV.config(state=DISABLED)
        nlabeltextV.grid(row=lastLabel - 62, column=1)
        nlabeltextH = Entry(root, width=2)
        nlabeltextH.insert(0, chr(lastLabel))
        nlabeltextH.config(state=DISABLED)
        nlabeltextH.grid(row=2, column=lastLabel-63)
        all_labels[-1].append(nlabeltextH)
        all_labels[-1].append(nlabeltextV)
        for size in range(len(matriz)):
            ent = Entry(root, width=3)
            ent.insert(0, "0")
            ent.grid(row=lastLabel - 62, column=size+2)
            matriz[-1].append(0)
            if size == len(matriz)-1:
                ent.config(state=DISABLED)
            all_entries[-1].append(ent)

        for nodo in range(len(matriz) - 1):
            matriz[nodo].append(0)
            ent = Entry(root, width=3)
            ent.insert(0, "0")
            ent.grid(row=3 + nodo, column=lastLabel-63)
            all_entries[nodo].append(ent)
        textBox.config(state=NORMAL)
        textBox.insert('1.0', "Se creo el Nodo " + chr(lastLabel) + "\n")
        textBox.config(state=DISABLED)
    else:
        textBox.config(state=NORMAL)
        textBox.insert('1.0', "No se puede crear mas Nodos" + "\n")
        textBox.config(state=DISABLED)
        print("No se puede agregar mas Nodos")
    for rows in matriz:
        print(rows)
    print(nodos)

def eliminar_nodo():
    global lastLabel
    if lastLabel - 1 != 64:
        lastLabel -= 1

        for entry in range(len(matriz[-1])):
            all_entries[-1][entry].grid_forget()

        all_entries.pop()
        nodos.pop()
        matriz.pop()

        for nodo in range(len(matriz)):
            matriz[nodo].pop()
            all_entries[nodo][-1].grid_forget()
            all_entries[nodo].pop()

        all_labels[-1][0].grid_forget()
        all_labels[-1][1].grid_forget()
        all_labels.pop()
        textBox.config(state=NORMAL)
        textBox.insert('1.0', "Se elimino el nodo " + chr(lastLabel+1) + "\n")
        textBox.config(state=DISABLED)
    else:
        textBox.config(state=NORMAL)
        textBox.insert('1.0', "No se puede eliminar mas nodos" + "\n")
        textBox.config(state=DISABLED)
        print("El ultimo Nodo no se puede eliminar")
    for rows in matriz:
        print(rows)
    print(nodos)

def asignar_matriz():
    for rows in range(len(matriz)):
        for columns in range(len(matriz[rows])):
            if all_entries[rows][columns].get().isdigit():
                if int(all_entries[rows][columns].get()) != 0:
                    if all_entries[columns][rows].get().isdigit():
                        if (int(all_entries[rows][columns].get()) == int(all_entries[columns][rows].get())) | (
                                int(all_entries[columns][rows].get()) == 0):
                            matriz[rows][columns] = int(all_entries[rows][columns].get())
                        else:
                            matriz[rows][columns] = int(all_entries[rows][columns].get())
                            all_entries[columns][rows].grid_forget()
                            all_entries[columns][rows] = Entry(root, width=3)
                            all_entries[columns][rows].insert(0, "0")
                            all_entries[columns][rows].grid(row=3 + columns, column=2 + rows)
                    else:
                        matriz[rows][columns] = int(all_entries[rows][columns].get())
                elif int(all_entries[rows][columns].get()) != matriz[rows][columns]:
                    matriz[rows][columns] = int(all_entries[rows][columns].get())
                    all_entries[rows][columns].grid_forget()
                    all_entries[rows][columns] = Entry(root, width=3)
                    all_entries[rows][columns].insert(0, "0")
                    all_entries[rows][columns].grid(row=3 + rows, column=2 + columns)
            else:
                print("Dato no asignado: [" + chr(65+rows) + ", " + chr(65+columns) + "]: " + "No es digito o entero positivo")
    for rows in matriz:
        print(rows)
    print(nodos)

def clear_matriz():
    for rows in range(len(matriz)):
        for columns in range(len(matriz[rows])):
            all_entries[rows][columns].grid_forget()
            all_entries[rows][columns] = Entry(root, width=3)
            all_entries[rows][columns].insert(0, "0")

            if rows == columns:
                all_entries[rows][columns].config(state=DISABLED)

            all_entries[rows][columns].grid(row= 3 + rows, column= 2 + columns)
    textBox.config(state=NORMAL)
    textBox.insert('1.0', "Clear" + "\n")
    textBox.config(state=DISABLED)


def quit_program():
    textBox.config(state=NORMAL)
    textBox.insert('1.0', "Quit" + "\n")
    textBox.config(state=DISABLED)
    mensaje_despedida = "Muchas gracias por usar nuestro servicio"
    messagebox.showinfo("Despedida", mensaje_despedida)
    root.destroy()
    root.quit()
# ===================== #
# Unitialized
lastLabel = 64
nodos = []
matriz = [[]]
all_entries = [[]]
all_labels = [[]]
# ===================== #
# Inicio del programa
root = Tk()
root.title("Ruta Mas Corta")
root.geometry("700x600")
btn_agregar = Button(root, text="Agregar", command=agregar_nodo)
btn_eliminar = Button(root, text="Eliminar", command=eliminar_nodo)
btn_assing = Button(root, text="Generar",  command=lambda: generar_grafo(matriz, nodos))
btn_clear = Button(root, text="Clear", command=clear_matriz)
btn_quit = Button(root, text="Quit", command=quit_program)
textBox = Text(root, height=1)
textBox.insert(INSERT, "Welcome")
textBox.config(state=DISABLED)
matriz[0] = [0]
lastLabel += 1  # "A"
nodos.append(chr(lastLabel))
labeltextV = Entry(root, width=2)
labeltextV.insert(0, chr(lastLabel))
labeltextV.config(state=DISABLED)
labeltextH = Entry(root, width=2)
labeltextH.insert(0, chr(lastLabel))
labeltextH.config(state=DISABLED)
e = Entry(root, width=3)
e.insert(0, "0")
e.config(state=DISABLED)
# ===================== #
textBox.grid(row=0, column=1, columnspan=25, sticky=W+E)
btn_agregar.grid(row=0,column=0, columnspan=1, sticky=W+E)
btn_eliminar.grid(row=1,column=0, columnspan=1, sticky=W+E)
btn_assing.grid(row=2,column=0, columnspan=1, sticky=W+E)
btn_clear.grid(row=3,column=0, columnspan=1, sticky=W+E)
btn_quit.grid(row=4, column=0, columnspan=1, sticky=W+E)
labeltextV.grid(row=lastLabel - 62, column=1)
labeltextH.grid(row=2, column=lastLabel-63)
e.grid(row=lastLabel-62,column=2) # row = 2
all_labels[0].append(labeltextH)
all_labels[0].append(labeltextV)
all_entries[0].append(e)
# ===================== #
root.mainloop()
# Imprimir
# for rows in matriz:
#    print(rows)
# print(nodos)