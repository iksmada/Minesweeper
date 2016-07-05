from classes import *
from utils import *
from multiplayer import *
from server_handler import compute_total

import pygame
import random
from threading import Thread

def wait_for_space_key_message(screen):
    message = 'PRESS SPACE TO START MATCH'
    font = pygame.font.Font(None, min(EXTRA_LARGE_FONT_SIZE,get_recommended_font_size(screen,95,message)))
    wait = font.render(message, 1, BLACK)
    screen.blit(wait, ((GameController.screen_width - wait.get_size()[0]) / 2,
                (GameController.screen_height + TITLE_AND_SCORE_SIZE - wait.get_size()[1]) / 2))
    pygame.display.flip()

    set_up_new_match()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                elif event.key == pygame.K_ESCAPE:
                    GameController.round_is_finished = True
                    GameController.done = True
                    done = True
            elif event.type == pygame.QUIT:
                GameController.round_is_finished = True
                GameController.done = True
                done = True

    start_match()

def wait_for_match_message(screen):
    message = 'WAIT FOR MATCH TO START'
    font = pygame.font.Font(None, min(EXTRA_LARGE_FONT_SIZE,get_recommended_font_size(screen,95,message)))
    wait = font.render(message, 1, BLACK)
    screen.blit(wait, ((GameController.screen_width - wait.get_size()[0]) / 2,
                (GameController.screen_height + TITLE_AND_SCORE_SIZE - wait.get_size()[1]) / 2))
    pygame.display.flip()

def match_has_started_message(screen):
    message = 'SORRY, MATCH IS UNAVALAIBLE :('
    font = pygame.font.Font(None, min(EXTRA_LARGE_FONT_SIZE,get_recommended_font_size(screen,95,message)))
    wait = font.render(message, 1, BLACK)
    screen.blit(wait, ((GameController.screen_width - wait.get_size()[0]) / 2,
                       (GameController.screen_height + TITLE_AND_SCORE_SIZE - wait.get_size()[1]) / 2))
    pygame.display.flip()

    pygame.time.delay(3000)

def show_global_score(screen):
    scores = get_global_score()

    height = BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE
    step = BLOCK_SIZE*GameController.rows/float(7)
    font = pygame.font.Font('fonts/UbuntuMonoBold.ttf', SMALL_FONT_SIZE)

    if GameController.columns >= 20:
        message = '%-12s %5s %7s %7s %7s %5s %8s' % tuple('USERNAME ROWS COLUMNS BOMBS_% SCORE MOVS TOTAL'.split())
    elif GameController.columns >= 15:
        message = '%-12s %5s %5s %8s' % tuple('USERNAME SCORE MOVS TOTAL'.split())
    else:
        message = '%-12s %8s' % tuple('USERNAME TOTAL'.split())

    wait = font.render(message, 1, COLOR_TITLE)
    screen.blit(wait, ((GameController.screen_width - wait.get_width())/2 , height))
    pygame.display.flip()

    has_scored = False
    for score in scores:
        height += step
        # score = (total, username, rows, cols, bombs, score, movs)
        if GameController.columns >= 20:
            message = '%-12s %5d %7d %7s %7d %5d %8d' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
        elif GameController.columns >= 15:
            message = '%-12s %5d %5d %8d' % (score[1], score[5], score[6], score[0])
        else:
            message = '%-12s %8d' % (score[1], score[0])
        if score[1] == GameController.username  \
            and score[5] == GameController.score \
            and score[6] == GameController.movs:
            wait = font.render(message, 1, COLOR_THIS_SCORE)
            has_scored = True
        elif score[1] == GameController.username:
            wait = font.render(message, 1, COLOR_MY_SCORE)
        else:
            wait = font.render(message, 1, COLOR_OTHER_SCORE)
        screen.blit(wait, ((GameController.screen_width - wait.get_width())/2, height))
        pygame.time.wait(100)
        pygame.display.flip()

    total = compute_total(GameController.rows, GameController.columns, GameController.bombs_percentage,
                          GameController.score, GameController.movs)
    score = (total, GameController.username, GameController.rows,
             GameController.columns, GameController.bombs_percentage,
             GameController.score, GameController.movs)

    if not has_scored:
        if GameController.columns >= 20:
            message = '%-12s %5d %7d %7s %7d %5d %8d' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
        elif GameController.columns >= 15:
            message = '%-12s %5d %5d %8d' % (score[1], score[5], score[6], score[0])
        else:
            message = '%-12s %8d' % (score[1], score[0])
        wait = font.render(message, 1, COLOR_THIS_SCORE)
        screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + step))
        pygame.time.wait(100)
        pygame.display.flip()

    message = 'TOTAL = (100*SCORE*BOMBS_%)/(ROWS*COLUMNS) - MOVS%'
    font = pygame.font.Font('fonts/UbuntuMono.ttf', min(NORMAL_FONT_SIZE,get_recommended_font_size(screen,100,message)))
    wait = font.render(message, 1, COLOR_RESULT)
    screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + 2*step))
    pygame.time.wait(100)
    pygame.display.flip()

def show_match_score(screen):
    scores = get_match_score()
    all_players = get_match_players()
    finished_players = [score[1] for score in scores]

    all_players.sort()
    for player in all_players:
        if player not in finished_players:
            scores.append(('?????', player, 0, 0, 0, 0, 0))


    height = BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE
    step = BLOCK_SIZE*GameController.rows/float(7)
    font = pygame.font.Font('fonts/UbuntuMonoBold.ttf', SMALL_FONT_SIZE)

    if GameController.columns >= 20:
        message = '%-12s %5s %7s %7s %7s %5s %8s' % tuple('USERNAME ROWS COLUMNS BOMBS_% SCORE MOVS TOTAL'.split())
    elif GameController.columns >= 15:
        message = '%-12s %5s %5s %8s' % tuple('USERNAME SCORE MOVS TOTAL'.split())
    else:
        message = '%-12s %8s' % tuple('USERNAME TOTAL'.split())

    wait = font.render(message, 1, COLOR_TITLE)
    screen.blit(wait, ((GameController.screen_width - wait.get_width())/2 , height))

    has_scored = False
    for score in scores:
        height += step
        # score = (total, username, rows, cols, bombs, score, movs)
        if GameController.columns >= 20:
            message = '%-12s %5d %7d %7s %7d %5d %8s' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
        elif GameController.columns >= 15:
            message = '%-12s %5d %5d %8s' % (score[1], score[5], score[6], score[0])
        else:
            message = '%-12s %8s' % (score[1], score[0])
        if score[1] == GameController.username  \
            and score[5] == GameController.score \
            and score[6] == GameController.movs:
            wait = font.render(message, 1, COLOR_THIS_SCORE)
            has_scored = True
        elif score[1] == GameController.username:
            wait = font.render(message, 1, COLOR_MY_SCORE)
        else:
            wait = font.render(message, 1, COLOR_OTHER_SCORE)
        screen.blit(wait, ((GameController.screen_width - wait.get_width())/2, height))

        total = compute_total(GameController.rows, GameController.columns, GameController.bombs_percentage,
                              GameController.score, GameController.movs)

        score = (total, GameController.username, GameController.rows, GameController.columns, GameController.bombs_percentage,
                 GameController.score, GameController.movs)

    if not has_scored:
        if GameController.columns >= 20:
            message = '%-12s %5d %7d %7s %7d %5d %8d' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
        elif GameController.columns >= 15:
            message = '%-12s %5d %5d %8d' % (score[1], score[5], score[6], score[0])
        else:
            message = '%-12s %8d' % (score[1], score[0])
        wait = font.render(message, 1, COLOR_THIS_SCORE)
        screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + step))
        pygame.time.wait(100)
        pygame.display.flip()

    message = 'TOTAL = (100*SCORE*BOMBS_%)/(ROWS*COLUMNS) - MOVS%'
    font = pygame.font.Font('fonts/UbuntuMono.ttf', min(NORMAL_FONT_SIZE,get_recommended_font_size(screen,100,message)))
    wait = font.render(message, 1, COLOR_RESULT)
    screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + 2*step))

def play_game():
    if GameController.is_multiplayer:
        shared_click_list = []
        GameController.player_ID = get_player_ID()
        thread_get = Thread(target=thread_get_data, args=(GameController.player_ID, GameController.match_ID, shared_click_list))
        thread_get.start()

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode([GameController.screen_width, GameController.screen_height])
    GameController.done = False
    while not GameController.done:
        #grupo dos elementos para minas e todos os outros elementos
        mines = pygame.sprite.Group()
        all_sprites_list = pygame.sprite.Group()
        # Criando matriz ROWS+1 por COLUMNS+1
        # Neste caso, nao sera gerado IndexError quando elemento esta fora da matriz
        matrix = [[None for x in range(GameController.rows + 1)] for y in range(GameController.columns + 1)]
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

        if GameController.player_ID == 0:
            create_new_tabuleiro_on_server()
            delete_match_score()

        tabuleiro = get_tabuleiro_from_server().replace('\n', '')

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
                                        bloco.posX, bloco.posY, GameController.player_ID, GameController.match_ID, GameController.player_color, ACTION_REGISTER_CLICK))
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
                                                                                            GameController.match_ID,
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
            GameController.draw(screen)
            # Limit to 20 frames per second
            clock.tick(20)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            if GameController.is_multiplayer and new_game:
                if GameController.username == GameController.match_ID:
                    wait_for_space_key_message(screen)
                else:
                    if not check_match_has_begun():
                        wait_for_match_message(screen)
                        while not wait_match_to_begin() > 0:
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
                GameController.draw(screen, "LOST", COLOR_RESULT)
                #revela minas
                for mine in mines:
                    mine.reveal_unrevealed()
            # ganhou
            else:
                GameController.draw(screen, "WIN", COLOR_RESULT)

            pygame.time.wait(1000)
            if not GameController.is_multiplayer:
                screen.fill(COLOR_CLEAR_SCREEN_SCORE)
                GameController.draw(screen, "SCORE", COLOR_RESULT)
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
                    GameController.draw(screen, "SCORE", COLOR_RESULT)
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
