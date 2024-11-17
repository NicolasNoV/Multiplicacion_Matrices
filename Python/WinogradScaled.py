import numpy as np

def multiplicacion_matrices_winograd_scaled(A, B):
    """
    Realiza la multiplicación de matrices utilizando el algoritmo Winograd con factores de escalado.
    Args:
        A (list of list of float): Matriz A.
        B (list of list of float): Matriz B.
    Returns:
        list of list of float: Resultado de la multiplicación de A y B.
    """
    # Convertir A y B en numpy arrays con float64 para mayor precisión
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)
    
    filas_A, columnas_A = A.shape
    filas_B, columnas_B = B.shape

    if columnas_A != filas_B:
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B.")

    # Pre-computar factores de fila y columna
    row_factor = np.zeros(filas_A, dtype=np.float64)
    col_factor = np.zeros(columnas_B, dtype=np.float64)

    for i in range(filas_A):
        for j in range(0, columnas_A // 2):
            row_factor[i] += A[i, 2 * j] * A[i, 2 * j + 1]

    for i in range(columnas_B):
        for j in range(0, filas_B // 2):
            col_factor[i] += B[2 * j, i] * B[2 * j + 1, i]

    # Calcular la matriz resultado
    C = np.zeros((filas_A, columnas_B), dtype=np.float64)
    for i in range(filas_A):
        for j in range(columnas_B):
            # Inicialización con factores de escalado
            C[i, j] = -row_factor[i] - col_factor[j]
            for k in range(0, columnas_A // 2):
                C[i, j] += (A[i, 2 * k] + B[2 * k + 1, j]) * (A[i, 2 * k + 1] + B[2 * k, j])

    # Si la matriz tiene un número impar de columnas
    if columnas_A % 2 == 1:
        for i in range(filas_A):
            for j in range(columnas_B):
                C[i, j] += A[i, columnas_A - 1] * B[columnas_A - 1, j]

    return C.tolist()  # Convertir a lista de listas si se necesita
