# -*- coding: utf-8

MINA_SIZE   = 20 # tamanho de uma mina
BLOCK_SIZE  = 24 # tamanho de um bloco que contem uma mina

# Espaço entre tabuleiro e minas
PADDING = (BLOCK_SIZE - MINA_SIZE)
# Espaço para informações da partida
TITLE_AND_SCORE_SIZE = 4 * BLOCK_SIZE

# Tamanho de fonte padrão
TINY_FONT_SIZE =            int(BLOCK_SIZE*0.25)
EXTRA_SMALL_FONT_SIZE =     int(BLOCK_SIZE*0.5)
SMALL_FONT_SIZE =           int(BLOCK_SIZE*0.75)
NORMAL_FONT_SIZE =          int(BLOCK_SIZE)
LARGE_FONT_SIZE =           int(BLOCK_SIZE*1.25)
EXTRA_LARGE_FONT_SIZE =     int(BLOCK_SIZE*1.5)
HUGE_FONT_SIZE =            int(BLOCK_SIZE*2)

# Definição das cores utilizadas
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)

YELLOW   = ( 255, 255,   0)
PINK     = ( 255,   0, 255)
CYAN     = (   0, 255, 255)

GRAYDARK = ( 150, 150, 150)
GRAYLIGHT= ( 215, 215, 215)

# Definição de cores em alto-nível
COLOR_CLEAR_SCREEN = GRAYDARK
COLOR_CLEAR_SCREEN_SCORE = BLACK
COLOR_UNCLICKED_BLOCK = GRAYLIGHT
COLOR_CLICKED_BLOCK = GRAYDARK
COLOR_TITLE = RED
COLOR_RESULT= YELLOW
COLOR_MENU_POINTS = BLACK
COLOR_MY_SCORE = BLUE
COLOR_THIS_SCORE = GREEN
COLOR_OTHER_SCORE = GRAYLIGHT

# Definição de ações
ACTION_FILL_CLICKED = 1

ACTION_REGISTER_CLICK = 1
ACTION_REGISTER_MARK = 2

# Variáveis para partidas multiplayer
# Troque as próximas linhas para partidas localhost
#SERVER_NAME = 'http://127.0.0.1'
SERVER_NAME = 'http://ec2-52-67-17-125.sa-east-1.compute.amazonaws.com'
SERVER_PORT = 8000

SERVER_ADRESS =  SERVER_NAME + ':' + str(SERVER_PORT) + '/'

ROUTE_JOGOS = SERVER_ADRESS + 'jogos/'
ROUTE_SCORE = SERVER_ADRESS + 'score/'

ROUTE_JOGADAS = ROUTE_JOGOS + 'jogadas/'
ROUTE_PARTIDAS = ROUTE_JOGOS + 'partidas/'
ROUTE_TABULEIROS = ROUTE_JOGOS + 'tabuleiros/'
ROUTE_JOGADORES = ROUTE_JOGOS + 'jogadores/'
