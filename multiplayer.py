import requests
import time
from constants import *
from classes import GameController


def get_tabuleiro_from_server(partida):

    ROUTE = ROUTE_TABULEIROS + '/' + str(partida)
    tabuleiro = ''
    data = {'rows':GameController.rows,'cols':GameController.columns,'bombs':GameController.bombs}
    try:
        requests.post(ROUTE,data)
        result = requests.get(ROUTE).content
        if result is not None and len(result) > 0:
            for par in result.split('&'):
                par = str(par).split('=')
                if str(par[0]) == 'tabuleiro':
                    tabuleiro = str(par[1])
    except:
        raise RuntimeError('Nao foi possivel conectar no servidor')

    return tabuleiro

def create_new_tabuleiro_on_server(partida):

    # Tabuleiro sempre muda quando pelo menos uma das variaveis muda
    GameController.bombs += 1
    get_tabuleiro_from_server(partida)

    GameController.bombs -= 1
    try:
        return get_tabuleiro_from_server(partida)
    except:
        raise RuntimeError('Nao foi possivel conectar no servidor')

def get_player_ID(player,partida):
    ROUTE = ROUTE_JOGADORES + '/' + str(partida)
    dados = {'player':player}

    try:
        ID = requests.post(ROUTE, player).content
        return int(ID)
    except:
        raise RuntimeError('Nao foi possivel conectar no servidor')

def set_up_new_match(partida):
    ROUTE = ROUTE_PARTIDAS + '/' + str(partida)

    try:
        requests.post(ROUTE, partida)
    except:
        raise RuntimeError('Nao foi possivel conectar no servidor')

def start_match(partida):
    ROUTE = ROUTE_PARTIDAS + '/' + str(partida)

    try:
        requests.delete(ROUTE, partida)
    except:
        raise RuntimeError('Nao foi possivel conectar no servidor')

def wait_match_to_begin(partida):
    ROUTE = ROUTE_PARTIDAS + '/' + str(partida)

    while True:
        try:
            response = requests.get(ROUTE, partida).content
            if len(response) == 0:
                break
        except:
            raise RuntimeError('Nao foi possivel conectar no servidor')

        time.sleep(0.1)


def thread_get_data(player,partida,lista):

    if lista is None:
        raise RuntimeError('Lista compartilhada nao pode ser nula')

    ROUTE = ROUTE_JOGADAS + '/' + str(partida) + '/' + str(player)
    while True:

        if len(lista) > 0 and type(lista[0]) is bool:
            break


        try:
            result = requests.get(ROUTE).content
            params = {}
            if result is not None and len(result) > 0:
                for par in result.split('&'):
                    par = str(par).split('=')
                    params[str(par[0])] = str(par[1])
                requests.delete(ROUTE)
                if str(params['player']) != str(player):
                    print params
                    lista.append((params['x'], params['y'], params['action']))
        except:
            raise RuntimeError('Nao foi possivel conectar no servidor')

        time.sleep(0.1)

def thread_send_data(x,y,player,partida,action):
    ROUTE = ROUTE_JOGADAS + '/' + str(partida)
    data = {'x':x,'y':y,'player':player,'action':action}
    try:
        for i in range(5):
            requests.post(ROUTE + '/' + str(i), data)
    except:
        raise RuntimeError('Nao foi possivel conectar no servidor')

if __name__ == '__main__':
    thread_send_data(10, 10, 1, 'test3', 1)
    thread_send_data(10, 11, 1, 'test3', 1)
    thread_send_data(10, 12, 1, 'test3', 1)
    thread_get_data(0, 'test3', [])