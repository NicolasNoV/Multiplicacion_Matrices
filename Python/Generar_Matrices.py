import numpy as np
import os

def guardar_matriz(matriz, filename):
    # Obtiene la ruta absoluta de la carpeta en la que se encuentra el archivo actual
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    # Define la ruta hacia la carpeta "Matrices"
    ruta_carpeta = os.path.join(ruta_base, "..", "Matrices")
    
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)  # Crear la carpeta si no existe
    
    ruta_completa = os.path.join(ruta_carpeta, filename)
    
    with open(ruta_completa, "w") as f:
        for fila in matriz:
            f.write(" ".join(map(str, fila)) + "\n")

def generar_casos_de_prueba():
    tamanos = [2, 4, 8, 16, 32, 64, 128, 256]  # Tamaños de matrices como potencias de 2
    for i, n in enumerate(tamanos, start=1):
        # Generar matrices A y B con números aleatorios de al menos 6 dígitos
        matriz_A = np.random.randint(100000, 999999, size=(n, n))
        matriz_B = np.random.randint(100000, 999999, size=(n, n))
        
        # Guardar las matrices con los nombres específicos
        guardar_matriz(matriz_A, f"{i}A.txt")
        guardar_matriz(matriz_B, f"{i}B.txt")

# Ejecutar la función para generar los casos de prueba
generar_casos_de_prueba()
