# -*- coding: utf-8

from classes import *
from multiplayer import *

import pygame
import random
from threading import Thread

def play_game():
    """
        Fluxo principal do jogo

        Existem dois loops principais:
            1 - controla que seja possível que uma partida seja iniciada logo após outra
            2 - controla os eventos do pygame da partida atual
    :return: nada
    """
    # Inicializa a thread que escuta novos cliques do servidor e pega o identificador de usuário
    if GameController.is_multiplayer:
        shared_click_list = []

        GameController.player_ID = get_player_ID()

        thread_get = Thread(target=thread_get_data,
                            args=(GameController.player_ID, GameController.match, shared_click_list))
        thread_get.start()

    # Inicializa pygame
    pygame.init()
    GameController.done = False # Variável de controle do loop principal
    while not GameController.done:
        # Inicializa cada partida multiplayer
        if GameController.is_multiplayer:
            # Se é o host da partida

            if GameController.player_ID == 0:
                result = create_new_tabuleiro_on_server()
                delete_match_score()
            else:
                result = get_tabuleiro_from_server()

            # Inicializa o tabuleiro e as dimensões do tabuleiro
            tabuleiro, GameController.rows, GameController.columns = result

        # Inicializa a tela a ser exibida
        GameController.screen_width = GameController.columns * BLOCK_SIZE + PADDING + 2 * BLOCK_SIZE
        GameController.screen_height = GameController.rows * BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE + 2 * BLOCK_SIZE
        screen = pygame.display.set_mode([GameController.screen_width, GameController.screen_height])

        # Criando matriz ROWS+1 por COLUMNS+1
        # Neste caso, não será gerado IndexError quando elemento está fora da matriz
        matrix = [[None for x in range(GameController.rows + 1)] for y in range(GameController.columns + 1)]
        # grupo dos elementos para minas e todos os outros elementos do jogo
        mines = pygame.sprite.Group()
        all_sprites_list = pygame.sprite.Group()
        # Fila de elementos que precisam ser atualizados a cada clique
        blocks_to_reveal = []

        # Inicializa variáveis estáticas de outras classes (e compartilhadas)
        Block.screen = screen
        Block.all_sprites_list = all_sprites_list
        Block.matrix = matrix
        Block.blocks_to_reveal = blocks_to_reveal

        # Inicializa valores default de variáveis
        GameController.score = 0
        GameController.movs = 0
        GameController.markedBombs = 0
        GameController.revealedBlocks = 0
        GameController.bombs = GameController.columns * GameController.rows * GameController.bombs_percentage / 100
        GameController.totalBlocks = GameController.rows * GameController.columns

        # Se partida não é multiplayer, gera um tabuleiro local
        # Se não, faz parse do tabuleiro recebi previamente
        if not GameController.is_multiplayer:
            i = 0
            while i < GameController.bombs:
                posX=random.randrange(GameController.columns)
                posY=random.randrange(GameController.rows)
                # Se posição estiver vazia
                if matrix[posX][posY] is None:
                    mine = Mine(posX,posY)
                    matrix[posX][posY]=mine
                    # Adiciona mina na fila de Minas
                    mines.add(mine)
                    all_sprites_list.add(mine)
                    i += 1
        else:
            for posX in range(GameController.columns):
                for posY in range(GameController.rows):
                    # Acessa matriz na forma de array
                    if tabuleiro[posY*GameController.columns + posX] == '1':
                        mine = Mine(posX, posY)
                        matrix[posX][posY] = mine
                        mines.add(mine)
                        all_sprites_list.add(mine)

        # Preenche os espaços em branco do tabuleiro com a informação dos vizinhos
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

        GameController.round_is_finished = False # Variável de controle do segundo loop principal
        win = False
        new_game = True

        # Pega elemento do clock para mudar framerate
        clock = pygame.time.Clock()

        # Atualiza importação da classe com valores atualizados de GameController
        import utils

        # Limpa cliques antigos não recebidos na última partida
        if GameController.is_multiplayer:
            while len(shared_click_list) > 0:
                shared_click_list.pop()

        while not GameController.round_is_finished:
            # Se recebeu um novo clique na lista compartilhada
            if GameController.is_multiplayer and len(shared_click_list) > 0:
                click = shared_click_list.pop(0)
                posX = int(click[0])
                posY = int(click[1])
                color = str(click[2])
                action = int(click[3])
                bloco = matrix[posX][posY]
                # Executa a ação do clique que chegou
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
                        pass #TODO O que fazer quando seu parceiro clica na mina?
                    elif action == ACTION_REGISTER_MARK:
                        bloco.mark(color)

            # Para eventos recebidos pelo pygame
            for event in pygame.event.get():
                # Se clicou com o mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button1, button2, button3 = pygame.mouse.get_pressed()
                    x, y = event.pos
                    for bloco in all_sprites_list:
                        # Procura colisão de clique com todos os blocos
                        # vantagem -> ignora se clicar entre dois quadrados
                        if bloco.rect.collidepoint(x, y):
                            # Se clicou com o botão esquerdo do mouse, revela o bloco
                            if button1:
                                if not bloco.revealed:
                                    # Cria thread para enviar clique aos outros jogadores
                                    if GameController.is_multiplayer:
                                        thread_send = Thread(target=thread_send_data, args=(
                                            bloco.posX, bloco.posY, GameController.player_ID, GameController.match, GameController.player_color, ACTION_REGISTER_CLICK))
                                        thread_send.start()
                                    # Não adiciona movimentos quando todas as bombas foram encontradas
                                    if not (GameController.markedBombs == GameController.bombs or isinstance(bloco,Mine)):
                                        GameController.movs += 1
                                    bloco.reveal()
                                    # Adiciona o número de vizinhos no score
                                    GameController.score += bloco.neighbors
                                    # Continua revelando os blocos vizinhos até acabar
                                    while len(blocks_to_reveal) > 0:
                                        bloco = blocks_to_reveal.pop(0)
                                        bloco.reveal()
                                        GameController.score += bloco.neighbors

                                    # Se clicou em uma Mina
                                    if isinstance(bloco,Mine): #and not bloco.marked:
                                        # PERDEU
                                        GameController.round_is_finished = True
                            # Se clicou com o botão direito do mouse, marca o bloco
                            elif button3:
                                # Não marca blocos já marcados e já revelados
                                if not bloco.marked and not  bloco.revealed:
                                    # Cria thread para enviar clique aos outros jogadores
                                    if GameController.is_multiplayer:
                                        thread_send = Thread(target=thread_send_data, args=(bloco.posX, bloco.posY,
                                                                                            GameController.player_ID,
                                                                                            GameController.match,
                                                                                            GameController.player_color,
                                                                                            ACTION_REGISTER_MARK))
                                        thread_send.start()
                                    bloco.mark(GameController.player_color)
                                    # Se marcou uma mina
                                    if isinstance(bloco,Mine):
                                        GameController.markedBombs += 1
                                        GameController.score += 100
                                    # Se não marcou uma mina
                                    else:
                                        GameController.score -= 50

                        # Verifica o término do jogo
                        # Termina quando todos os blocos foram revelados e todas as bombas marcadas
                        if GameController.markedBombs + GameController.revealedBlocks == GameController.totalBlocks:
                            # GANHOU
                            GameController.round_is_finished = True
                            win = True

                # Se usuário quer fechar o jogo
                if event.type == pygame.QUIT:
                    # Termina os dois loops do jogo
                    GameController.round_is_finished = True
                    GameController.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        GameController.round_is_finished = True
                        GameController.done = True

            # Limpa a tela a cada iteração
            screen.fill(COLOR_CLEAR_SCREEN)

            # Redesenha objetos atualizados
            all_sprites_list.draw(screen)
            utils.show_match_info(screen)

            # Muda framerate para 20
            clock.tick(20)

            # Atualiza a tela
            pygame.display.flip()

            # Se uma partida multiplayer está começando (verificado depois da primeira iteração)
            if GameController.is_multiplayer and new_game:
                # Se é o criador da partida
                if GameController.username == GameController.match:
                    # Exibe mensagem e espera por tecla ESPAÇO
                    utils.wait_for_space_key_message(screen)
                else:
                    if not check_match_has_begun():
                        utils.wait_for_match_message(screen)
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
                        # Partida não está conectável
                        utils.match_has_started_message(screen)
                        GameController.round_is_finished = True
                        GameController.done = True
                # Nova partida foi configurada
                new_game = False

        # Terminou rodada, mas não pediu pra sair do jogo
        if not GameController.done:
            screen.fill(COLOR_CLEAR_SCREEN)
            all_sprites_list.draw(screen)
            # Se não ganhou, altera mensagem para LOST e exibe as minas não encontradas
            if not win:
                utils.show_match_info(screen, "YOU HAVE LOST :(", COLOR_RESULT)
                #revela minas
                for mine in mines:
                    mine.reveal_unrevealed()
            # Se ganhou, altera mensagem para WiNNER
            else:
                utils.show_match_info(screen, "WINNER !!1", COLOR_RESULT)

            # Atualiza o score de tanto quem ganhou como perdeu
            pygame.time.wait(1000)
            if not GameController.is_multiplayer:
                screen.fill(COLOR_CLEAR_SCREEN_SCORE)
                utils.show_match_info(screen, "SCORE", COLOR_RESULT)
                # Envia score ao servidor
                register_global_score()
                utils.show_global_score(screen)
                pygame.display.flip()
                pygame.time.wait(1000)
            else:
                # Registra o score da partida multiplayer, mas não exibe ainda
                register_match_score()

            # Espera um clique ou teclas ESPAÇO ou ESCAPE para terminar
            clicked = False

            # Limpa a fila de eventos acumulados anteriormente
            for event in pygame.event.get():
                pass

            # Termina com um clique ou chamando o fim da janela
            while not clicked and not GameController.done:

                # Exibe o placar multiplayer (atualizado a cada iteração)
                if GameController.is_multiplayer:
                    screen.fill(COLOR_CLEAR_SCREEN_SCORE)
                    utils.show_match_info(screen, "SCORE", COLOR_RESULT)
                    utils.show_match_score(screen)
                    pygame.display.flip()

                pygame.time.wait(100)

                # Interpreta eventos recebidos
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True
                    if event.type == pygame.QUIT:
                        GameController.done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            GameController.done = True
                        elif event.key == pygame.K_KP_ENTER:
                            clicked = True
                        elif event.key == pygame.K_SPACE:
                            clicked = True

    # Insere um booleano na lista compartilhada para Thread terminar
    if GameController.is_multiplayer:
        shared_click_list.insert(0,True)

    pygame.quit()
