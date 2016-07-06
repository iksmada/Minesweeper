# -*- coding: utf-8

import requests
import time
from ast import literal_eval

from constants import *
from classes import GameController

"""
    Script que contém métodos auxiliares para partidas multiplayer
"""

def get_tabuleiro_from_server():
    """
        Método que obtém o tabuleiro de uma partida do servidor
    :return: string com a informação do tabuleiro
    """
    return get_board(False)

def create_new_tabuleiro_on_server():
    """
        Método que gera um novo tabuleiro no servidor
    :return: nada
    """
    return get_board(True)

def get_board(new=False):
    """
        Método auxiliar para criar ou pegar um tabuleiro do servidor
    :param new: indica se uma novo tabuleiro deve ser criado
    :return: tabuleiro criado ou pegado do servidor
    """

    ROUTE = ROUTE_TABULEIROS + '/' + str(GameController.match)
    # Envia a informação de linhas, colunas e porcentagem de bombas para criação ou verificação
    data = {'rows':GameController.rows, 'cols':GameController.columns, 'bombs':GameController.bombs_percentage, 'new':new}
    try:
        # Se um novo tabuleiro precisa ser criado
        if new:
            requests.post(ROUTE, data)

        result = requests.get(ROUTE).content
        if result is not None and len(result) > 0:
            # Converte string para dicionário
            result = literal_eval(result)
            # Retorna o tabuleiro e suas dimensões
            return result['tabuleiro'], result['rows'], result['cols'], result['bombs']
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def get_player_ID():
    """
        Método que obtém o ID do jogador para uso interno (ex: 0, 1, 2, ...)
    :return: id do usuário para esta partida
    """
    ROUTE = ROUTE_JOGADORES + '/' + str(GameController.match)
    dados = {'player':GameController.username}

    try:
        ID = requests.post(ROUTE, dados).content
        return int(ID)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def set_up_new_match():
    """
        Método que registra uma nova partida multiplayer no servidor
    :return: nada
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match)
    dados = {'connect':True}

    try:
        requests.post(ROUTE, dados)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def delete_match():
    """
        Método que registra o início de uma partida no servidor
    :return: nada
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match)

    try:
        requests.delete(ROUTE)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def start_match():
    """
        Método que registra uma nova partida multiplayer no servidor
    :return: nada
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match)
    dados = {'connect':False}

    try:
        requests.post(ROUTE, dados)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def get_match_status():
    """
        Método que verifica se uma partida começou ou terminou (com delay)
    :return: 0 se não começou, 1 se começou ou -1 se terminou
    """
    ROUTE = ROUTE_PARTIDAS + '/' + str(GameController.match)

    try:
        response = requests.get(ROUTE).content
        if len(response) == 2:
            return -1
        else:
            try:
                response = literal_eval(response)
                if 'connect' in response:
                    if response['connect'] == 'True':
                        return 1
                    elif response['connect'] == 'False':
                        return 0
            except:
                pass
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

    return -1

def check_match_has_begun():
    """
        Método que verifica se uma partida já começou (sem delay)
    :return: verdadeiro ou falso
    """
    return get_match_status() <= 0

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
                    # Adiciona clique na lista compartilhada
                    lista.append((params['x'], params['y'], params['color'], params['action']))
        except:
            raise RuntimeError('Não foi possivel conectar no servidor')

        # Verifica a cada 100ms
        time.sleep(0.1)

def thread_send_data(x,y,player,partida,color,action):
    """
        Thread que envia a informação de um clique ao servidor
    :param x:       coordenada x do tabuleiro
    :param y:       coordenada y do tabuleiro
    :param player:  ID interno do jogador que clicou
    :param partida: nome da partida
    :param color:   cor da bandeira do jogador
    :param action:  ID da ação (revelar, marcar com bandeira, ...)
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

    """
        Método que obtém o score de partidas single player
    :return: retorna uma lista ordenada dos cinco melhores scores registrados no servidor
    """
    ROUTE = ROUTE_GLOBAL_SCORE

    try:
        result = requests.get(ROUTE).content
        if result is not None and len(result) > 0:
            return literal_eval(result)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def register_global_score():
    """
        Método que registra um novo score no servidor
    :return: nada
    """
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

def get_match_score():
    """
        Método que obtém o score de uma partida multiplayer
    :return: retorna uma lista ordenada dos scores registrados no servidor
    """
    ROUTE = ROUTE_SCORE + '/' + str(GameController.match)

    try:
        result = requests.get(ROUTE).content
        if result is not None and len(result) > 0:
            return literal_eval(result)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def get_match_players():
    """
        Método que obtém todos os nomes de usuários de uma partida multiplayer
    :return: lista com todos os usernames
    """
    ROUTE = ROUTE_JOGADORES + '/' + str(GameController.match)

    try:
        result = requests.get(ROUTE).content
        if result is not None and len(result) > 0:
            return literal_eval(result)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')

def register_match_score():
    """
        Método que registra um novo score de uma partida multiplayer no servidor
    :return: nada
    """
    ROUTE = ROUTE_SCORE + '/' + str(GameController.match)
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

def delete_match_score():
    """
        Método que remove a informação de score de uma partida multiplayer do servidor
    :return: nada
    """
    ROUTE = ROUTE_SCORE + '/' + str(GameController.match)

    try:
        requests.delete(ROUTE)
    except:
        raise RuntimeError('Não foi possivel conectar no servidor')
