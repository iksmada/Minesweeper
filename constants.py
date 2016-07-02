# -*- coding: utf-8
from pygame.font import Font

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

def get_recommended_font_size(screen_object,screen_percentage,text):
    width = int(screen_object.get_width()*screen_percentage/100)
    font = Font(None, HUGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return HUGE_FONT_SIZE

    font = Font(None, EXTRA_LARGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return EXTRA_LARGE_FONT_SIZE

    font = Font(None, LARGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return LARGE_FONT_SIZE

    font = Font(None, NORMAL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return NORMAL_FONT_SIZE

    font = Font(None, SMALL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return SMALL_FONT_SIZE

    font = Font(None, EXTRA_SMALL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return EXTRA_SMALL_FONT_SIZE

    font = Font(None, TINY_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return TINY_FONT_SIZE

    return TINY_FONT_SIZE


# Definição das cores utilizadas
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
YELLOW   = ( 255, 255,   0)
GRAYDARK = ( 127, 127, 127)
GRAYLIGHT= ( 215, 215, 215)

# Definição de cores em alto-nível
COLOR_CLEAR_SCREEN = GRAYDARK
COLOR_UNCLICKED_BLOCK = GRAYLIGHT
COLOR_CLICKED_BLOCK = GRAYDARK
COLOR_TITLE = RED
COLOR_RESULT= YELLOW
COLOR_SCORE = BLACK

# Definição de ações
ACTION_FILL_CLICKED = 1
ACTION_REGISTER_CLICK = 1
ACTION_REGISTER_MARK = 2

# Variáveis para partidas multiplayer
# Troque as próximas linhas para partidas localhost
#SERVER_NAME = 'http://127.0.0.1'
SERVER_NAME = 'http://ec2-52-67-17-125.sa-east-1.compute.amazonaws.com'
SERVER_PORT = 8000

SERVER_ADRESS =  SERVER_NAME + ':' + str(SERVER_PORT) + '/jogos/'
ROUTE_JOGADAS = SERVER_ADRESS + 'jogadas/'
ROUTE_PARTIDAS = SERVER_ADRESS + 'partidas/'
ROUTE_TABULEIROS = SERVER_ADRESS + 'tabuleiros/'
ROUTE_JOGADORES = SERVER_ADRESS + 'jogadores/'
