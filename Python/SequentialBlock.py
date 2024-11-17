import numpy as np

def multiplicacion_bloques_secuencial(A, B, tamaño_bloque=2):
    """
    Realiza la multiplicación de matrices utilizando bloques secuenciales.
    Args:
        A (list of list of float): Matriz A.
        B (list of list of float): Matriz B.
        tamaño_bloque (int): Tamaño de bloque para la multiplicación.
    Returns:
        list of list of float: Resultado de la multiplicación de A y B.
    """
    # Convertir a numpy para optimizar operaciones
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)
    
    # Dimensiones de las matrices
    filas_A, columnas_A = A.shape
    filas_B, columnas_B = B.shape
    
    if columnas_A != filas_B:
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B.")
    
    # Crear la matriz de resultados con ceros
    C = np.zeros((filas_A, columnas_B), dtype=np.float64)

    # Multiplicación por bloques
    for i in range(0, filas_A, tamaño_bloque):
        for j in range(0, columnas_B, tamaño_bloque):
            for k in range(0, columnas_A, tamaño_bloque):
                # Calcular el límite efectivo del bloque actual
                sub_A = A[i:i + tamaño_bloque, k:k + tamaño_bloque]
                sub_B = B[k:k + tamaño_bloque, j:j + tamaño_bloque]
                
                # Obtener las dimensiones reales de los sub-bloques
                bloque_filas = sub_A.shape[0]
                bloque_columnas = sub_B.shape[1]
                
                # Actualizar los elementos de la matriz de resultados
                C[i:i + bloque_filas, j:j + bloque_columnas] += np.dot(sub_A, sub_B)
                
    return C.tolist()
