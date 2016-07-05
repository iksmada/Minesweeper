# -*- coding: utf-8

import requests
import time
from ast import literal_eval

from constants import *
from classes import GameController

"""
    Arquivo que contém métodos auxiliares para partidas multiplayer
"""

def get_tabuleiro_from_server():
    """
        Método que obtém o tabuleiro de uma partida do servidor
    :param partida: ID da partida
    :return: string com a informação do tabuleiro
    """
    ROUTE = ROUTE_TABULEIROS + '/' + str(GameController.match_ID)
    # Envia a informação de linhas, colunas e porcentagem de bombas para criação ou verificação
    data = {'rows':GameController.rows,'cols':GameController.columns,'bombs':GameController.bombs}
    try:
        requests.post(ROUTE,data)
        result = requests.get(ROUTE).content
        if result is not None and len(result) > 0:
            result = literal_eval(result)
            return result['tabuleiro']
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def create_new_tabuleiro_on_server():
    """
        Método que gera um novo tabuleiro no servidor
    :param partida: string com o criador da partida
    :return: nada
    """

    # Servidor sempre muda o tabuleiro quando pelo menos uma das variaveis mudam

    # Muda o número de bombas
    GameController.bombs += 1
    get_tabuleiro_from_server()
    # Retorna o número de bombas
    GameController.bombs -= 1
    try:
        return get_tabuleiro_from_server()
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def get_player_ID():
    """
        Método que obtém o ID do jogador para uso interno (ex: 0, 1, 2, ...)
    :param player: string com o username do jogador
    :param partida: string com o nome da partida (username do criador da partida)
    :return: id do usuário para esta partida
    """
    ROUTE = ROUTE_JOGADORES + '/' + str(GameController.match_ID)
    dados = {'player':GameController.username}

    try:
        ID = requests.post(ROUTE, dados).content
        return int(ID)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def set_up_new_match():
    """
        Método que registra uma nova partida multiplayer no servidor
    :param partida: string com o nome da partida
    :return: nada
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match_ID)

    try:
        requests.post(ROUTE, GameController.match_ID)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def start_match():
    """
        Método que registra o início de uma partida no servidor
    :param partida: string com o nome da partida
    :return: nada
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match_ID)

    try:
        requests.delete(ROUTE)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def wait_match_to_begin():
    """
        Método que 'trava' o jogo até que o criador da partida inicie-a
    :param partida: string com o nome da partida
    :return: nada
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match_ID)

    try:
        response = requests.get(ROUTE).content
        if len(response) == 2:
            return 1
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')
    # Checa a cada 100ms
    time.sleep(0.1)
    return 0

def check_match_has_begun():
    """
        Método que verifica se uma partida já começou
    :param partida: string com o nome da partida
    :return: verdadeiro ou falso
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match_ID)

    try:
        response = requests.get(ROUTE).content
        if len(response) == 2:
            return True
        else:
            return False
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def thread_get_data(player,partida,lista):
    """
        Thread que carrega informações de cliques de uma partida e passa para uma lista compartilhada
    :param player: string com username do jogador
    :param partida: string com nome da partida
    :param lista: lista compartilhada
    :return: nada
    """
    if lista is None:
        raise RuntimeError('Lista compartilhada não pode ser nada')

    ROUTE = ROUTE_JOGADAS + '/' + str(partida) + '/' + str(player)
    while True:

        # Condição para terminar a thread
        # Primeiro elemento da lista compartilhada é um booleano qualquer
        if len(lista) > 0 and type(lista[0]) is bool:
            break

        try:
            # Obtém último clique
            result = requests.get(ROUTE).content
            # Se existe último clique
            if result is not None and len(result) > 2:
                # Obtém informação do clique
                params = literal_eval(result)
                # Remove último clique da lista
                requests.delete(ROUTE)
                if str(params['player']) != str(player):
                    print params
                    # Adiciona na lista compartilhada
                    lista.append((params['x'], params['y'], params['color'], params['action']))
        except:
            raise RuntimeError('Não foi possivel conectar no servidor')

        # Verifica a cada 100ms
        time.sleep(0.1)

def thread_send_data(x,y,player,partida,color,action):
    """
        Thread que envia a informação de um clique ao servidor
    :param x: coordenada x do tabuleiro
    :param y: coordenada y do tabuleiro
    :param player: ID interno do jogador que clicou
    :param partida: nome da partida
    :param color: cor da bandeira do jogador
    :param action: ID da ação (revelar, marcar com bandeira, ...)
    :return: nada
    """
    ROUTE = ROUTE_JOGADAS + '/' + str(partida)
    data = {'x':x,'y':y,'player':player,'color':color,'action':action}
    try:
        # Envia para todos os jogadores de 0 a 4
        for i in range(5):
            requests.post(ROUTE + '/' + str(i), data)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def get_global_score():

    ROUTE = ROUTE_GLOBAL_SCORE

    try:
        result = requests.get(ROUTE).content
        if result is not None and len(result) > 0:
            return literal_eval(result)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def register_global_score():

    ROUTE = ROUTE_GLOBAL_SCORE
    data = {'username':     GameController.username,
            'rows':         GameController.rows,
            'cols':         GameController.columns,
            'bombs':        GameController.bombs_percentage,
            'score':        GameController.score,
            'movs':         GameController.movs}

    try:
        requests.post(ROUTE, data)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')


if __name__ == '__main__':
    thread_send_data(10, 10, 1, 'test3', 1)
    thread_send_data(10, 11, 1, 'test3', 1)
    thread_send_data(10, 12, 1, 'test3', 1)
    thread_get_data(0, 'test3', [])