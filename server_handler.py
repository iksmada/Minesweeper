import BaseHTTPServer
import urlparse
import json

server_data = {}

class MineSweeperServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        print self.requestline
        path = self.path.strip().split('/')[1:]

        ultimo_dict = server_data
        while len(path) > 0:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]

        response = ''
        for key, val in ultimo_dict.items():
            response += '&' + key + '=' + val
        response = response[1:]
        print response

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)

    def do_POST(self):
        print self.requestline
        path = self.path.strip().split('/')[1:]

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

        for par in str(POST_data).split('&'):
            par = str(par).split('=')
            ultimo_dict[str(par[0])] = str(par[1])

        print server_data

        self.send_response(200)
        self.end_headers()
        self.wfile.write('OK')

    def do_DELETE(self):
        print self.requestline
        path = self.path.strip().split('/')[1:]

        ultimo_dict = server_data
        while len(path) > 1:
            if path[0] in ultimo_dict:
                ultimo_dict = ultimo_dict[path[0]]
            else:
                ultimo_dict[path[0]] = {}
                ultimo_dict = ultimo_dict[path[0]]

            path = path[1:]

        print server_data
        del ultimo_dict[path[0]]
        print server_data

        self.send_response(200)
        self.end_headers()
        self.wfile.write('')