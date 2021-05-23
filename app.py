from random import randint, getrandbits
import statistics
from perfil import *


estatistica = {
    'timeout': 0,
    'ultima_rodada': [],
}

players = [
    {'nome': 'player1', 'win': 0, 'comportamento': 'impulsivo'},
    {'nome': 'player2', 'win': 0, 'comportamento': 'exigente'},
    {'nome': 'player3', 'win': 0, 'comportamento': 'cauteloso'},
    {'nome': 'player4', 'win': 0, 'comportamento': 'aleatorio'}
]


class Jogador:
    def __init__(self, nome,estrategia, status=1):
        """
        Instancia a classe jogador.

        :param nome:
        :param status:
        :param perfil:
        """
        self.posicao = 0
        self.nome = nome
        self.saldo = 300
        self.status = status
        self.estrategia = estrategia

    def desativar(self):
        """
        Desativa jogador na partida.

        :return:
        """
        self.status = 0

    def receber(self, valor):
        """
        Receber aluguel de alguma propriedade que possue.

        :param valor:
        :return:
        """
        self.saldo += valor

    def pagar(self, valor, recebedor):
        """
        Efetua o pagamento do aluguel.

        :param valor:
        :param recebedor:
        :return:
        """
        self.saldo -= valor
        recebedor.receber(valor)
        print(
            f'pago aluguel para o {recebedor.nome}, saldo: {recebedor.saldo}'
        )


class Propriedade:
    def __init__(self, nome, custo_venda, aluguel):
        """
        Instancia a classe Propriedade.

        :param nome:
        :param custo_venda:
        :param aluguel:
        """
        self.nome = nome
        self.custo_venda = custo_venda
        self.aluguel = aluguel
        self.proprietario = None


class Dado:
    @staticmethod
    def get_numero():
        return randint(1, 6)


class Game:
    def __init__(self):
        """
        Instancia configurações para inicio da partida.
        """
        self.jogadores = [
            Jogador(nome='player1', estrategia=impulsivo),
            Jogador(nome='player2', estrategia=exigente),
            Jogador(nome='player3', estrategia=cauteloso),
            Jogador(nome='player4', estrategia=aleatorio),
        ]
        self.timeout = 1

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
        """
        Efetua a busca de um jogador.

        :param nome:
        :return:
        """
        for player in self.jogadores:
            if nome == player.nome:
                return player

    def zerar_jogador(self, nome):
        """
        Zera um jogador na partida desativando
        status e removendo as propriedades.

        :param nome:
        :return:
        """
        print(f'perdeu: {nome}')
        for propriedade in self.tabuleiro:
            if nome == propriedade.proprietario:
                propriedade.proprietario = None
        self.get_player(nome).desativar()
        if self.check_vencedor():
            raise KeyboardInterrupt

    def check_vencedor(self):
        """
        Verifica se tem apenas um jogador ativo
        na partida para identificar o vencedor.

        :return:
        """
        player_on = []
        for player in self.jogadores:
            if player.status:
                player_on.append(player)
        if len(player_on) == 1:
            return player_on[0]

    def comprar_propriedade(self, player, propriedade):
        """
        Efetura a compra da propridade.

        :param player:
        :param propriedade:
        :return:
        """
        if player.saldo >= propriedade.custo_venda:
            if player.estrategia(player=player, propriedade=propriedade):
                propriedade.proprietario = player.nome
                player.saldo -= propriedade.custo_venda
                return True
        return False

    def start(self):
        """
        Inicia o jogo.

        :return:
        """
        while self.rodadas < 1000:
            try:
                self.rodadas += 1
                print(f'Rodada {self.rodadas}', end="\n\n")
                for player in self.jogadores:
                    if player.status:
                        posicao = self.tabuleiro[player.posicao-1].nome if player.posicao else None
                        print(
                            f'{player.nome} posição: {posicao} saldo: {player.saldo}'
                        )
                        numero = Dado.get_numero()
                        print('numero sortido', numero)
                        player.posicao += numero

                        # Verifica se chegou final do tabuleiro
                        if player.posicao > self.qtd_casas:
                            player.posicao -= self.qtd_casas
                            player.saldo += 100

                        propriedade = self.tabuleiro[player.posicao-1]
                        print(
                            f'propriedade {propriedade.nome}, dono: {propriedade.proprietario}'
                        )

                        # Compra do imovel de acordo com perfil
                        if not propriedade.proprietario:
                            # Aplica pattern strategy
                            self.comprar_propriedade(player=player, propriedade=propriedade)

                        # Paga aluguel caso o imovel pertence a outro jogador
                        elif propriedade.proprietario != player.nome:
                            if player.saldo > propriedade.aluguel:
                                recebedor = self.get_player(propriedade.proprietario)
                                if propriedade.proprietario == recebedor.nome:
                                    player.pagar(propriedade.aluguel, recebedor)
                            # Jogador Eliminado
                            else:
                                recebedor = self.get_player(propriedade.proprietario)
                                player.pagar(player.saldo, recebedor)
                                self.zerar_jogador(player.nome)
            except KeyboardInterrupt:
                self.timeout = 0
                break

        global estatistica, players

        ganhador = max(self.jogadores, key=lambda jogador: jogador.saldo)

        for player in players:
            if player['nome'] == ganhador.nome:
                player['win'] += 1
                break

        estatistica['timeout'] += self.timeout
        estatistica['ultima_rodada'].append(self.rodadas)


if __name__ == "__main__":
    qtd_games = 300
    for x in range(qtd_games):
        game = Game()
        game.start()

    print("********** ESTATÍSTICAS **********", end='\n\n')

    # QUANTAS PARTIDAS TERMINAM POR TIMEOUT
    print(f"***** Quantidade de Timeout ***** \n {estatistica['timeout']}", end='\n\n')

    # QUANTOS TURNO EM MÉDIA DEMORA UMA PARTIDA
    print(f"***** Média de rodadas ***** \n {statistics.mean(estatistica['ultima_rodada'])}")

    # QUAL A PORCENTAGEM DE VITÓRIAS POR COMPORTAMENTO
    comportamentos = list(map(lambda player: f"{player['comportamento']} {(player['win'] / qtd_games) * 100:.2f}% de vitoria", players))

    print("\n ***** Porcentagem de vitórias por comportamento *****", end='\n\n')
    for comportamento in comportamentos:
        print(comportamento)

    vencedor = max(players, key=lambda player: player['win'])
    # QUAL COMPORTAMENTO MAIS VENCEU
    print("\n ***** Qual comportamento mais vence *****")
    print(vencedor.get('comportamento'))
