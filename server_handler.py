from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from constants import SERVER_PORT
import datetime
import random
from threading import Thread
import time

server_data = {}
last_timestamp = 0

def clean_path(path):
    path = path.strip().split('/')
    # Remove string vazias
    path = [x for x in path if x]
    return path

accepted_services = ['jogos']
accepted_route = {'jogos':['partidas', 'tabuleiros', 'segredo']}

class MineSweeperServer(BaseHTTPRequestHandler):

    # Remova esse metodo para ver todas as requests chegando
    def log_message(self, f, *args):
        pass

    def do_GET(self):
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

        if path[0] == 'partidas':
            OPERATION = 1
        elif path[0] == 'tabuleiros':
            OPERATION = 2
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

        if OPERATION == 1:
            try:
                chave_mais_antiga = sorted(ultimo_dict.keys())[0]
                ultimo_dict = ultimo_dict[chave_mais_antiga]
            except:
                pass # Dict esta vazio

        response = ''
        for key, val in ultimo_dict.items():
            response += '&' + str(key) + '=' + str(val)
        response = response[1:]
        # print response

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)
        return

    def do_POST(self):
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

        if path[0] == 'partidas':
            OPERATION = 1
        elif path[0] == 'tabuleiros':
            OPERATION = 2
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

        # print server_data

        self.send_response(200)
        self.end_headers()
        self.wfile.write('Done!')
        return

    def do_DELETE(self):
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

        if path[0] == 'partidas':
            LOOP = 0
        elif path[0] == 'tabuleiros':
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
    global last_timestamp
    last_timestamp = time.time()

    # Server_data is cleaned after one hour that it has not been used.
    while True:
        d = datetime.datetime.fromtimestamp(last_timestamp)
        d = datetime.datetime(d.year, d.month, d.day, d.hour + 1, d.minute, d.second, d.microsecond)

        if d < datetime.datetime.now():
            server_data.clear()
            print "Server has been cleaned at %s" % str(datetime.datetime.now())

        time.sleep(60*5)


if __name__ == '__main__':
    clean_server_data = Thread(target=garbage_collector)
    clean_server_data.start()
    server_address = ('', SERVER_PORT)
    server = HTTPServer(server_address, MineSweeperServer)
    sa = server.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    server.serve_forever()