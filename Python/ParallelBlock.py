import concurrent.futures
import numpy as np

def multiplicacion_bloques_paralelo(A, B, tamaño_bloque=2):
    """
    Realiza la multiplicación de matrices utilizando bloques paralelos.
    Args:
        A (np.array): Matriz A.
        B (np.array): Matriz B.
        tamaño_bloque (int): Tamaño de bloque para la multiplicación.
    Returns:
        np.array: Resultado de la multiplicación de A y B.
    """
    # Convertir matrices a float64 para evitar desbordamiento
    A = A.astype(np.float64)
    B = B.astype(np.float64)
    
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.float64)

    def procesar_bloque(i, j, k):
        # Multiplica un bloque específico y acumula los resultados en C
        for i1 in range(i, min(i + tamaño_bloque, n)):
            for j1 in range(j, min(j + tamaño_bloque, n)):
                for k1 in range(k, min(k + tamaño_bloque, n)):
                    C[i1, j1] += A[i1, k1] * B[k1, j1]

    # Usamos un ThreadPoolExecutor para paralelizar el trabajo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tareas = []
        for i in range(0, n, tamaño_bloque):
            for j in range(0, n, tamaño_bloque):
                for k in range(0, n, tamaño_bloque):
                    tareas.append(executor.submit(procesar_bloque, i, j, k))

        # Esperamos a que todas las tareas terminen
        concurrent.futures.wait(tareas)

    return C
