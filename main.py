from multiplayer import *
from classes import *
from constants import *

import pygame
import random
from threading import Thread

#TODO Placa e wait avisando se ganho uo perdeu e quantos pontos
#TODO pintar de vermelho bomba que clicou e fez perde

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Inicializa variaveis estaticas
Block.screen = screen
Title_and_Score.screen = screen

title_score = Title_and_Score()
done = False
# Variavel para controlar alguns componentes multiplayer
IS_MULTIPLAYER = False

if IS_MULTIPLAYER:
    shared_click_list = []
    PLAYER_ID = raw_input('ID:')
    PARTIDA_KEY = raw_input('PARTIDA:')
    thread_get = Thread(target=thread_get_data, args=(PLAYER_ID, PARTIDA_KEY, shared_click_list))
    thread_get.start()

while not done:
    #grupo dos elementos de minas e total
    mines = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    #cria bombas
    # Criando matriz ROWS+1 por COLUMNS+1
    # Neste caso, nao sera gerado IndexError quando elemento esta fora da matriz
    matrix = [[0 for x in range(ROWS + 1)] for y in range(COLUMNS + 1)]
    # Fila de elementos que precisam ser atualizados a cada clique
    blocks_to_reveal = []

    # Inicializa variaveis estaticas
    Block.all_sprites_list = all_sprites_list
    Block.matrix = matrix
    Block.blocks_to_reveal = blocks_to_reveal

    for i in range(BOMBS):
        posX=random.randrange(COLUMNS)
        posY=random.randrange(ROWS)
       # print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
        if matrix[posX][posY]==0:
            mine = Mine(posX,posY)
            matrix[posX][posY]=mine
        # Add the block to the list of objects
            mines.add(mine)
            all_sprites_list.add(mine)
           # print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

    for posX in range(COLUMNS):
        for posY in range(ROWS):
            #print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
            if matrix[posX][posY] == 0:
                neighbors = 0
                if type(matrix[posX + 1][posY    ]) is Mine:
                    neighbors += 1
                if type(matrix[posX    ][posY + 1]) is Mine:
                    neighbors += 1
                if type(matrix[posX - 1][posY    ]) is Mine:
                    neighbors += 1
                if type(matrix[posX    ][posY - 1]) is Mine:
                    neighbors += 1
                if type(matrix[posX + 1][posY + 1]) is Mine:
                    neighbors += 1
                if type(matrix[posX - 1][posY + 1]) is Mine:
                    neighbors += 1
                if type(matrix[posX + 1][posY - 1]) is Mine:
                    neighbors += 1
                if type(matrix[posX - 1][posY - 1]) is Mine:
                    neighbors += 1

                bloco = Block(posX, posY, neighbors)
                matrix[posX][posY] = bloco
                all_sprites_list.add(bloco)
                #print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

    #Loop until the user clicks the close button.
    round_is_finished = False
    win=False
    title_score.movs=0

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not round_is_finished:
        if IS_MULTIPLAYER and len(shared_click_list) > 0:
            click = shared_click_list.pop(0)
            print click
            posX = int(click[0])
            posY = int(click[1])
            action = int(click[2])
            bloco = matrix[posX][posY]
            if type(bloco) is Block and not bloco.revealed:
                if action == ACTION_REGISTER_CLICK:
                    bloco.reveal()
                    while len(blocks_to_reveal) > 0:
                        bloco = blocks_to_reveal.pop(0)
                        bloco.reveal()
                elif ACTION_REGISTER_MARK:
                    bloco.mark()

        for event in pygame.event.get(): # User did something

            if event.type == pygame.MOUSEBUTTONDOWN:
                button1, button2, button3 = pygame.mouse.get_pressed()
                x, y = event.pos
                bombsMarked=0
                blocksRevealed=0
                for bloco in all_sprites_list:
                    if bloco.rect.collidepoint(x, y):
                        if button1:
                            if IS_MULTIPLAYER:
                                thread_send = Thread(target=thread_send_data,
                                                         args=(bloco.posX, bloco.posY, PLAYER_ID, PARTIDA_KEY,
                                                               ACTION_REGISTER_CLICK))
                                thread_send.start()
                            if not bloco.revealed: title_score.movs+=1
                            bloco.reveal()
                            while len(blocks_to_reveal) > 0:
                                bloco = blocks_to_reveal.pop(0)
                                bloco.reveal()
                    # usa colisao:
                    # vantagem -> ignora se clicar entre dois quadrados

                        elif button3:
                            if IS_MULTIPLAYER:
                                thread_send = Thread(target=thread_send_data,
                                                         args=(bloco.posX, bloco.posY, PLAYER_ID, PARTIDA_KEY,
                                                               ACTION_REGISTER_MARK))
                                thread_send.start()
                            bloco.mark()
                        #se for mina
                    if type(bloco)==Mine:
                            #revelou uma mina
                        if bloco.revealed:
                            #PERDEU
                            round_is_finished=True
                            #marcou uma mina
                        if bloco.marked:
                            bombsMarked+=1
                    #se for bloco normal e se revelou o bloco
                    elif bloco.revealed:
                            blocksRevealed+=1
                        #se marcou todas as bombas e revelou todos os blocos
                    #print "bombas marcadas:"+str(bombsMarked)+" e blocos revelados:"+ str(blocksRevealed)
                if bombsMarked==BOMBS and blocksRevealed==(COLUMNS*ROWS-BOMBS):
                            #GANHOU
                    round_is_finished=True
                    win=True

            if event.type == pygame.QUIT:  # If user clicked close
                round_is_finished = True  # Flag that we are round so we exit this loop
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    round_is_finished = True
                    done = True

        # Clear the screen
        screen.fill(COLOR_CLEAR_SCREEN)

        #for block in all_sprites_list: block.reveal()
        all_sprites_list.draw(screen)
        title_score.draw()
        # Limit to 20 frames per second
        clock.tick(20)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    #terminou rodada,mas nao pediu pra sair do jogo
    if not done:
        #mostrar se ganhou ou perdeu
        screen.fill(COLOR_CLEAR_SCREEN)
        all_sprites_list.draw(screen)
        #perder
        if not win:
            title_score.draw("LOST", COLOR_RESULT)
            #revela minas
            for mine in mines:
                mine.reveal()
        # ganhou
        else:
            title_score.draw("WIN", COLOR_RESULT)
        pygame.display.flip()

        # espera clicar pra continuar nova rodada ou sair do jogo
        clicked=False
        while not clicked and not done:
            pygame.time.wait(500)
            for event in pygame.event.get():  # User did something
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked=True
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

if IS_MULTIPLAYER:
    shared_click_list.insert(0,True)
pygame.quit()
