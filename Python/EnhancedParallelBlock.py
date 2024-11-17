import numpy as np
from multiprocessing import Pool, cpu_count

# Definir el tamaño del bloque
TAMANIO_BLOQUE = 64

def procesar_bloque(i, j, k, A, B, n):
    """
    Multiplica y acumula un bloque específico y devuelve la parte correspondiente del resultado.
    Args:
        i, j, k (int): Índices de bloques en A y B.
        A, B (np.array): Matrices A y B.
        n (int): Dimensión de la matriz.
    Returns:
        tuple: (i, j, C_bloque) Posición del bloque y la submatriz resultado.
    """
    # Inicializar el bloque con el tipo de dato float64
    C_bloque = np.zeros((TAMANIO_BLOQUE, TAMANIO_BLOQUE), dtype=np.float64)
    for i1 in range(i, min(i + TAMANIO_BLOQUE, n)):
        for j1 in range(j, min(j + TAMANIO_BLOQUE, n)):
            for k1 in range(k, min(k + TAMANIO_BLOQUE, n)):
                C_bloque[i1 - i, j1 - j] += A[i1, k1] * B[k1, j1]
    return (i, j, C_bloque)

def enhanced_parallel_block_multiplication(A, B):
    """
    Realiza la multiplicación de matrices utilizando el algoritmo Enhanced Parallel Block.
    Args:
        A (np.array): Matriz A.
        B (np.array): Matriz B.
    Returns:
        np.array: Resultado de la multiplicación de A y B.
    """
    # Convertir matrices a tipo float64
    A = A.astype(np.float64)
    B = B.astype(np.float64)
    
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.float64)

    # Preparar los argumentos para cada bloque
    tareas = [(i, j, k, A, B, n) for i in range(0, n, TAMANIO_BLOQUE)
              for j in range(0, n, TAMANIO_BLOQUE)
              for k in range(0, n, TAMANIO_BLOQUE)]

    # Ejecutar en paralelo las multiplicaciones de bloques
    with Pool(cpu_count()) as pool:
        resultados = pool.starmap(procesar_bloque, tareas)

    # Combinar los resultados de los bloques en la matriz C
    for i, j, C_bloque in resultados:
        C[i:i + TAMANIO_BLOQUE, j:j + TAMANIO_BLOQUE] += C_bloque[:min(TAMANIO_BLOQUE, n - i), :min(TAMANIO_BLOQUE, n - j)]

    return C
