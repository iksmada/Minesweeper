import time

from classes import *
from constants import *

def open_title():
    pygame.init()
    screen = pygame.display.set_mode([15 * BLOCK_SIZE, 12 * BLOCK_SIZE])
    screen.fill(GRAYLIGHT)
    menu_itens = pygame.sprite.Group()
    menu_itens.add(Button('SINGLE', 'SINGLE PLAYER', screen.get_width() / 4, 50, screen.get_width() / 2, 40))
    menu_itens.add(Button('MULTI', 'MULTIPLAYER', screen.get_width() / 4, 100, screen.get_width() / 2, 40))
    button_width = 70
    menu_itens.add(Button('ROWS', 'LINHAS', screen.get_width()*2/10 - button_width/2, 170, button_width, 30, SMALL_FONT_SIZE))
    menu_itens.add(Button('COLS', 'COLUNAS', screen.get_width()*5/10 - button_width/2, 170, button_width, 30, SMALL_FONT_SIZE))
    menu_itens.add(Button('BOMBS', 'BOMBAS', screen.get_width()*8/10 - button_width/2, 170, button_width, 30, SMALL_FONT_SIZE))

    menu_itens.draw(screen) # Desenha os retangulos
    menu_itens.update(screen) # Escreve o texto

    pygame.display.flip()
    time.sleep(3)
    pygame.quit()