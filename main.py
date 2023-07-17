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
    dados: list[Dados]

    def __init__(self, nomeArquivo: str):
        self.lerDados(nomeArquivo)

    def lerDados(self, nomeArquivo: str):
        self.dados = list()

        with open(nomeArquivo, 'r') as arquivo:
            leitor = csv.reader(arquivo, delimiter=',')

            for linha in leitor:
                i = 0
                for tempo, quantidade in [(linha[i], linha[i + 1])
                                          for i in range(0, int(len(linha)), 2)]:
                    try:
                        t = self.dados[i]
                    except IndexError:
                        self.dados.append(Dados())

                    self.dados[i].adicionarTempoEQuantidade(int(tempo), int(quantidade))
                    i = i + 1

    def imprimirDados(self):
        for dados in self.dados:
            dados.imprimirDados()

    def pegarDadosNoIndex(self, i):
        return self.dados[i].pegarDados()

    def pegarDadosEnumeradosNoIndex(self, i):
        return self.dados[i].pegarDadosEnumerados()

    def calcularCoeficientesPrimeiroGrau(self, dadoIndex):
        matrizA: np.array = np.zeros((2, 2), np.int64)
        vetorB: np.array = np.zeros(2, np.int64)

        for i in range(2):
            for j in range(i + 1):
                coeficiente: np.int64 = self.dados[dadoIndex].calcularCoeficienteMatrizA(i, j)
                matrizA[i][j] = np.int64(coeficiente)

                if i != j:
                    matrizA[j][i] = np.int64(coeficiente)

            vetorB[i] = self.dados[dadoIndex].calcularCoeficienteVetorB(i)

        return pivoteamento(matrizA, vetorB, 2)

    def calcularCoeficientesSegundoGrau(self, dadoIndex):
        matrizA: np.array = np.zeros((3, 3), np.int64)
        vetorB: np.array = np.zeros(3, np.int64)

        for i in range(3):
            for j in range(i + 1):
                coeficiente: np.int64 = self.dados[dadoIndex].calcularCoeficienteMatrizA(i, j)
                matrizA[i][j] = np.int64(coeficiente)

                if i != j:
                    matrizA[j][i] = np.int64(coeficiente)

            vetorB[i] = self.dados[dadoIndex].calcularCoeficienteVetorB(i)

        return pivoteamento(matrizA, vetorB, 3)

    def pegarQuantidadeDados(self):
        return len(self.dados)


def imprimirCoeficientes(coeficientes):
    for i, coeficiente in enumerate(coeficientes):
        print('\tβ' + str(i) + ' = ' + str(coeficiente))


if __name__ == '__main__':
    nomeArquivo = 'dados.csv'

    regressor = Regressor(nomeArquivo)
    coeficientesDadosPrimeiroGrau: list = list()
    coeficientesDadosSegundoGrau: list = list()
    coeficientesDadosExponencial: list = list()

    for i in range(regressor.pegarQuantidadeDados()):
        print(str(i+1) + 'ª Tabela de Dados:')

        coeficientesDadosPrimeiroGrau.append(regressor.calcularCoeficientesPrimeiroGrau(i))
        coeficientesDadosSegundoGrau.append(regressor.calcularCoeficientesSegundoGrau(i))

        print('coeficientes do primeiro grau:')
        imprimirCoeficientes(coeficientesDadosPrimeiroGrau[i])

        print('coeficientes do segundo grau:')
        imprimirCoeficientes(coeficientesDadosSegundoGrau[i])

        print()
