import numpy as np

def multiplicacion_matrices_unrolling_two(A, B):
    """
    Realiza la multiplicación de matrices con desenrollado de bucle en bloques de dos.
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
    
    # Realizar multiplicación matricial con desenrollado en bloques de dos
    for i in range(filas_A):
        for j in range(columnas_B):
            k = 0
            while k <= columnas_A - 2:
                C[i, j] += A[i, k] * B[k, j] + A[i, k + 1] * B[k + 1, j]
                k += 2
            # Para el caso en que la cantidad de columnas no es par
            if k < columnas_A:
                C[i, j] += A[i, k] * B[k, j]
    
    return C.tolist()  # Convertir el resultado a lista de listas si es necesario
