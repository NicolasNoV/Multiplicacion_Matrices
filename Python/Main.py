import os
import time
import numpy as np
import matplotlib.pyplot as plt
from NaivOnArray import multiplicacion_matrices_naiv as method_1
from NaivLoopUnrollingTwo import multiplicacion_matrices_unrolling_two as method_2
from NaivLoopUnrollingFour import multiplicacion_matrices_unrolling_four as method_3
from WinogradOriginal import multiplicacion_matrices_winograd as method_4
from WinogradScaled import multiplicacion_matrices_winograd_scaled as method_5
from StrassenNaiv import strassen_naiv as method_6
from StrassenWinograd import strassen_winograd as method_7
from SequentialBlock import multiplicacion_bloques_secuencial as method_8
from ParallelBlock import multiplicacion_bloques_paralelo as method_9
from EnhancedParallelBlock import enhanced_parallel_block_multiplication as method_10

# Diccionario para guardar tiempos de ejecución en memoria
tiempos_ejecucion = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": []
}

import os
import numpy as np

def cargar_matriz(filename):
    # Cambia esto a la ruta real de tu carpeta 'Matrices'
    base_dir = r"C:/Users/nicol/OneDrive/Desktop/Archivos/Proyectos Python/Proyecto Final A.A/Matrices"
    ruta_completa = os.path.join(base_dir, filename)

    # Verifica si el archivo existe
    if not os.path.exists(ruta_completa):
        raise FileNotFoundError(f"No se pudo encontrar el archivo: {ruta_completa}")

    # Lee y carga la matriz
    with open(ruta_completa, "r") as f:
        matriz = [list(map(int, line.split())) for line in f]
    return np.array(matriz)


def guardar_tiempos(tamano, tiempos):
    # Definir la ruta de los archivos de tiempos de Python
    ruta_python = r"C:/Users/nicol/OneDrive/Desktop/Archivos/Proyectos Python/Proyecto Final A.A/Tiempos/Python"
    
    # Crear la carpeta si no existe
    if not os.path.exists(ruta_python):
        os.makedirs(ruta_python)
    
    # Actualizar los tiempos en memoria
    if tamano in tiempos_ejecucion:
        tiempos_ejecucion[tamano].clear()
    else:
        tiempos_ejecucion[tamano] = []

    tiempos_ejecucion[tamano].extend(tiempos)

    # Guardar en archivo en la ruta especificada
    with open(os.path.join(ruta_python, f"{tamano}_tiempos.txt"), "w") as f:
        for nombre, tiempo in tiempos:
            f.write(f"{nombre}: {tiempo} segundos\n")


def cargar_tiempos_desde_archivo(tamano):
    # Ruta de los tiempos de Python
    ruta_python = r"C:/Users/nicol/OneDrive/Desktop/Archivos/Proyectos Python/Proyecto Final A.A/Tiempos/Python"
    filename = os.path.join(ruta_python, f"{tamano}_tiempos.txt")

    if not os.path.exists(filename):
        print(f"No existe el archivo {filename}")
        return []

    tiempos = []
    with open(filename, "r") as f:
        for line in f:
            partes = line.split(":")
            if len(partes) == 2:
                nombre = partes[0].strip()
                tiempo = float(partes[1].strip().split()[0])
                tiempos.append((nombre, tiempo))
    return tiempos


def cargar_tiempos_cplusplus(tamano):
    # Ruta de los tiempos de C++
    ruta_cplusplus = r"C:/Users/nicol/OneDrive/Desktop/Archivos/Proyectos Python/Proyecto Final A.A/Tiempos/Cplusplus"
    filename = os.path.join(ruta_cplusplus, f"{tamano}C_tiempos.txt")

    if not os.path.exists(filename):
        print(f"No existe el archivo {filename}")
        return []

    tiempos = []
    with open(filename, "r") as f:
        for line in f:
            partes = line.split(":")
            if len(partes) == 2:
                nombre = partes[0].strip()
                tiempo = float(partes[1].strip().split()[0])
                tiempos.append((nombre, tiempo))
    return tiempos


def graficar_tiempos(tamano):
    tiempos = cargar_tiempos_desde_archivo(tamano)
    if not tiempos:
        print(f"No hay datos de tiempos guardados para el tamaño {tamano}.")
        return

    tiempos = sorted(tiempos, key=lambda x: x[1])
    nombres = [nombre for nombre, _ in tiempos]
    valores = [tiempo for _, tiempo in tiempos]

    plt.figure(figsize=(10, 6))
    plt.barh(nombres, valores, color="skyblue")
    plt.xlabel("Tiempo de Ejecución (segundos)")
    plt.ylabel("Método")
    plt.title(f"Tiempos de Ejecución para Matrices Tamaño {tamano}")
    plt.show()

def graficar_tiempos_cplusplus(tamano):
    tiempos = cargar_tiempos_cplusplus(tamano)
    if not tiempos:
        print(f"No hay datos de tiempos guardados para el tamaño {tamano}.")
        return

    tiempos = sorted(tiempos, key=lambda x: x[1])
    nombres = [nombre for nombre, _ in tiempos]
    valores = [tiempo for _, tiempo in tiempos]

    plt.figure(figsize=(10, 6))
    plt.barh(nombres, valores, color="coral")
    plt.xlabel("Tiempo de Ejecución (segundos)")
    plt.ylabel("Método")
    plt.title(f"Tiempos de Ejecución (C++) para Matrices Tamaño {tamano}")
    plt.show()

def seleccionar_y_ejecutar_multiplicacion(opcion):
    matriz_A = cargar_matriz(f"{opcion}A.txt")
    matriz_B = cargar_matriz(f"{opcion}B.txt")
    metodos = [
        ("Naiv On Array", method_1), ("Naiv Loop Unrolling Two", method_2),
        ("Naiv Loop Unrolling Four", method_3), ("Winograd Original", method_4),
        ("Winograd Scaled", method_5), ("Strassen Naiv", method_6),
        ("Strassen Winograd", method_7), ("Sequential Block", method_8),
        ("Parallel Block", method_9), ("Enhanced Parallel Block", method_10)
    ]
    
    tiempos = []
    for nombre, metodo in metodos:
        start_time = time.time()
        metodo(matriz_A, matriz_B)
        end_time = time.time()
        tiempo_ejecucion = end_time - start_time
        tiempos.append((nombre, tiempo_ejecucion))
        print(f"{nombre} tomó {tiempo_ejecucion:.6f} segundos")
    
    guardar_tiempos(opcion, tiempos)

def comparar_resultados(tamano):
    # Cargar los tiempos de Python
    tiempos_python = cargar_tiempos_desde_archivo(tamano)
    if not tiempos_python:
        print(f"No se encontraron resultados para Python con el tamaño de matriz {tamano}.")
        return

    # Cargar los tiempos de C++
    tiempos_cplusplus = cargar_tiempos_cplusplus(tamano)
    if not tiempos_cplusplus:
        print(f"No se encontraron resultados para C++ con el tamaño de matriz {tamano}.")
        return

    # Convertir a diccionarios para facilitar la comparación
    tiempos_python_dict = dict(tiempos_python)
    tiempos_cplusplus_dict = dict(tiempos_cplusplus)

    print(f"\nComparación de resultados para matriz de tamaño {tamano}:\n")
    print(f"{'Método':<30} {'Python (s)':<15} {'C++ (s)':<15} {'Mejor':<10}")

    for metodo in set(tiempos_python_dict.keys()).union(tiempos_cplusplus_dict.keys()):
        tiempo_python = tiempos_python_dict.get(metodo, float('inf'))
        tiempo_cplusplus = tiempos_cplusplus_dict.get(metodo, float('inf'))

        if tiempo_python < tiempo_cplusplus:
            mejor = "Python"
        elif tiempo_cplusplus < tiempo_python:
            mejor = "C++"
        else:
            mejor = "Iguales"

        print(f"{metodo:<30} {tiempo_python:<15.6f} {tiempo_cplusplus:<15.6f} {mejor:<10}")

def main():
    tamanos_matriz = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8"
    }

    while True:
        print("\nSeleccione una opción:")
        print("1. Ejecutar multiplicación para matriz 2x2")
        print("2. Ejecutar multiplicación para matriz 4x4")
        print("3. Ejecutar multiplicación para matriz 8x8")
        print("4. Ejecutar multiplicación para matriz 16x16")
        print("5. Ejecutar multiplicación para matriz 32x32")
        print("6. Ejecutar multiplicación para matriz 64x64")
        print("7. Ejecutar multiplicación para matriz 128x128")
        print("8. Ejecutar multiplicación para matriz 256x256")
        print("9. Graficar tiempos de ejecución")
        print("10. Comparar resultados entre Python y C++")
        print("0. Salir")

        opcion = input("Ingrese el número de opción: ")

        if opcion in tamanos_matriz:
            seleccionar_y_ejecutar_multiplicacion(opcion)
        elif opcion == "9":
            sub_opcion = input("Seleccione el lenguaje para graficar (1=Python, 2=C++): ")
            if sub_opcion == "1":
                tamano = input("Ingrese el tamaño de matriz para graficar (1=2x2, 2=4x4, etc.): ")
                if tamano in tamanos_matriz:
                    graficar_tiempos(tamanos_matriz[tamano])
            elif sub_opcion == "2":
                tamano = input("Ingrese el tamaño de matriz para graficar (1=2x2, 2=4x4, etc.): ")
                if tamano in tamanos_matriz:
                    graficar_tiempos_cplusplus(tamanos_matriz[tamano])
        elif opcion == "10":
            tamano = input("Ingrese el tamaño de matriz para comparar (1=2x2, 2=4x4, etc.): ")
            if tamano in tamanos_matriz:
                comparar_resultados(tamanos_matriz[tamano])
        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
