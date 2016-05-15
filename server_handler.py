from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from constants import SERVER_PORT
import datetime
server_data = {}

def clean_path(path):
    path = path.strip().split('/')
    # Remove string vazias
    path = [x for x in path if x]
    return path

class MineSweeperServer(BaseHTTPRequestHandler):

    # Remova esse metodo para ver todas as requests chegando
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        # print self.requestline
        path = clean_path(self.path)

        ultimo_dict = server_data
        while len(path) > 0:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]

        try:
            chave_mais_antiga = sorted(ultimo_dict.keys())[0]
            ultimo_dict = ultimo_dict[chave_mais_antiga]
        except:
            pass # Dict esta vazio

        response = ''
        for key, val in ultimo_dict.items():
            response += '&' + key + '=' + val
        response = response[1:]
        # print response

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)

    def do_POST(self):
        # print self.requestline
        path = clean_path(self.path)

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

        instante = datetime.datetime.now()
        chave_instante = str(instante).replace('.', ':')
        ultimo_dict[chave_instante] = {}
        ultimo_dict = ultimo_dict[chave_instante]

        for par in str(POST_data).split('&'):
            par = str(par).split('=')
            ultimo_dict[str(par[0])] = str(par[1])

        # print server_data

        self.send_response(200)
        self.end_headers()
        self.wfile.write('OK')

    def do_DELETE(self):
        # print self.requestline
        path = clean_path(self.path)

        ultimo_dict = server_data
        while len(path) > 0:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]

        try:
            chave_mais_antiga = sorted(ultimo_dict.keys())[0]

            del ultimo_dict[chave_mais_antiga]
        except:
            pass # Dict esta vazio

        self.send_response(200)
        self.end_headers()
        self.wfile.write('')

if __name__ == '__main__':
    server_address = ('', SERVER_PORT)
    server = HTTPServer(server_address, MineSweeperServer)
    sa = server.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    server.serve_forever()