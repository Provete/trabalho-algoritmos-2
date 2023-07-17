# Feito por:    Gustavo Provete de Andrade
#               Ruan Vieira Ribeiro
#               Tiago Artém dos Santos

import numpy
import numpy as np
import sys
import time


def isfloat(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    NOME_ENTRADA = sys.argv[1]


def ler_entrada() -> tuple:
    with open(NOME_ENTRADA, 'r') as entrada:
        quantidade_sistemas, dimencao_matriz, margem_erro = entrada.readline().split(' ')

        quantidade_sistemas = int(quantidade_sistemas.strip())
        dimencao_matriz = int(dimencao_matriz.strip())
        margem_erro = float(margem_erro.strip())

        A: np.array = np.zeros((dimencao_matriz, dimencao_matriz))
        B: np.array = np.zeros((quantidade_sistemas, dimencao_matriz))

        for linha in range(0, dimencao_matriz):
            for coluna, valor in enumerate(entrada.readline().split(' ')):
                if isfloat(valor.strip()) and coluna < dimencao_matriz:
                    A[linha][coluna] = float(valor.strip())

        for linha in range(0, quantidade_sistemas):
            for coluna, valor in enumerate(entrada.readline().split(' ')):
                if isfloat(valor.strip()) and coluna < dimencao_matriz:
                    B[linha][coluna] = float(valor.strip())

        return A, B, dimencao_matriz, quantidade_sistemas, margem_erro


def gerar_matriz_auxiliar(matriz: np.array, b: np.array) -> np.array:
    dimencao_matriz = matriz.shape[0]
    matriz_auxiliar: np.array = np.zeros((dimencao_matriz, dimencao_matriz + 1))

    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            matriz_auxiliar[i][j] = valor

    for i, valor in enumerate(b):
        matriz_auxiliar[i][dimencao_matriz] = valor

    return matriz_auxiliar


def multiplicar_linha(linha: np.array, multiplicador: float) -> np.array:
    for i in range(0, linha.size):
        linha[i] *= multiplicador

    return linha


def somar_linhas_com_multiplicador(linha1: np.array
                                   , linha2: np.array
                                   , multiplicador: float) -> np.array:
    linha2 = multiplicar_linha(linha2, multiplicador)

    for i in range(0, linha1.size):
        linha1[i] += linha2[i]

    return linha1


# Eliminação de Gauss
def pivoteamento(A: np.array, b: np.array, n: int) -> np.array:
    for i in range(n - 1):
        pivo = A[i][i]
        troca_pivo = i

        # Identificando maior pivo da coluna
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(pivo):
                pivo = A[j][i]
                troca_pivo = j

        # troca de linha, pivo na posição diferente de i
        if troca_pivo != i:
            b[i], b[troca_pivo] = b[troca_pivo], b[i]
            for k in range(n):
                A[i][k], A[troca_pivo][k] = A[troca_pivo][k], A[i][k]

        # divisão dos elementos
        for j in range(i + 1, n):
            matriz_aux = A[j][i] / A[i][i]
            A[j][i] = 0

            for k in range(i + 1, n):
                A[j][k] = A[j][k] - (matriz_aux * A[i][k])
            b[j] = b[j] - (matriz_aux * b[i])

    result: np.array = np.zeros(n)
    # calculo triangular superior
    for i in range(n - 1, -1, -1):
        result[i] = b[i] / A[i][i]
        for j in range(i - 1, -1, -1):
            b[j] = b[j] - A[j][i] * result[i]

    return result


class Lu:
    def __init__(self, size):
        self.size = size
        self.sistema = np.zeros((size, size))
        self.matrizL = np.zeros((size, size))
        self.matrizU = np.zeros((size, size))
        self.arrayY = np.zeros(size)
        self.arrayR = np.zeros(size)
        self.arrayX = np.zeros(size)

    def ImprimeMatriz(self, matriz):
        for i in range(self.size):
            print()
            for j in range(self.size):
                print(f'{matriz[i][j]:.2f}', end=' ')
        print()

    def ImprimeVetor(self, vetor):
        for i in range(self.size):
            print(f'{vetor[i]:.2f}')
        print()

    def OperacaoPivo(self, k):
        for i in range(k + 1, self.size):
            self.matrizL[i][k] = self.sistema[i][k] / self.sistema[k][k]
            for j in range(k, self.size):
                self.sistema[i][j] -= self.matrizL[i][k] * self.sistema[k][j]

    def MatrizL(self):
        for i in range(self.size):
            self.matrizL[i][i] = 1.0
            for j in range(i + 1, self.size):
                self.matrizL[i][j] = 0.0

    def MatrizU(self):
        for i in range(self.size):
            for j in range(i, self.size):
                self.matrizU[i][j] = self.sistema[i][j]

    def LY(self):
        for i in range(self.size):
            self.arrayY[i] = self.arrayR[i]
            for j in range(i):
                self.arrayY[i] -= self.matrizL[i][j] * self.arrayY[j]

    def UX(self):
        for i in range(self.size - 1, -1, -1):
            sum = 0.0
            for j in range(i + 1, self.size):
                sum += self.matrizU[i][j] * self.arrayX[j]
            self.arrayX[i] = (self.arrayY[i] - sum) / self.matrizU[i][i]


def pegar_x_inicial(A: np.array, b: np.array) -> np.array:
    xInicial: np.array = b.copy()
    xInicial.fill(0)

    for i in range(b.size):
        xInicial[i] = b[i] / A[i][i]

    return xInicial


def resolver_sistema_gauss_jacob(A: np.array,
                                 b: np.array,
                                 X: np.array,
                                 margem_erro: float) -> np.array:
    novoX: np.array = X.copy()

    while True:

        for i in range(X.size):
            novoX[i] = b[i]

            for j in range(A.shape[0]):
                if i != j:
                    novoX[i] -= A[i][j] * X[j]
            novoX[i] /= A[i][i]

        diferenca_X = numpy.subtract(novoX, X)
        erro_relativo: float = np.abs(diferenca_X).max() / np.abs(novoX).max()

        if erro_relativo <= margem_erro:
            return novoX
        else:
            X = novoX


def resolver_sistema_gauss_seidel(A: np.array,
                                  b: np.array,
                                  X: np.array,
                                  margem_erro: float) -> np.array:
    novoX: np.array = X.copy()

    while True:
        for i in range(A.shape[0]):
            novoX[i] = b[i]

            for j in range(A.shape[0]):
                if i != j:
                    novoX[i] -= A[i][j] * novoX[j]
            novoX[i] /= A[i][i]

        diferenca_X = numpy.subtract(novoX, X)
        erro_relativo: float = np.abs(diferenca_X).max() / np.abs(novoX).max()

        if erro_relativo <= margem_erro:
            return novoX
        else:
            X = novoX


# chamada pivoteamento para todos os sistemas
if __name__ == '__main__':
    A, B, dimencao_matriz, quantidade_sistemas, margem_erro = ler_entrada()
    print('Eliminação de Gauss:')
    for i in range(0, quantidade_sistemas):
        pivoteamento(A.copy(), B[i].copy(), dimencao_matriz)

    print('\n\n')

    print('Metodo Gauss-Jacob:')
    for i in range(0, quantidade_sistemas):
        print('Solução: ')

        start = time.perf_counter()
        print(resolver_sistema_gauss_jacob(A.copy(), B[i].copy(), pegar_x_inicial(A, B[i]), margem_erro))
        print(f'Resolvido em {start - time.perf_counter()} segundos')

    print('\n\n')

    print('Metodo Gauss-Seidel:')
    for i in range(0, quantidade_sistemas):
        print('Solução: ')

        start = time.perf_counter()
        print(resolver_sistema_gauss_seidel(A.copy(), B[i].copy(), pegar_x_inicial(A, B[i]), margem_erro))
        print(f'Resolvido em {start - time.perf_counter()} segundos')

    print('\n\n\n')

    print('Fatoração LU: ')
    with open(NOME_ENTRADA, 'r') as file:
        # Leitura da quantidade de matrizes, tamanho do vetor e precisão
        line = file.readline().split()
        num_matrices = int(line[0])
        size = int(line[1])
        matrizA = np.zeros((size, size))

        # Leitura da matriz A
        for i in range(size):
            matrizA[i] = list(map(float, file.readline().split()))

        for _ in range(num_matrices):
            lu = Lu(size)

            # Definir a matriz A para cada iteração
            lu.sistema = matrizA.copy()

            # Leitura da matriz B
            lu.arrayR = list(map(float, file.readline().split()))

            start = time.perf_counter()
            for k in range(size - 1):
                lu.OperacaoPivo(k)

            lu.MatrizL()

            lu.MatrizU()

            lu.LY()

            lu.UX()

            print(f'Resolvido em {start - time.perf_counter()} segundos')
            print('Resultado: ')
            lu.ImprimeVetor(lu.arrayX)
