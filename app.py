from random import randint
from time import sleep
from abc import abstractmethod
class Jogador:
    def __init__(self, nome):
        self.posicao = 0
        self.nome = nome
        self.saldo = 300
        self.perfil = None

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
            Jogador('player3'),
            Jogador('player4'),
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
    
    def start(self):
        while self.rodadas < 10:
            #contator de rodadas limetes
            self.rodadas += 1
            print(f'Rodada {self.rodadas}', end="\n\n")
            for player in self.jogadores:
                posicao = self.tabuleiro[player.posicao-1].nome if player.posicao else None
                print(f'{player.nome} posição: {posicao}')
                numero = Dado.get_numero()
                print('numero sortido', numero)
                player.posicao += numero

                #Verifica se chegou final do tabuleiro
                if player.posicao > self.qtd_casas:
                    player.posicao -= self.qtd_casas
                    player.saldo += 100

                propriedade = self.tabuleiro[player.posicao-1]
                print(f'propriedade {propriedade.nome}, dono: {propriedade.proprietario}')
                #Compra do imovel
                if not propriedade.proprietario:
                    print('compro')
                    propriedade.proprietario = player.nome
                    player.saldo -= propriedade.custo_venda
                elif propriedade.proprietario != player.nome:
                    player.saldo -= propriedade.aluguel
                    for recebedor in self.jogadores:
                        if propriedade.proprietario == recebedor.nome:
                            recebedor.saldo += propriedade.aluguel
                            print(f'pago aluguel para o {recebedor.nome}')
                    #devolver aluguel pago
                else:
                    print('minha casa vida que segue')
                print()

        print()


if __name__ == "__main__":
    game = Game()
    game.start()
