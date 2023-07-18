import math

import numpy as np
import csv
from escalonador import pivoteamento


class Dados:
    tempoArray: list
    quantidadeArray: list

    def __init__(self):
        self.tempoArray = list()
        self.quantidadeArray = list()

    def adicionarTempoEQuantidade(self, novoTempo: int, novaQuantidade: int):
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

    def calcularCoeficienteMatrizA(self, i: int, j: int):
        soma: np.int64 = 0
        for tempo in self.tempoArray:
            soma += np.int64(math.pow(tempo, i + j))

        return soma

    def calcularCoeficienteVetorB(self, i: int):
        soma: np.int64 = 0

        for tempo, quantidade in zip(self.tempoArray, self.quantidadeArray):
            soma += np.int64(quantidade) * np.int64(math.pow(tempo, i))

        return soma


class Regressor:
    dados: Dados

    def __init__(self, nomeArquivo: str):
        self.lerDados(nomeArquivo)

    def lerDados(self, nomeArquivo: str):
        self.dados = Dados()

        with open(nomeArquivo, 'r') as arquivo:
            leitor = csv.reader(arquivo, delimiter=',')

            for linha in leitor:
                tempo = int(linha[0])
                quantidade = int(linha[1])
                self.dados.adicionarTempoEQuantidade(tempo, quantidade)

    def calcularCoeficientesPrimeiroGrau(self):
        matrizA: np.array = np.zeros((2, 2), np.int64)
        vetorB: np.array = np.zeros(2, np.int64)

        for i in range(2):
            for j in range(i + 1):
                coeficiente: np.int64 = self.dados.calcularCoeficienteMatrizA(i, j)
                matrizA[i][j] = np.int64(coeficiente)

                if i != j:
                    matrizA[j][i] = np.int64(coeficiente)

            vetorB[i] = self.dados.calcularCoeficienteVetorB(i)

        return pivoteamento(matrizA, vetorB, 2)

    def calcularCoeficientesSegundoGrau(self):
        matrizA: np.array = np.zeros((3, 3), np.int64)
        vetorB: np.array = np.zeros(3, np.int64)

        for i in range(3):
            for j in range(i + 1):
                coeficiente: np.int64 = self.dados.calcularCoeficienteMatrizA(i, j)
                matrizA[i][j] = np.int64(coeficiente)

                if i != j:
                    matrizA[j][i] = np.int64(coeficiente)

            vetorB[i] = self.dados.calcularCoeficienteVetorB(i)

        return pivoteamento(matrizA, vetorB, 3)


def imprimirCoeficientes(coeficientes):
    for i, coeficiente in enumerate(coeficientes):
        print('\tβ' + str(i) + ' = ' + str(coeficiente))


if __name__ == '__main__':
    nomeArquivo = 'dados.csv'

    regressor = Regressor(nomeArquivo)
    coeficientesDadosPrimeiroGrau: list
    coeficientesDadosSegundoGrau: list
    coeficientesDadosExponencial: list

    print('imprimindo regressões do dado: ')

    coeficientesDadosPrimeiroGrau = regressor.calcularCoeficientesPrimeiroGrau()
    coeficientesDadosSegundoGrau = regressor.calcularCoeficientesSegundoGrau()

    print('coeficientes do primeiro grau:')
    imprimirCoeficientes(coeficientesDadosPrimeiroGrau)

    print('coeficientes do segundo grau:')
    imprimirCoeficientes(coeficientesDadosSegundoGrau)
