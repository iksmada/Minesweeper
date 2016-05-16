# GAME SETTINGS
MINA_SIZE   = 20 # tamanho de uma mina
BLOCK_SIZE  = 22 # tamanho de um bloco que contem uma mina
ROWS        = 10
COLUMNS     = 2 * ROWS
BOMBS       = ROWS*COLUMNS/4 #25% do tabuleiro sao bombas
# espaco entre tabuleiro e minas
PADDING = (BLOCK_SIZE - MINA_SIZE)
TITLE_AND_SCORE_SIZE = BLOCK_SIZE
# tamanho da janela depende do numero de columas linhas e do tamanho de cada celula da matrix
SCREEN_WIDTH  = COLUMNS * BLOCK_SIZE + PADDING
SCREEN_HEIGHT = ROWS * BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE

# COLORS
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
YELLOW   = ( 255, 255,   0)
GRAYDARK = ( 167, 167, 167)
GRAYLIGHT= ( 205, 205, 205)

COLOR_CLEAR_SCREEN = GRAYDARK
COLOR_UNCLICKED_BLOCK = GRAYLIGHT
COLOR_CLICKED_BLOCK = GRAYDARK
COLOR_TITLE = RED
COLOR_RESULT= YELLOW
COLOR_SCORE = BLACK

# ACTIONS
ACTION_FILL_CLICKED = 1

ACTION_REGISTER_CLICK = 1
ACTION_REGISTER_MARK = 2

# MULTIPLAYER
#SERVER_NAME = 'http://127.0.0.1'
SERVER_NAME = 'http://ec2-52-67-17-125.sa-east-1.compute.amazonaws.com'
SERVER_PORT = 8000

SERVER_ADRESS =  SERVER_NAME + ':' + str(SERVER_PORT) + '/jogos/'
ROUTE_PARTIDAS = SERVER_ADRESS + 'partidas/'
ROUTE_TABULEIROS = SERVER_ADRESS + 'tabuleiros/'