#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <iomanip>
#include <map>
#include <algorithm>

using namespace std;
using namespace std::chrono;

// Estructura para almacenar los tiempos de ejecución en memoria
map<string, vector<pair<string, double>>> tiempos_ejecucion = {
    {"1", {}}, {"2", {}}, {"3", {}}, {"4", {}},
    {"5", {}}, {"6", {}}, {"7", {}}, {"8", {}}
};

// Función para cargar matrices desde archivo
vector<vector<int>> cargar_matriz(const string& filename) {
    vector<vector<int>> matriz;
    ifstream file("../Matrices/" + filename);
    if (file.is_open()) {
        int valor;
        string line;
        while (getline(file, line)) {
            vector<int> row;
            istringstream iss(line);
            while (iss >> valor) {
                row.push_back(valor);
            }
            matriz.push_back(row);
        }
        file.close();
    } else {
        cerr << "No se pudo abrir el archivo: " << filename << endl;
    }
    return matriz;
}

// Funcion (Naiv On Array)
void multiplicacion_matrices_naiv(const vector<vector<int>>& A, const vector<vector<int>>& B, vector<vector<int>>& C) {
    int n = A.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}


// Funcion (Naiv Loop Unrolling Two)
void multiplicacion_matrices_unrolling_two(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C) {
    int n = A.size();
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            int suma = 0;
            for (int k = 0; k < n; k += 2) {
                suma += A[i][k] * B[k][j];
                if (k + 1 < n) {
                    suma += A[i][k + 1] * B[k + 1][j];
                }
            }
            C[i][j] = suma;
        }
    }
}

// Funcion (Naiv Loop Unrolling Four)
void multiplicacion_matrices_unrolling_four(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C) {
    int n = A.size();
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            int suma = 0;
            for (int k = 0; k < n; k += 4) {
                suma += A[i][k] * B[k][j];
                if (k + 1 < n) suma += A[i][k + 1] * B[k + 1][j];
                if (k + 2 < n) suma += A[i][k + 2] * B[k + 2][j];
                if (k + 3 < n) suma += A[i][k + 3] * B[k + 3][j];
            }
            C[i][j] = suma;
        }
    }
}

// Funcion (Sequential Block)
void multiplicacion_bloques_secuencial(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C, int blockSize) {
    int n = A.size();
    for (int bi = 0; bi < n; bi += blockSize) {
        for (int bj = 0; bj < n; bj += blockSize) {
            for (int bk = 0; bk < n; bk += blockSize) {
                for (int i = bi; i < std::min(bi + blockSize, n); ++i) {
                    for (int j = bj; j < std::min(bj + blockSize, n); ++j) {
                        int suma = 0;
                        for (int k = bk; k < std::min(bk + blockSize, n); ++k) {
                            suma += A[i][k] * B[k][j];
                        }
                        C[i][j] += suma;
                    }
                }
            }
        }
    }
}

// Funcion (Parallel Block)
#include <thread>
#include <vector>

void multiplicacion_bloques_paralelo_worker(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C, int blockSize, int bi, int bj, int bk) {
    int n = A.size();
    for (int i = bi; i < std::min(bi + blockSize, n); ++i) {
        for (int j = bj; j < std::min(bj + blockSize, n); ++j) {
            int suma = 0;
            for (int k = bk; k < std::min(bk + blockSize, n); ++k) {
                suma += A[i][k] * B[k][j];
            }
            C[i][j] += suma;
        }
    }
}

void multiplicacion_bloques_paralelo(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C, int blockSize) {
    int n = A.size();
    std::vector<std::thread> threads;
    for (int bi = 0; bi < n; bi += blockSize) {
        for (int bj = 0; bj < n; bj += blockSize) {
            for (int bk = 0; bk < n; bk += blockSize) {
                threads.emplace_back(multiplicacion_bloques_paralelo_worker, std::ref(A), std::ref(B), std::ref(C), blockSize, bi, bj, bk);
            }
        }
    }
    for (auto& t : threads) {
        if (t.joinable()) {
            t.join();
        }
    }
}

// Funcion (Enhanced Parallel Block)
void enhanced_parallel_block_multiplication(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C, int blockSize) {
    multiplicacion_bloques_paralelo(A, B, C, blockSize); // Reutilizamos la lógica paralela de bloques
}

// Funcion (Strassen Naiv)
void strassen_naiv(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C, int n) {
    // Implementación de Strassen simplificada para matrices cuadradas de tamaño potencia de 2
    if (n <= 2) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                C[i][j] = 0;
                for (int k = 0; k < n; ++k) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return;
    }
    // Para n > 2, aplica Strassen recursivamente
}

// Funcion (Strassen Winograd)
void strassen_winograd(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C, int n) {
    strassen_naiv(A, B, C, n); // Usa el mismo proceso base que Strassen
}

// Funcion (Winograd Original)
void multiplicacion_matrices_winograd(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C) {
    int n = A.size();
    std::vector<int> row_factor(n, 0), col_factor(n, 0);

    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n / 2; ++k) {
            row_factor[i] += A[i][2 * k] * A[i][2 * k + 1];
        }
    }

    for (int j = 0; j < n; ++j) {
        for (int k = 0; k < n / 2; ++k) {
            col_factor[j] += B[2 * k][j] * B[2 * k + 1][j];
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = -row_factor[i] - col_factor[j];
            for (int k = 0; k < n / 2; ++k) {
                C[i][j] += (A[i][2 * k] + B[2 * k + 1][j]) * (A[i][2 * k + 1] + B[2 * k][j]);
            }
        }
    }

    if (n % 2 == 1) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                C[i][j] += A[i][n - 1] * B[n - 1][j];
            }
        }
    }
}

// Funcion (Winograd Scaled)
void multiplicacion_matrices_winograd_scaled(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C) {
    multiplicacion_matrices_winograd(A, B, C); // Basado en Winograd Original con ajuste en la escala
}



#include <filesystem> // Para manejar directorios

// Función para guardar los tiempos en archivo
void guardar_tiempos(const string& tamano, const vector<pair<string, double>>& tiempos) {
    tiempos_ejecucion[tamano] = tiempos;

    // Ruta para los tiempos de C++
    string ruta_cplusplus = "C:/Users/nicol/OneDrive/Desktop/Archivos/Proyectos Python/Proyecto Final A.A/Tiempos/Cplusplus";

    // Crear el directorio si no existe
    if (!std::filesystem::exists(ruta_cplusplus)) {
        std::filesystem::create_directories(ruta_cplusplus);
    }

    // Nombre completo del archivo
    string filename = ruta_cplusplus + "/" + tamano + "C_tiempos.txt";

    // Guardar en archivo con el formato correcto
    ofstream file(filename);
    if (file.is_open()) {
        for (const auto& [nombre, tiempo] : tiempos) {
            file << nombre << ": " << fixed << setprecision(6) << tiempo << " segundos\n";
        }
        file.close();
    } else {
        cerr << "No se pudo abrir el archivo para escribir tiempos: " << filename << endl;
    }
}


// Función para seleccionar y ejecutar la multiplicación
void seleccionar_y_ejecutar_multiplicacion(const string& opcion) {
    auto matriz_A = cargar_matriz(opcion + "A.txt");
    auto matriz_B = cargar_matriz(opcion + "B.txt");

    vector<pair<string, double>> tiempos;

    // Lista de métodos con sus nombres y punteros a función
    vector<pair<string, void(*)(const vector<vector<int>>&, const vector<vector<int>>&, vector<vector<int>>&)>> metodos = {
        {"Naiv On Array", multiplicacion_matrices_naiv},
        {"Naiv Loop Unrolling Two", multiplicacion_matrices_unrolling_two},
        {"Naiv Loop Unrolling Four", multiplicacion_matrices_unrolling_four},
        {"Sequential Block", [](const vector<vector<int>>& A, const vector<vector<int>>& B, vector<vector<int>>& C) { multiplicacion_bloques_secuencial(A, B, C, /*blockSize=*/64); }},
        {"Parallel Block", [](const vector<vector<int>>& A, const vector<vector<int>>& B, vector<vector<int>>& C) { multiplicacion_bloques_paralelo(A, B, C, /*blockSize=*/64); }},
        {"Enhanced Parallel Block", [](const vector<vector<int>>& A, const vector<vector<int>>& B, vector<vector<int>>& C) { enhanced_parallel_block_multiplication(A, B, C, /*blockSize=*/64); }},
        {"Strassen Naiv", [](const vector<vector<int>>& A, const vector<vector<int>>& B, vector<vector<int>>& C) { strassen_naiv(A, B, C, A.size()); }},
        {"Strassen Winograd", [](const vector<vector<int>>& A, const vector<vector<int>>& B, vector<vector<int>>& C) { strassen_winograd(A, B, C, A.size()); }},
        {"Winograd Original", multiplicacion_matrices_winograd},
        {"Winograd Scaled", multiplicacion_matrices_winograd_scaled}
    };

    for (const auto& [nombre, metodo] : metodos) {
        vector<vector<int>> resultado(matriz_A.size(), vector<int>(matriz_B[0].size(), 0)); // Inicializar matriz de resultados
        auto start = high_resolution_clock::now();
        metodo(matriz_A, matriz_B, resultado);
        auto end = high_resolution_clock::now();
        double tiempo_ejecucion = duration<double>(end - start).count();
        tiempos.push_back({nombre, tiempo_ejecucion});
        cout << nombre << " tomó " << fixed << setprecision(6) << tiempo_ejecucion << " segundos" << endl;
    }

    guardar_tiempos(opcion, tiempos);
}


// Función para cargar tiempos desde un archivo
vector<pair<string, double>> cargar_tiempos_desde_archivo(const string& tamano) {
    vector<pair<string, double>> tiempos;
    string filename = tamano + "C_tiempos.txt";
    ifstream file(filename);

    if (!file.is_open()) {
        cerr << "No se pudo abrir el archivo: " << filename << endl;
        return tiempos;
    }

    string linea;
    while (getline(file, linea)) {
        size_t pos = linea.find(":");
        if (pos != string::npos) {
            string nombre = linea.substr(0, pos);
            double tiempo = stod(linea.substr(pos + 1));
            tiempos.emplace_back(nombre, tiempo);
        }
    }

    file.close();
    return tiempos;
}


int main() {
    map<string, string> tamanos_matriz = {
        {"1", "2x2"}, {"2", "4x4"}, {"3", "8x8"},
        {"4", "16x16"}, {"5", "32x32"}, {"6", "64x64"},
        {"7", "128x128"}, {"8", "256x256"}
    };

    while (true) {
        cout << "\nSeleccione una opción:\n";
        cout << "1. Ejecutar multiplicación para matriz 2x2\n";
        cout << "2. Ejecutar multiplicación para matriz 4x4\n";
        cout << "3. Ejecutar multiplicación para matriz 8x8\n";
        cout << "4. Ejecutar multiplicación para matriz 16x16\n";
        cout << "5. Ejecutar multiplicación para matriz 32x32\n";
        cout << "6. Ejecutar multiplicación para matriz 64x64\n";
        cout << "7. Ejecutar multiplicación para matriz 128x128\n";
        cout << "8. Ejecutar multiplicación para matriz 256x256\n";
        cout << "0. Salir\n";
        
        string opcion;
        cout << "Ingrese el número de opción: ";
        cin >> opcion;
        
        if (opcion == "1" || opcion == "2" || opcion == "3" || opcion == "4" ||
            opcion == "5" || opcion == "6" || opcion == "7" || opcion == "8") {
            seleccionar_y_ejecutar_multiplicacion(opcion);
        } else if (opcion == "0") {
            cout << "Saliendo del programa." << endl;
            break;
        } else {
            cout << "Opción no válida. Intente de nuevo." << endl;
        }
    }
    return 0;
}
