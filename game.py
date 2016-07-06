from utils import *

import pygame
import random
from threading import Thread

def play_game():
    if GameController.is_multiplayer:

        GameController.player_ID = get_player_ID()

        shared_click_list = []
        thread_get = Thread(target=thread_get_data,
                            args=(GameController.player_ID, GameController.match, shared_click_list))
        thread_get.start()

    # Initialize Pygame
    pygame.init()
    GameController.done = False
    while not GameController.done:

        if GameController.is_multiplayer:
            if GameController.player_ID == 0:
                result = create_new_tabuleiro_on_server()
                delete_match_score()
            else:
                result = get_tabuleiro_from_server()

            tabuleiro, GameController.rows, GameController.columns = result

        GameController.screen_width = GameController.columns * BLOCK_SIZE + PADDING + 2 * BLOCK_SIZE
        GameController.screen_height = GameController.rows * BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE + 2 * BLOCK_SIZE
        screen = pygame.display.set_mode([GameController.screen_width, GameController.screen_height])

        # Criando matriz ROWS+1 por COLUMNS+1
        # Neste caso, nao sera gerado IndexError quando elemento esta fora da matriz
        matrix = [[None for x in range(GameController.rows + 1)] for y in range(GameController.columns + 1)]
        # grupo dos elementos para minas e todos os outros elementos
        mines = pygame.sprite.Group()
        all_sprites_list = pygame.sprite.Group()
        # Fila de elementos que precisam ser atualizados a cada clique
        blocks_to_reveal = []

        # Inicializa variaveis estaticas (e compartilhadas)
        Block.screen = screen
        Block.all_sprites_list = all_sprites_list
        Block.matrix = matrix
        Block.blocks_to_reveal = blocks_to_reveal

        GameController.score = 0
        GameController.movs = 0
        GameController.markedBombs = 0
        GameController.revealedBlocks = 0
        # Inicializa valores default
        GameController.bombs = GameController.columns * GameController.rows * GameController.bombs_percentage / 100
        GameController.totalBlocks = GameController.rows * GameController.columns

        if not GameController.is_multiplayer:
            i = 0
            while i < GameController.bombs:
                posX=random.randrange(GameController.columns)
                posY=random.randrange(GameController.rows)
                if matrix[posX][posY] is None:
                    mine = Mine(posX,posY)
                    matrix[posX][posY]=mine
                    # Add the block to the list of objects
                    mines.add(mine)
                    all_sprites_list.add(mine)
                    i += 1
        else:
            for posX in range(GameController.columns):
                for posY in range(GameController.rows):
                    if tabuleiro[posY*GameController.columns + posX] == '1':
                        mine = Mine(posX, posY)
                        matrix[posX][posY] = mine
                        mines.add(mine)
                        all_sprites_list.add(mine)

        for posX in range(GameController.columns):
            for posY in range(GameController.rows):
                if matrix[posX][posY] is None:
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

        #Loop until the user clicks the close button.
        GameController.round_is_finished = False
        win=False
        new_game = True

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Clean former clicked points
        if GameController.is_multiplayer:
            while len(shared_click_list) > 0:
                shared_click_list.pop()

        # -------- Main Program Loop -----------
        while not GameController.round_is_finished:
            if GameController.is_multiplayer and len(shared_click_list) > 0:
                click = shared_click_list.pop(0)
                posX = int(click[0])
                posY = int(click[1])
                color = str(click[2])
                action = int(click[3])
                bloco = matrix[posX][posY]
                if type(bloco) is Block and not bloco.revealed:
                    if action == ACTION_REGISTER_CLICK:
                        bloco.reveal()
                        while len(blocks_to_reveal) > 0:
                            bloco = blocks_to_reveal.pop(0)
                            bloco.reveal()
                    elif action == ACTION_REGISTER_MARK:
                        bloco.mark(color)
                elif type(bloco) is Mine and not bloco.revealed:
                    if action == ACTION_REGISTER_CLICK:
                        pass
                        #TODO O que fazer quando seu parceiro clica na mina?
                    elif action == ACTION_REGISTER_MARK:
                        bloco.mark(color)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    button1, button2, button3 = pygame.mouse.get_pressed()
                    x, y = event.pos
                    for bloco in all_sprites_list:
                        # usa colisao:
                        # vantagem -> ignora se clicar entre dois quadrados
                        if bloco.rect.collidepoint(x, y):
                            if button1:
                                if not bloco.revealed:
                                    if GameController.is_multiplayer:
                                        thread_send = Thread(target=thread_send_data, args=(
                                            bloco.posX, bloco.posY, GameController.player_ID, GameController.match, GameController.player_color, ACTION_REGISTER_CLICK))
                                        thread_send.start()
                                    # Nao adiciona movimentos quando todas as bombas foram encontradas
                                    if not (GameController.markedBombs == GameController.bombs or isinstance(bloco,Mine)):
                                        GameController.movs += 1
                                    bloco.reveal()
                                    GameController.score += bloco.neighbors
                                    while len(blocks_to_reveal) > 0:
                                        bloco = blocks_to_reveal.pop(0)
                                        bloco.reveal()
                                        GameController.score += bloco.neighbors
                                    # revelou uma mina
                                    if isinstance(bloco,Mine): #and not bloco.marked:
                                        # PERDEU
                                        GameController.round_is_finished = True
                            elif button3:
                                if not bloco.marked and not  bloco.revealed:
                                    if GameController.is_multiplayer:
                                        thread_send = Thread(target=thread_send_data, args=(bloco.posX, bloco.posY,
                                                                                            GameController.player_ID,
                                                                                            GameController.match,
                                                                                            GameController.player_color,
                                                                                            ACTION_REGISTER_MARK))
                                        thread_send.start()
                                    bloco.mark(GameController.player_color)
                                    #se for mina
                                    if isinstance(bloco,Mine):
                                        #marcou uma mina
                                        GameController.markedBombs += 1
                                        GameController.score += 100
                                    else:
                                        GameController.score -= 20
                        #GANHOU
                        if GameController.markedBombs + GameController.revealedBlocks == GameController.totalBlocks:
                            GameController.round_is_finished = True
                            win = True

                if event.type == pygame.QUIT:  # If user clicked close
                    GameController.round_is_finished = True  # Flag that we are round so we exit this loop
                    GameController.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        GameController.round_is_finished = True
                        GameController.done = True

            # Clear the screen
            screen.fill(COLOR_CLEAR_SCREEN)

            all_sprites_list.draw(screen)
            show_match_info(screen)
            # Limit to 20 frames per second
            clock.tick(20)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            if GameController.is_multiplayer and new_game:
                if GameController.username == GameController.match:
                    wait_for_space_key_message(screen)
                else:
                    if not check_match_has_begun():
                        wait_for_match_message(screen)
                        while not get_match_status() > 0:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        GameController.round_is_finished = True
                                        GameController.done = True
                                elif event.type == pygame.QUIT:
                                    GameController.round_is_finished = True
                                    GameController.done = True
                    else:
                        match_has_started_message(screen)
                        GameController.round_is_finished = True
                        GameController.done = True
                new_game = False

        #terminou rodada, mas nao pediu pra sair do jogo
        if not GameController.done:
            #mostrar se ganhou ou perdeu
            screen.fill(COLOR_CLEAR_SCREEN)
            all_sprites_list.draw(screen)
            #perdeu
            if not win:
                show_match_info(screen, "LOST", COLOR_RESULT)
                #revela minas
                for mine in mines:
                    mine.reveal_unrevealed()
            # ganhou
            else:
                show_match_info(screen, "WIN", COLOR_RESULT)

            pygame.time.wait(1000)
            if not GameController.is_multiplayer:
                screen.fill(COLOR_CLEAR_SCREEN_SCORE)
                show_match_info(screen, "SCORE", COLOR_RESULT)
                register_global_score()
                show_global_score(screen)
                pygame.display.flip()
                pygame.time.wait(1000)
            else:
                register_match_score()

            # espera clicar pra continuar nova rodada ou sair do jogo
            clicked = False
            while not clicked and not GameController.done:

                if GameController.is_multiplayer:
                    screen.fill(COLOR_CLEAR_SCREEN_SCORE)
                    show_match_info(screen, "SCORE", COLOR_RESULT)
                    show_match_score(screen)
                    pygame.display.flip()

                pygame.time.wait(100)

                for event in pygame.event.get():  # User did something
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True
                    if event.type == pygame.QUIT:  # If user clicked close
                        GameController.done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            GameController.done = True
                        elif event.key == pygame.K_KP_ENTER:
                            clicked = True
                        elif event.key == pygame.K_SPACE:
                            clicked = True

    if GameController.is_multiplayer:
        shared_click_list.insert(0,True)
    pygame.quit()
