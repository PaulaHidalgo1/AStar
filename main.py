import heapq
import numpy as np
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk

class Nodo:
    def __init__(self, posicion, padre=None, costo_g=0, costo_h=0):
        self.posicion = posicion
        self.padre = padre
        self.g = costo_g
        self.h = costo_h
        self.f = self.g + self.h

    def __lt__(self, otro):
        return self.f < otro.f

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(mapa, inicio, fin):
    filas, cols = mapa.shape
    abiertos = []
    heapq.heappush(abiertos, Nodo(inicio, None, 0, heuristica(inicio, fin)))
    cerrados = set()
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    while abiertos:
        nodo_actual = heapq.heappop(abiertos)

        if nodo_actual.posicion == fin:
            ruta = []
            while nodo_actual:
                ruta.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return ruta[::-1]

        cerrados.add(nodo_actual.posicion)

        for mov in movimientos:
            nueva_pos = (nodo_actual.posicion[0] + mov[0], nodo_actual.posicion[1] + mov[1])
            if (0 <= nueva_pos[0] < filas and 0 <= nueva_pos[1] < cols and 
                mapa[nueva_pos] == 0 and nueva_pos not in cerrados):
                
                nuevo_nodo = Nodo(nueva_pos, nodo_actual, nodo_actual.g + 1, heuristica(nueva_pos, fin))
                heapq.heappush(abiertos, nuevo_nodo)
    
    return None  

def generar_mapa(filas=10, cols=10):
    return np.zeros((filas, cols), dtype=int)

def crear_obstaculos_aleatorios(mapa, inicio, fin, porcentaje=0.25):
    filas, cols = mapa.shape
    mapa.fill(0)
    num_obstaculos = int(filas * cols * porcentaje)

    for _ in range(num_obstaculos):
        x, y = random.randint(0, filas - 1), random.randint(0, cols - 1)
        if (x, y) != inicio and (x, y) != fin:
            mapa[x, y] = 1
    return mapa

def mostrar_mapa(mapa, ruta=None, inicio=None, fin=None):
    colores = {0: "lightgreen", 1: "black"}  # Calles en verde, edificios en negro
    fig, ax = plt.subplots(figsize=(7, 7))
    
    for x in range(mapa.shape[0]):
        for y in range(mapa.shape[1]):
            ax.add_patch(plt.Rectangle((y, x), 1, 1, color=colores[mapa[x, y]], ec="gray", lw=1.5))

    # Dibujar puntos de inicio y destino con iconos diferentes
    ax.text(inicio[1] + 0.3, inicio[0] + 0.3, "🏎️", fontsize=12, ha='center', va='center')
    ax.text(fin[1] + 0.3, fin[0] + 0.3, "🏁", fontsize=12, ha='center', va='center')

    # Dibujar la ruta con animación progresiva
    if ruta:
        for i, (x, y) in enumerate(ruta):
            ax.add_patch(plt.Circle((y + 0.5, x + 0.5), 0.3, color="red", alpha=0.8))
            plt.pause(0.1)  # Simulación de movimiento
        
    ax.set_xticks(range(mapa.shape[1] + 1))
    ax.set_yticks(range(mapa.shape[0] + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, linestyle='-', color='black', linewidth=1)
    plt.show()

def obtener_coordenadas(mensaje, filas, cols):
    while True:
        try:
            x, y = map(int, input(mensaje).split(","))
            if 0 <= x < filas and 0 <= y < cols:
                return (x, y)
            else:
                print(f"⚠️ Coordenadas fuera de rango (0-{filas-1}, 0-{cols-1}). Intenta de nuevo.")
        except ValueError:
            print("⚠️ Entrada inválida. Debes ingresar dos números separados por coma.")

def iniciar_juego():
    global mapa, inicio, fin, ruta

    filas, cols = 10, 10
    mapa = generar_mapa(filas, cols)

    inicio = obtener_coordenadas("\n📍 Introduce la posición de inicio (x,y): ", filas, cols)
    fin = obtener_coordenadas("🏁 Introduce la posición de destino (x,y): ", filas, cols)

    if inicio == fin:
        print("🚨 Error: La posición de inicio y destino no pueden ser iguales.")
        return iniciar_juego()

    mapa = crear_obstaculos_aleatorios(mapa, inicio, fin)
    ruta = a_star(mapa, inicio, fin)

    if ruta:
        print("✅ Ruta encontrada:", ruta)
        mostrar_mapa(mapa, ruta, inicio, fin)
    else:
        print("❌ No se encontró una ruta posible.")

    crear_interfaz()

def reiniciar_juego():
    iniciar_juego()

def generar_obstaculos():
    global mapa, ruta
    mapa = crear_obstaculos_aleatorios(mapa, inicio, fin)
    ruta = a_star(mapa, inicio, fin)

    if ruta:
        print("✅ Nueva ruta encontrada:", ruta)
        mostrar_mapa(mapa, ruta, inicio, fin)
    else:
        print("❌ No se encontró una nueva ruta.")

def crear_interfaz():
    root = tk.Tk()
    root.title("Opciones del Juego")
    root.geometry("300x200")
    root.configure(bg="#34495E")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)

    label = tk.Label(root, text="⚙️ Opciones", font=("Arial", 14, "bold"), bg="#34495E", fg="white")
    label.pack(pady=10)

    reiniciar_button = ttk.Button(root, text="🔄 Reiniciar Juego", command=reiniciar_juego, style="TButton")
    reiniciar_button.pack(pady=10)

    generar_button = ttk.Button(root, text="🚧 Generar Obstáculos Nuevos", command=generar_obstaculos, style="TButton")
    generar_button.pack(pady=10)

    root.mainloop()

iniciar_juego()
