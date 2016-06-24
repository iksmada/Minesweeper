# -*- coding: utf-8

import datetime
import random
import time

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from constants import SERVER_PORT

server_data = {}
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

# Rotas acessíveis
accepted_services = ['jogos']
# Sub-rotas acessíveis
accepted_route = {'jogos':['jogadas','partidas', 'tabuleiros', 'jogadores','segredo']}

class MineSweeperServer(BaseHTTPRequestHandler):
    """
        Servidor REST (HTTP) para partidas multiplayer
    """

    # Remova esse metodo para ver todas as requests chegando
    def log_message(self, f, *args):
        pass

    def do_GET(self):
        """
            Método que responde a requisições GET
        :return:
        """
        # Atualiza último acesso
        global last_timestamp
        last_timestamp = time.time()

        path = clean_path(self.path)

        if len(path) < 3:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Running :)')
            return

        if path[0] not in accepted_services:
            self.send_response(403)
            self.end_headers()
            self.wfile.write('Unknown service')
            return

        if path[1] not in accepted_route[path[0]]:
            self.send_response(403)
            self.end_headers()
            self.wfile.write('Unknown access route')
            return

        path = path[1:]

        if path[0] == 'jogadas':
            OPERATION = 1
        elif path[0] == 'tabuleiros':
            OPERATION = 2
        elif path[0] == 'partidas':
            OPERATION = 3
        elif path[0] == 'segredo':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(server_data))
            return
        else:
            OPERATION = 0

        ultimo_dict = server_data
        while len(path) > 0:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]

        response = ''
        if OPERATION == 1:
            try:
                chave_mais_antiga = sorted(ultimo_dict.keys())[0]
                ultimo_dict = ultimo_dict[chave_mais_antiga]
            except:
                pass # Dict esta vazio
        if OPERATION in {1, 2, 3}:
            for key, val in ultimo_dict.items():
                response += '&' + str(key) + '=' + str(val)
            response = response[1:]

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

        if len(path) < 3:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(':(')
            return

        if path[0] not in accepted_services:
            self.send_response(403)
            self.end_headers()
            self.wfile.write('Unknown service')
            return

        if path[1] not in accepted_route[path[0]]:
            self.send_response(403)
            self.end_headers()
            self.wfile.write('Unknown access route')
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
        else:
            OPERATION = 0

        ultimo_dict = server_data
        while len(path) > 0:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]

        content_length = int(self.headers.getheader('content-length', 0))
        POST_data = self.rfile.read(content_length)

        if OPERATION == 1:
            instante = datetime.datetime.now()
            chave_instante = str(instante).replace('.', ':')
            ultimo_dict[chave_instante] = {}
            ultimo_dict = ultimo_dict[chave_instante]

            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                ultimo_dict[str(par[0])] = str(par[1])
        elif OPERATION == 2:
            temp_dict = {}
            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                temp_dict[str(par[0])] = str(par[1])
            try:
                rows = int(temp_dict['rows'])
                cols = int(temp_dict['cols'])
                bombs = int(temp_dict['bombs'])
            except:
                self.send_response(406)
                self.end_headers()
                self.wfile.write('Invalid parameters')
                return
            tabuleiro = ('0'*cols + '\n')*rows
            i = 0
            while i < bombs:
                r = random.randrange(rows)
                c = random.randrange(cols)
                if tabuleiro[r*cols + c] == '0':
                    tabuleiro = tabuleiro[:r*cols + c] + '1' + tabuleiro[r*cols + c + 1:]
                    i += 1
            if 'tabuleiro' not in ultimo_dict \
                    or ultimo_dict['soma'] != rows + cols + bombs\
                    or ultimo_dict['mult'] != rows * cols * bombs:
                ultimo_dict['tabuleiro']=tabuleiro
                # Usado para comparar a assinatura do tabuleiro atual com o antigo
                ultimo_dict['soma'] = rows + cols + bombs
                ultimo_dict['mult'] = rows * cols * bombs
        elif OPERATION == 3:
            ultimo_dict['conectando'] = True
        elif OPERATION == 4:
            for par in str(POST_data).split('&'):
                par = str(par).split('=')
                if par[0] == 'player':
                    if len(ultimo_dict) == 0:
                        ultimo_dict[par[1]] = 0
                    elif par[1] not in ultimo_dict.keys():
                        ultimo_dict[par[1]] = max(ultimo_dict.values()) + 1

                    response = ultimo_dict[par[1]]

        # print server_data

        self.send_response(200)
        self.end_headers()
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

        if len(path) < 3:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(':(')
            return

        if path[0] not in accepted_services:
            self.send_response(403)
            self.end_headers()
            self.wfile.write('Unknown service')
            return

        if path[1] not in accepted_route[path[0]]:
            self.send_response(403)
            self.end_headers()
            self.wfile.write('Unknown access route')
            return

        path = path[1:]

        if path[0] == 'jogadas' or 'partidas':
            LOOP = 0
        elif path[0] == 'tabuleiros' :
            LOOP = 1
        else:
            LOOP = len(path)

        ultimo_dict = server_data
        while len(path) > LOOP:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]
        if LOOP == 0:
            try:
                chave_mais_antiga = sorted(ultimo_dict.keys())[0]
                del ultimo_dict[chave_mais_antiga]
            except:
                pass # Dict esta vazio
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
        Thread que limpa as informações do servidor a cada 15 minutos
    :return: nada
    """
    # Atualiza primeiro acesso
    global last_timestamp
    last_timestamp = time.time()

    while True:
        # Horário do último acesso
        d = datetime.datetime.fromtimestamp(last_timestamp)
        # Horário do último acesso + 15 minutos
        d = datetime.datetime(d.year, d.month, d.day, d.hour, min(d.minute + 15,59), d.second, d.microsecond)

        # Se passou 15 minutos
        if d < datetime.datetime.now():
            server_data.clear()
            print "Server has been cleaned at %s" % str(datetime.datetime.now())
            last_timestamp = time.time()

        #  Dorme um minuto
        time.sleep(60)


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
