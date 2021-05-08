from random import randint
from time import sleep
from abc import abstractmethod
class Jogador():
    def __init__(self, nome):
        self.posicao = 0
        self.nome = nome
        self.saldo = 300

class Propriedade():
    def __init__(self, nome, custo_venda, aluguel):
        self.nome = nome
        self.custo_venda = custo_venda
        self.aluguel = aluguel
        self.proprietario = None

class Dado():
    def __init__(self):
        pass
    
    @abstractmethod
    def get_numero():
        return randint(1,6)

class Tabuleiro():
    pass

class Game():
    def __init__(self):
        self.jogadores = [
            Jogador('player1'),
            Jogador('player2'),
        ]
        self.jogador = Jogador('player3')
        self.tabuleiro = [Propriedade(str(x), 100, 1) for x in range (1, 21)]
        self.rodadas = 0
    
    def start(self):
        for x in range (0,10):
            # select jogador
            numero = Dado.get_numero()
            print('numero sortido', numero)
            self.jogador.posicao += numero
            if self.jogador.posicao > 20:
                self.jogador.posicao -= 20
                self.jodador.saldo += 100
            
            print(f'{self.jogador.nome} esta na casa {self.tabuleiro[self.jogador.posicao-1].nome}')
            print("\n\n")


game = Game()

game.start()