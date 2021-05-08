from random import randint
from time import sleep
from abc import abstractmethod
class Jogador:
    def __init__(self, nome, status=1):
        self.posicao = 0
        self.nome = nome
        self.saldo = 300
        self.perfil = None
        self.status = status

    def desativar(self):
        self.status = 0

    def receber(self, valor):
        self.saldo += valor

    def pagar(self, valor, recebedor):
        self.saldo -= valor
        recebedor.receber(valor)
        print(f'pago aluguel para o {recebedor.nome}, saldo: {recebedor.saldo}')

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

    def get_player(self, nome):
        for player in self.jogadores:
            if nome == player.nome:
                return player

    def zerar_jogador(self, nome):
        print(f'perdeu: {nome}')
        for propriedade in self.tabuleiro:
            if nome == propriedade.proprietario:
                propriedade.proprietario = None
        self.get_player(nome).desativar()
        if self.check_vencedor():
            raise KeyboardInterrupt

    def check_vencedor(self):
        player_on = []
        for player in self.jogadores:
            if player.status:
                player_on.append(player)
        if len(player_on) == 1:
            return player_on[0]



    def start(self):
        while self.rodadas < 100:
            try:
                self.rodadas += 1
                print(f'Rodada {self.rodadas}', end="\n\n")
                for player in self.jogadores:
                    if player.status:
                        posicao = self.tabuleiro[player.posicao-1].nome if player.posicao else None
                        print(f'{player.nome} posição: {posicao} saldo: {player.saldo}')
                        numero = Dado.get_numero()
                        print('numero sortido', numero)
                        player.posicao += numero

                        #Verifica se chegou final do tabuleiro
                        if player.posicao > self.qtd_casas:
                            player.posicao -= self.qtd_casas
                            player.saldo += 100

                        propriedade = self.tabuleiro[player.posicao-1]
                        print(f'propriedade {propriedade.nome}, dono: {propriedade.proprietario}')

                        #Compra do imovel de acordo com perfil
                        if not propriedade.proprietario:
                            if player.saldo >= propriedade.custo_venda:
                                propriedade.proprietario = player.nome
                                player.saldo -= propriedade.custo_venda

                        #Paga aluguel caso o imovel pertence a outro jogador
                        elif propriedade.proprietario != player.nome:
                            if player.saldo > propriedade.aluguel:
                                recebedor = self.get_player(propriedade.proprietario)
                                if propriedade.proprietario == recebedor.nome:
                                    player.pagar(propriedade.aluguel, recebedor)
                            #Jogador Eliminado
                            else:
                                recebedor = self.get_player(propriedade.proprietario)
                                player.pagar(player.saldo, recebedor)
                                self.zerar_jogador(player.nome)
                    print()
            except KeyboardInterrupt:
                print('Game winner')
                break

        for player in self.jogadores:
            print(f'{player.nome}: {player.saldo}')


if __name__ == "__main__":
    game = Game()
    game.start()
