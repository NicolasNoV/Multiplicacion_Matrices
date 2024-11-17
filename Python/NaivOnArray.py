import numpy as np

def multiplicacion_matrices_naiv(A, B):
    """
    Realiza la multiplicación de matrices de manera ingenua (NaivOnArray).
    Args:
        A (list of list of float): Matriz A.
        B (list of list of float): Matriz B.
    Returns:
        list of list of float: Resultado de la multiplicación de A y B.
    """
    # Convertir las matrices a arreglos de numpy con tipo de dato float64
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)
    
    filas_A, columnas_A = A.shape
    filas_B, columnas_B = B.shape

    if columnas_A != filas_B:
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B.")
    
    # Inicializar matriz resultado con ceros y tipo de dato float64
    C = np.zeros((filas_A, columnas_B), dtype=np.float64)
    
    # Realizar multiplicación matricial
    for i in range(filas_A):
        for j in range(columnas_B):
            for k in range(columnas_A):
                C[i, j] += A[i, k] * B[k, j]
                
    return C.tolist()  # Convertir el resultado a lista de listas si es necesario
