import numpy as np

def strassen_naiv(A, B):
    """
    Realiza la multiplicación de matrices utilizando el algoritmo de Strassen.
    Args:
        A (list of list of float): Matriz A.
        B (list of list of float): Matriz B.
    Returns:
        list of list of float: Resultado de la multiplicación de A y B.
    """
    # Convertir a numpy para mejor manejo en potencias de 2 y precisión
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)

    # Verificar tamaño y ajustar a potencia de 2 si es necesario
    def ajustar_a_potencia2(M):
        tamaño_actual = M.shape[0]
        potencia = 2**int(np.ceil(np.log2(tamaño_actual)))
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

    # Cálculo de los productos de Strassen
    P1 = strassen_naiv(A11, resta_matrices(B12, B22))
    P2 = strassen_naiv(suma_matrices(A11, A12), B22)
    P3 = strassen_naiv(suma_matrices(A21, A22), B11)
    P4 = strassen_naiv(A22, resta_matrices(B21, B11))
    P5 = strassen_naiv(suma_matrices(A11, A22), suma_matrices(B11, B22))
    P6 = strassen_naiv(resta_matrices(A12, A22), suma_matrices(B21, B22))
    P7 = strassen_naiv(resta_matrices(A11, A21), suma_matrices(B11, B12))

    # Calcular cuadrantes de C
    C11 = suma_matrices(resta_matrices(suma_matrices(P5, P4), P2), P6)
    C12 = suma_matrices(P1, P2)
    C21 = suma_matrices(P3, P4)
    C22 = suma_matrices(resta_matrices(suma_matrices(P5, P1), P3), P7)

    # Combinar los cuadrantes en la matriz C
    C = np.zeros((n, n))
    C[:mid, :mid] = C11
    C[:mid, mid:] = C12
    C[mid:, :mid] = C21
    C[mid:, mid:] = C22

    # Eliminar filas y columnas de padding si hubo ajuste
    return C[:len(A), :len(B)].tolist()

# Funciones auxiliares para suma y resta de matrices
def suma_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def resta_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
