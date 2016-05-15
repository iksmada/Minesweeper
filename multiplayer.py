from server_handler import *

SERVER_PORT = 8000

def thread_init_server():
    server_address = ('', SERVER_PORT)
    server = BaseHTTPServer.HTTPServer(server_address, MineSweeperServer)
    sa = server.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    server.serve_forever()