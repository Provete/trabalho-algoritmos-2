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

    def calcularCoeficienteMatrizA(self, i: int, j: int):
        soma: np.int = 0
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
        print('logC: ' + str(sum(logC)))
        print('t*logC ' + str(sum(tLogC)))
        return [sum(logC), sum(tLogC)]

    def calcularTaoQuadrado(self):
        novo_vetor = []
        for tempo in self.tempoArray:
            novo_vetor.append(tempo*tempo)
        return novo_vetor

    def calcularMatrizALog(self):
        nova_matriz = np.zeros((2,2))
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
                coeficiente: np.float64 = self.dados.calcularCoeficienteMatrizA(i, j)
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
                coeficiente: np.float64 = self.dados.calcularCoeficienteMatrizA(i, j)
                matrizA[i][j] = np.float64(coeficiente)

                if i != j:
                    matrizA[j][i] = np.float64(coeficiente)

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
    coeficientesDadosExponencial: list = pivoteamento(regressor.dados.calcularMatrizALog(),
                                                      regressor.dados.calcularVetorBLog(), 2)

    coeficientesDadosExponencial[0] = math.pow(math.e, coeficientesDadosExponencial[0])


    print('imprimindo regressões do dado: ')

    coeficientesDadosPrimeiroGrau = regressor.calcularCoeficientesPrimeiroGrau()
    coeficientesDadosSegundoGrau = regressor.calcularCoeficientesSegundoGrau()

    print('coeficientes do primeiro grau:')
    imprimirCoeficientes(coeficientesDadosPrimeiroGrau)

    print('coeficientes do segundo grau:')
    imprimirCoeficientes(coeficientesDadosSegundoGrau)
    print('coeficientes exponencial:')
    imprimirCoeficientes(coeficientesDadosExponencial)