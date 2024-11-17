import numpy as np

def multiplicacion_matrices_unrolling_four(A, B):
    """
    Realiza la multiplicación de matrices con desenrollado de bucle en bloques de cuatro.
    Args:
        A (list of list of float): Matriz A.
        B (list of list of float): Matriz B.
    Returns:
        list of list of float: Resultado de la multiplicación de A y B.
    """
    # Convertir las matrices de entrada a numpy arrays con tipo float64
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)
    
    filas_A, columnas_A = A.shape
    filas_B, columnas_B = B.shape

    if columnas_A != filas_B:
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B.")
    
    # Inicializar la matriz resultado con ceros y tipo float64
    C = np.zeros((filas_A, columnas_B), dtype=np.float64)
    
    # Realizar la multiplicación con desenrollado en bloques de cuatro
    for i in range(filas_A):
        for j in range(columnas_B):
            k = 0
            while k <= columnas_A - 4:
                C[i, j] += (A[i, k] * B[k, j] + A[i, k + 1] * B[k + 1, j] +
                            A[i, k + 2] * B[k + 2, j] + A[i, k + 3] * B[k + 3, j])
                k += 4
            # Para los elementos restantes no cubiertos en el bucle
            while k < columnas_A:
                C[i, j] += A[i, k] * B[k, j]
                k += 1
    
    return C.tolist()  # Convertir el resultado a lista de listas si es necesario
