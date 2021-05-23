from random import getrandbits

def impulsivo(player, propriedade):
    return True

def exigente(player, propriedade):
    if propriedade.aluguel > 50:
        return True

def cauteloso(player, propriedade):
    if (player.saldo - propriedade.custo_venda) >= 80:
        return True

def aleatorio(player, propriedade):
    if bool(getrandbits(1)):
        return True
