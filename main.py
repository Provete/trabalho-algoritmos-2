import math

import numpy as np
import csv


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


class Dados:
    tempoArray: list
    quantidadeArray: list

    def __init__(self):
        self.tempoArray = list()
        self.quantidadeArray = list()

    def adicionarTempoEQuantidade(self, novoTempo: float, novaQuantidade: float):
        self.tempoArray.append(novoTempo)
        self.quantidadeArray.append(novaQuantidade)

    def imprimirDados(self):
        for tempo, quantidade in self.pegarDados():
            print(tempo, ' ', quantidade)

        print()

    def pegarDadosEnumerados(self):
        return [(i + 1, self.tempoArray[i], self.quantidadeArray[i]) for i in range(len(self.tempoArray))]

    def pegarDados(self):
        return zip(self.tempoArray, self.quantidadeArray)

    def calcularCoeficienteMatrizA(self, i: int, j: int) -> float:
        soma: float = 0.0
        for tempo in self.tempoArray:
            soma += math.pow(tempo, i + j)

        return soma

    def calcularCoeficienteVetorB(self, i: int):
        soma: float = 0

        for tempo, quantidade in zip(self.tempoArray, self.quantidadeArray):
            soma += quantidade * math.pow(tempo, i)

        return soma

    def calcularLogaritmoVetorC(self):
        novo_vetor = []
        for quantidade in self.quantidadeArray:
            log = math.log(quantidade)
            novo_vetor.append(log)
        return novo_vetor

    def calcularMultiplicacaoVetorTeLogVetorC(self, logC):
        novo_vetor = []
        for tempo, logQntd in zip(self.tempoArray, logC):
            resultado = tempo * logQntd
            novo_vetor.append(resultado)
        return novo_vetor

    def calcularVetorBLog(self):
        logC = self.calcularLogaritmoVetorC()
        tLogC = self.calcularMultiplicacaoVetorTeLogVetorC(logC)
        return [sum(logC), sum(tLogC)]

    def calcularTaoQuadrado(self):
        novo_vetor = []
        for tempo in self.tempoArray:
            novo_vetor.append(tempo * tempo)
        return novo_vetor

    def calcularMatrizALog(self):
        nova_matriz = np.zeros((2, 2))
        nova_matriz[0][0] = len(self.tempoArray)
        nova_matriz[0][1] = sum(self.tempoArray)
        nova_matriz[1][0] = nova_matriz[0][1]
        nova_matriz[1][1] = sum(self.calcularTaoQuadrado())
        return nova_matriz


class Regressor:
    dados: Dados

    def __init__(self, nomeArquivo: str):
        self.lerDados(nomeArquivo)

    def lerDados(self, nomeArquivo: str):
        self.dados = Dados()

        with open(nomeArquivo, 'r') as arquivo:
            leitor = csv.reader(arquivo, delimiter=',')

            for linha in leitor:
                tempo = float(linha[0])
                quantidade = float(linha[1])
                self.dados.adicionarTempoEQuantidade(tempo, quantidade)

    def calcularCoeficientesPrimeiroGrau(self):
        matrizA: np.array = np.zeros((2, 2), np.float64)
        vetorB: np.array = np.zeros(2, np.float64)

        for i in range(2):
            for j in range(i + 1):
                coeficiente: np.float64 = np.float64(self.dados.calcularCoeficienteMatrizA(i, j))
                matrizA[i][j] = np.float64(coeficiente)

                if i != j:
                    matrizA[j][i] = np.float64(coeficiente)

            vetorB[i] = self.dados.calcularCoeficienteVetorB(i)

        return pivoteamento(matrizA, vetorB, 2)

    def calcularCoeficientesSegundoGrau(self):
        matrizA: np.array = np.zeros((3, 3), np.float64)
        vetorB: np.array = np.zeros(3, np.float64)

        for i in range(3):
            for j in range(i + 1):
                coeficiente: np.float64 = np.float64(self.dados.calcularCoeficienteMatrizA(i, j))
                matrizA[i][j] = np.float64(coeficiente)

                if i != j:
                    matrizA[j][i] = np.float64(coeficiente)

            vetorB[i] = self.dados.calcularCoeficienteVetorB(i)

        return pivoteamento(matrizA, vetorB, 3)

    def calcularErroSomaDosQuadradosFuncaoPolinomial(self, coeficientes: list[float]) -> float:
        somaDosQuadrados: float = 0

        for tempo, quantidade in zip(self.dados.tempoArray, self.dados.quantidadeArray):
            y: float = 0

            for i, coeficiente in enumerate(coeficientes):
                y += coeficiente * math.pow(tempo, i)

            somaDosQuadrados += (quantidade - y) ** 2

        return somaDosQuadrados

    def calcularErroSomaDosQuadradosFuncaoExponencial(self, coeficientes: list[float]) -> float:
        somaDosQuadrados: float = 0
        multiplicador, potencia = coeficientes

        for tempo, quantidade in zip(self.dados.tempoArray, self.dados.quantidadeArray):
            y: float = multiplicador * math.pow(math.e, potencia * tempo)

            somaDosQuadrados += (quantidade - y) ** 2
        return somaDosQuadrados

    def calcularSomaDosQuadradosDados(self) -> float:
        somaDosQuadrados: float = 0
        mediaQuantidade = np.mean(self.dados.quantidadeArray)

        for quantidade in self.dados.quantidadeArray:
            somaDosQuadrados += (quantidade - mediaQuantidade) ** 2

        return somaDosQuadrados

    def calcularR2Polinomio(self, coeficientes: list[float]) -> float:
        somaDosErrosQuadradosDados = self.calcularSomaDosQuadradosDados()
        somaDosErrosQuadradosFuncao = self.calcularErroSomaDosQuadradosFuncaoPolinomial(coeficientes)

        razao = somaDosErrosQuadradosFuncao / somaDosErrosQuadradosDados
        R2 = 1 - razao
        return R2

    def calcularR2Exponencial(self, coeficientes: list[float]) -> float:
        somaDosErrosQuadradosDados = self.calcularSomaDosQuadradosDados()
        somaDosErrosQuadradosFuncao = self.calcularErroSomaDosQuadradosFuncaoExponencial(coeficientes)

        razao = somaDosErrosQuadradosFuncao / somaDosErrosQuadradosDados
        R2 = 1 - razao
        return R2


def imprimirCoeficientes(coeficientes):
    for i, coeficiente in enumerate(coeficientes):
        print('\tβ' + str(i) + ' = ' + str(coeficiente))


if __name__ == '__main__':
    nomeArquivo = 'dados.csv'

    regressor = Regressor(nomeArquivo)
    coeficientesDadosPrimeiroGrau: list
    coeficientesDadosSegundoGrau: list
    coeficientesDadosExponencial: list = list(pivoteamento(regressor.dados.calcularMatrizALog(),
                                                      regressor.dados.calcularVetorBLog(), 2))

    coeficientesDadosExponencial[0] = math.pow(math.e, coeficientesDadosExponencial[0])

    coeficientesDadosPrimeiroGrau = list(regressor.calcularCoeficientesPrimeiroGrau())
    coeficientesDadosSegundoGrau = list(regressor.calcularCoeficientesSegundoGrau())

    R2PrimeiroGrau = regressor.calcularR2Polinomio(coeficientesDadosPrimeiroGrau)
    R2SegundoGrau = regressor.calcularR2Polinomio(coeficientesDadosSegundoGrau)
    R2Exponencial = regressor.calcularR2Exponencial(coeficientesDadosExponencial)

    """
    print('imprimindo regressões do dado: ')
    print('coeficientes do primeiro grau:')
    imprimirCoeficientes(coeficientesDadosPrimeiroGrau)
    print('\tR² = ' + str(R2PrimeiroGrau))

    print('coeficientes do segundo grau:')
    imprimirCoeficientes(coeficientesDadosSegundoGrau)
    print('\tR² = ' + str(R2SegundoGrau))

    print('coeficientes exponencial:')
    imprimirCoeficientes(coeficientesDadosExponencial)
    print('\tR² = ' + str(R2Exponencial))

    print()"""

    listaR2 = [R2PrimeiroGrau, R2SegundoGrau, R2Exponencial]

    maiorR2 = max(listaR2)

    if maiorR2 == R2PrimeiroGrau:
        print('O modelo que melhor se ajustou foi o de primeiro grau, com R² = ' + str(R2PrimeiroGrau))
    elif maiorR2 == R2SegundoGrau:
        print('O modelo que melhor se ajustou foi o de segundo grau, com R² = ' + str(R2SegundoGrau))
    elif maiorR2 == R2Exponencial:
        print('O modelo que melhor se ajustou foi o de exponencial, com R² = ' + str(R2Exponencial))
