import firebase
import time
from constants import *

def get_data(player,partida,lista):

    firebase_ref = firebase.FirebaseApplication(PARTIDA_URL,None)
    while True:

        if len(lista) > 0 and type(lista[0]) is bool:
            break

        try:
            result = firebase_ref.get('jogo/partidas/', str(partida) + '/' + str(player),
                                      params={'orderBy':'"$key"','limitToFirst':1})
            if result is not None:
                entry = result.keys()[0]
                click = result[entry]
                result = firebase_ref.delete('jogo/partidas/',
                                             str(partida) + '/' + str(player)+ '/' + entry,
                                             params={'print':'silent'})
                if click['player'] != str(player):
                    print click
                    lista.append((click['x'], click['y']))
        except Exception as ex:
            print ex
            break

def send_data(x,y,player,partida,action):
    firebase_ref = firebase.FirebaseApplication(PARTIDA_URL, None)
    try:
        for i in range(2):
            firebase_ref.post('jogo/partidas/' + str(partida) + '/' + str(i),
                          {'x':x, 'y':y, 'action':action,'player':player},
                          params={'print':'silent'})
    except:
        print "Nao foi possivel salvar clique"