import numpy as np

def strassen_winograd(A, B):
    """
    Realiza la multiplicación de matrices utilizando el algoritmo de Strassen con optimización de Winograd.
    Args:
        A (list of list of float): Matriz A.
        B (list of list of float): Matriz B.
    Returns:
        list of list of float: Resultado de la multiplicación de A y B.
    """
    # Convertir a numpy para un manejo eficiente
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)

    # Ajustar a potencia de 2 si es necesario
    def ajustar_a_potencia2(M):
        tamaño_actual = M.shape[0]
        potencia = 2 ** int(np.ceil(np.log2(tamaño_actual)))
        M_ajustada = np.zeros((potencia, potencia))
        M_ajustada[:tamaño_actual, :tamaño_actual] = M
        return M_ajustada

    n = A.shape[0]
    if n & (n - 1) != 0:  # si no es potencia de 2
        A = ajustar_a_potencia2(A)
        B = ajustar_a_potencia2(B)
        n = A.shape[0]

    if n == 1:
        return [[A[0, 0] * B[0, 0]]]

    # Dividir matrices en cuadrantes
    mid = n // 2
    A11, A12, A21, A22 = A[:mid, :mid], A[:mid, mid:], A[mid:, :mid], A[mid:, mid:]
    B11, B12, B21, B22 = B[:mid, :mid], B[:mid, mid:], B[mid:, :mid], B[mid:, mid:]

    # Cálculo de productos intermedios optimizados con Strassen-Winograd
    M1 = strassen_winograd(suma_matrices(A11, A22), suma_matrices(B11, B22))
    M2 = strassen_winograd(suma_matrices(A21, A22), B11)
    M3 = strassen_winograd(A11, resta_matrices(B12, B22))
    M4 = strassen_winograd(A22, resta_matrices(B21, B11))
    M5 = strassen_winograd(suma_matrices(A11, A12), B22)
    M6 = strassen_winograd(resta_matrices(A21, A11), suma_matrices(B11, B12))
    M7 = strassen_winograd(resta_matrices(A12, A22), suma_matrices(B21, B22))

    # Calcular cuadrantes de C
    C11 = suma_matrices(resta_matrices(suma_matrices(M1, M4), M5), M7)
    C12 = suma_matrices(M3, M5)
    C21 = suma_matrices(M2, M4)
    C22 = suma_matrices(resta_matrices(suma_matrices(M1, M3), M2), M6)

    # Combinar cuadrantes en la matriz C
    C = np.zeros((n, n))
    C[:mid, :mid] = C11
    C[:mid, mid:] = C12
    C[mid:, :mid] = C21
    C[mid:, mid:] = C22

    # Retornar la matriz sin padding
    return C[:len(A), :len(B)].tolist()

# Funciones auxiliares para suma y resta de matrices
def suma_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def resta_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
