from random import randint
from time import sleep
from abc import abstractmethod
class Jogador:
    def __init__(self, nome):
        self.posicao = 0
        self.nome = nome
        self.saldo = 300

class Propriedade:
    def __init__(self, nome, custo_venda, aluguel):
        self.nome = nome
        self.custo_venda = custo_venda
        self.aluguel = aluguel
        self.proprietario = None

class Dado:
    def __init__(self):
        pass
    
    @abstractmethod
    def get_numero():
        return randint(1, 6)

class Tabuleiro:
    pass

class Game:
    def __init__(self):
        self.jogadores = [
            Jogador('player1'),
            Jogador('player2'),
        ]

        # Carrega lista de propriedades de um csv e monta o tabuleiro
        self.tabuleiro = list()
        with open('propriedades.csv', 'r') as file:
            for propriedade in file.readlines():
                aux = propriedade.replace('\n', '').split(',')
                self.tabuleiro.append(
                    Propriedade(
                        nome=aux[0],
                        custo_venda=int(aux[1]),
                        aluguel=int(aux[2])
                    )
                )
        self.rodadas = 0
        self.qtd_casas = len(self.tabuleiro)
        print(self.qtd_casas)
    
    def start(self):
        while self.rodadas < 10:
            #contator de rodadas limetes
            self.rodadas += 1
            for player in self.jogadores:
                numero = Dado.get_numero()
                print('numero sortido', numero)
                player.posicao += numero
                if player.posicao > self.qtd_casas:
                    player.posicao -= self.qtd_casas
                    player.saldo += 100

                print(f'{player.nome} esta na casa {self.tabuleiro[player.posicao-1].nome}')
                print(f'rodada {self.rodadas}')
                print("\n\n")



game = Game()

game.start()
