import numpy as np
import csv


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
        return [(self.tempoArray[i], self.quantidadeArray[i]) for i in range(len(self.tempoArray))]


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

                    print(i)
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


if __name__ == '__main__':
    nomeArquivo = 'dados.csv'

    regressor = Regressor(nomeArquivo)
    regressor.imprimirDados()
