# -*- coding: utf-8

import datetime
import random
import time

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from constants import SERVER_PORT

server_data = {'jogos':{}, 'score':[]}
last_timestamp = 0

"""
    Servidor de partidas multiplayer
"""

def clean_path(path):
    """
        Método que faz parse da rota REST e transforma em uma lista
    :param path:
    :return:
    """
    path = path.strip().split('/')
    # Remove string vazias
    path = [x for x in path if x]
    return path

def compute_total(rows, cols, bombs, score, movs):
    """
        Método que calcula o score final de uma partida single player oy multiplayer
    :param rows:    número de linhas
    :param cols:    número de colunas
    :param bombs:   porcentagem (de 0 à 100) de bombas
    :param score:   score da partida
    :param movs:    número de movimentos da partida
    :return: score final calculado
    """
    bonus = min(10, rows * cols / 50 - 1)
    return score * (100 + bonus - max(0, movs - bombs)) / 100

# Rotas acessíveis
accepted_services = ['jogos','global']
# Sub-rotas acessíveis
accepted_route = {'jogos':['jogadas','partidas', 'tabuleiros', 'jogadores','score','segredo'],
                  'global':['score']}


class MineSweeperServer(BaseHTTPRequestHandler):
    """
        Servidor REST (HTTP) para partidas multiplayer
    """
    __version__ = '3.14'
    server_version = "MineSweeperHTTP/" + __version__

    # Remova esse método para ver todas as requests HTTP chegando
    def log_message(self, f, *args):
        pass

    def check_path(self,path):
        """
            Método que verifica se caminho desejado no servidor é válido
        :param path: lista com o caminho a ser percorrido
        :return: verdadeiro ou falso
        """
        # Verifica se tamanho é válido. Caso contrário, retorna o status do servidor
        if len(path) < 2:
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Running :)')
            return False
        # Verifica se é um serviço válido no servidor
        if path[0] not in accepted_services:
            self.send_response(503)
            self.end_headers()
            self.wfile.write('Unknown service')
            return False
        # Verifica se é um sub-serviço válido no servidor
        if len(path) >= 2 and path[1] not in accepted_route[path[0]]:
            self.send_response(503)
            self.end_headers()
            self.wfile.write('Unknown access route')
            return False

        return True

    def do_GET(self):
        """
            Método que responde a requisições GET
        :return:
        """
        # Atualiza último acesso
        global last_timestamp
        last_timestamp = time.time()

        # Converte endereço da request HTTP para uma lista
        path = clean_path(self.path)

        # Verifica se endereço representa uma rota válida
        if not self.check_path(path):
            return

        # Retorna a lista de score global
        if len(path) >= 2 and path[0] == 'global' and path[1] == 'score':
            self.send_response(200)
            self.end_headers()
            if 'score' in server_data:
                self.wfile.write(str(server_data['score']))
            else:
                self.wfile.write('[]')
            return

        path = path[1:]

        if path[0] == 'jogadas':
            OPERATION = 1
        elif path[0] == 'tabuleiros':
            OPERATION = 2
        elif path[0] == 'partidas':
            OPERATION = 3
        elif path[0] == 'jogadores':
            OPERATION = 4
        elif path[0] == 'score':
            OPERATION = 5
        elif path[0] == 'segredo':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(server_data))
            return
        else:
            OPERATION = 0

        # Percorre informações no servidor (por meio de dicionários)
        last_dict = server_data['jogos']
        while len(path) > 0:
            if path[0] in last_dict:
                last_dict = last_dict[path[0]]
            else:
                last_dict[path[0]] = {}
                last_dict = last_dict[path[0]]

            path = path[1:]

        response = ''
        if OPERATION == 1:
            # Retorna a informação do clique mais antigo ao usuário
            try:
                chave_mais_antiga = sorted(last_dict.keys())[0]
                last_dict = last_dict[chave_mais_antiga]
            except:
                last_dict = {} # Dict está vazio
        # Retorna uma representação literal do último dicionário
        if OPERATION in {1, 2, 3}:
            response = str(last_dict)
        # Retorna uma representação literal da lista de usuários
        elif OPERATION == 4:
            try:
                response = str(last_dict.keys())
            except:
                response = str([])
        # Retorna uma representação literal da lista de scores registrada
        elif OPERATION == 5:
            try:
                response = str(last_dict['score'])
            except:
                response = str([])

        # Termina request
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)
        return

    def do_POST(self):
        """
            Método que responde a requisições POST
        :return:
        """
        # Atualiza último acesso
        global last_timestamp
        last_timestamp = time.time()

        path = clean_path(self.path)

        if not self.check_path(path):
            return

        # Obtém a informação que chegaram por meio da requisição
        content_length = int(self.headers.getheader('content-length', 0))
        POST_data = self.rfile.read(content_length)

        # Registra um novo score global no servidor
        if len(path) >= 2 and path[0] == 'global' and path[1] == 'score':
            temp_dict = {}
            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                temp_dict[str(par[0])] = str(par[1])

            try:
                rows = int(temp_dict['rows'])
                cols = int(temp_dict['cols'])
                bombs = int(temp_dict['bombs'])
                score = int(temp_dict['score'])
                movs = int(temp_dict['movs'])
                username = temp_dict['username']
                total = compute_total(rows, cols, bombs, score, movs)
                tupla = (total, username, rows, cols, bombs, score, movs)

                # Adiciona novo score à lista, ordena novamente e pega os cinco melhores resultados
                server_data['score'].append(tupla)
                server_data['score'].sort(reverse=True)
                if len (server_data['score']) > 5:
                    server_data['score'] = server_data['score'][:5]
            except:
                self.send_response(406)
                self.end_headers()
                self.wfile.write('Invalid parameters')
                return

        path = path[1:]

        if len(path) == 0:
            OPERATION = 0
        elif path[0] == 'jogadas':
            OPERATION = 1
        elif path[0] == 'tabuleiros':
            OPERATION = 2
        elif path[0] == 'partidas':
            OPERATION = 3
        elif path[0] == 'jogadores':
            OPERATION = 4
        elif path[0] == 'score':
            OPERATION = 5
        else:
            OPERATION = 0

        # Percorre servidor até o último dicionário
        last_dict = server_data['jogos']
        while len(path) > 0:
            if path[0] in last_dict:
                last_dict = last_dict[path[0]]
            else:
                last_dict[path[0]] = {}
                last_dict = last_dict[path[0]]

            path = path[1:]

        if OPERATION == 1:
            # Registra um novo clique no servidor
            instante = datetime.datetime.now()
            chave_instante = str(instante).replace('.', ':')
            last_dict[chave_instante] = {}
            last_dict = last_dict[chave_instante]

            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                last_dict[str(par[0])] = str(par[1])
        elif OPERATION == 2:
            # Registra um novo tabuleiro (se configurado corretamente)
            temp_dict = {}
            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                temp_dict[str(par[0])] = str(par[1])

            try:
                rows = int(temp_dict['rows'])
                cols = int(temp_dict['cols'])
                bombs = int(temp_dict['bombs'])
                new = bool(temp_dict['new'])
            except:
                self.send_response(406)
                self.end_headers()
                self.wfile.write('Invalid parameters')
                return

            if not new:
                self.send_response(406)
                self.end_headers()
                self.wfile.write('Invalid parameters')
                return

            tabuleiro = ('0'*cols)*rows
            i = 0
            while i < bombs:
                r = random.randrange(rows)
                c = random.randrange(cols)
                if tabuleiro[r*cols + c] == '0':
                    tabuleiro = tabuleiro[:r*cols + c] + '1' + tabuleiro[r*cols + c + 1:]
                    i += 1

            if 'tabuleiro' not in last_dict \
                    or last_dict['soma'] != rows + cols + bombs\
                    or last_dict['mult'] != rows * cols * bombs:
                last_dict['tabuleiro'] = tabuleiro
                # Assinatura do tabuleiro para verificação de mudança
                last_dict['soma'] = rows + cols + bombs
                last_dict['mult'] = rows * cols * bombs
                last_dict['rows'] = rows
                last_dict['cols'] = cols
                last_dict['bombs'] = bombs
        elif OPERATION == 3:
            # Registra que partida é conectável ou não
            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                last_dict[str(par[0])] = str(par[1])
        elif OPERATION == 4:
            # Registra um novo jogador em uma partida
            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                if par[0] == 'player':
                    if len(last_dict) == 0:
                        last_dict[par[1]] = 0
                    elif par[1] not in last_dict.keys():
                        last_dict[par[1]] = max(last_dict.values()) + 1

                    response = last_dict[par[1]]
        elif OPERATION == 5:
            # Registra um novo score em uma partida
            if 'score' not in last_dict:
                last_dict['score'] = []

            temp_dict = {}
            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                temp_dict[str(par[0])] = str(par[1])

            try:
                rows = int(temp_dict['rows'])
                cols = int(temp_dict['cols'])
                bombs = int(temp_dict['bombs'])
                score = int(temp_dict['score'])
                movs = int(temp_dict['movs'])
                username = temp_dict['username']
                total = compute_total(rows, cols, bombs, score, movs)
                tupla = (total, username, rows, cols, bombs, score, movs)

                # Adiciona novo score à lista, ordena novamente e pega os cinco melhores resultados
                last_dict['score'].append(tupla)
                last_dict['score'].sort(reverse=True)
                if len(last_dict['score']) > 5:
                    last_dict['score'] = last_dict['score'][:5]
            except:
                self.send_response(406)
                self.end_headers()
                self.wfile.write('Invalid parameters')
                return

        self.send_response(200)
        self.end_headers()

        # Retorna 'Done!' para requests que funcionaram corretamente ou o identificador do usuário
        if OPERATION != 4:
            self.wfile.write('Done!')
        else:
            self.wfile.write(str(response))
        return

    def do_DELETE(self):
        """
            Método que responde a requisições DELETE
        :return:
        """
        # Atualiza último acesso
        global last_timestamp
        last_timestamp = time.time()

        path = clean_path(self.path)

        if not self.check_path(path):
            return

        path = path[1:]

        if path[0] in {'jogadas'}:
            LOOP = 0
        elif path[0] in {'tabuleiros','jogadores','score','partidas'} :
            LOOP = 1
        else:
            LOOP = len(path)

        # Percorre até o LOOP-ésimo último dicionário
        ultimo_dict = server_data['jogos']
        while len(path) > LOOP:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]

        # Remove do servidor apenas a primeira sub-chave do dicionário
        if LOOP == 0:
            try:
                chave_mais_antiga = sorted(ultimo_dict.keys())[0]
                del ultimo_dict[chave_mais_antiga]
            except:
                pass # Dict está vazio
        # Remove do servidor o último dicionário por completo
        elif LOOP == 1:
            try:
                del ultimo_dict[path[0]]
            except:
                pass

        self.send_response(200)
        self.end_headers()
        self.wfile.write('Done!')
        return

def garbage_collector():
    """
        Thread que limpa as informações do servidor uma vez por mês
    :return: nada
    """
    # Atualiza primeiro acesso
    global last_timestamp
    last_timestamp = time.time()

    while True:
        # Horário do último acesso
        d = datetime.datetime.fromtimestamp(last_timestamp)
        # Horário do último acesso + 1 mês
        d = datetime.datetime(d.year, min(11, d.month + 1), d.day, d.hour, d.minute, d.second, d.microsecond)

        # Se passou tempo esperado desde o último acesso
        if d < datetime.datetime.now():
            # Remove apenas dicionário jogos, preservando score global
            if 'jogos' in server_data:
                server_data['jogos'].clear()
            print "Server has been cleaned at %s" % str(datetime.datetime.now())
            last_timestamp = time.time()

        # Dorme um dia
        time.sleep(24*60*60)


if __name__ == '__main__':
    """
        Inicia a thread para limpar dados e inicia servidor
    """
    clean_server_data = Thread(target=garbage_collector)
    clean_server_data.start()
    server_address = ('', SERVER_PORT)
    server = HTTPServer(server_address, MineSweeperServer)
    sa = server.socket.getsockname()
    print "Serving on", sa[0], "port", sa[1], "..."
    server.serve_forever()
