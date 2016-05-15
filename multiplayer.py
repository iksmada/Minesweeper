import requests
from constants import ROUTE_PARTIDAS


def thread_get_data(player,partida,lista):

    if lista is None:
        raise RuntimeError('Lista compartilhada nao pode ser nula')

    ROUTE = ROUTE_PARTIDAS + '/' + str(partida) + '/' + str(player)
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
        except Exception as ex:
            print ex
            break

def thread_send_data(x,y,player,partida,action):
    ROUTE = ROUTE_PARTIDAS + '/' + str(partida)
    data = {'x':x,'y':y,'player':player,'action':action}
    try:
        for i in range(2):
            requests.post(ROUTE + '/' + str(i), data)
    except:
        print "Nao foi possivel salvar clique"

if __name__ == '__main__':
    thread_send_data(10, 10, 1, 'test3', 1)
    thread_send_data(10, 11, 1, 'test3', 1)
    thread_send_data(10, 12, 1, 'test3', 1)
    thread_get_data(0, 'test3', [])