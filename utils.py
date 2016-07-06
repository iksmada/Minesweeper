# -*- coding: utf-8

from server_handler import compute_total
from multiplayer import *
from classes import *
from constants import *

"""
    Arquivo com métodos auxiliares
"""

def show_match_info(screen, text="MINESWEEPER", color=COLOR_TITLE):
    """
        Método que insere as informações da partida na janela do jogo
    :param screen: objeto que representa a tela/janela onde outros objetos são desenhados
    :param text: texto a ser exibido
    :param color: cor do texto a ser exibido
    :return: nada
    """

    # Seleciona a maior fonte possível e escreve o conteúdo de 'texto' centralizado na parte superior da tela
    font = pygame.font.Font('fonts/UbuntuMonoBold.ttf', get_recommended_font_size(screen, 100, text))
    title = font.render(text, 1, color)
    screen.blit(title, (GameController.screen_width / 2 - (PADDING + title.get_size()[0]) / 2, PADDING))

    # Verifica qual das mensagens é a maior entre elas para encontrar tamanho de fonte adequado
    username = "USERNAME: %s" % GameController.username
    match = "MATCH: %s" % GameController.match
    if len(username) >= len(match):
        text = username
    else:
        text = match
    # Se o tamanho máximo é maior que o desejado, escolha o desejado; se não, escolha o máximo
    if get_recommended_font_size(screen,45,text) > NORMAL_FONT_SIZE:
        font = pygame.font.Font('fonts/UbuntuMono.ttf', NORMAL_FONT_SIZE)
    else:
        font = pygame.font.Font('fonts/UbuntuMono.ttf', get_recommended_font_size(screen,45,text))

    # Exibe a quantidade de pontos obtidos na janela
    score_text = font.render("%5s %07d" % ('SCORE', GameController.score), 1, COLOR_MENU_POINTS)
    screen.blit(score_text, (PADDING, PADDING + 2*BLOCK_SIZE))

    # Exibe a quantidade de cliques/movimentos na janela
    movs = font.render("%-9s %03d " % ('MOVS',GameController.movs), 1, COLOR_MENU_POINTS)
    screen.blit(movs, (PADDING, PADDING + 3*BLOCK_SIZE))

    # Exibe o nome de usuário na janela
    username = font.render(username, 1, COLOR_MENU_POINTS)
    screen.blit(username, (GameController.screen_width-(PADDING + username.get_size()[0]),PADDING + 2*BLOCK_SIZE))

    # Se for uma partida multiplayer, exibe o nome da partida na janela
    if GameController.is_multiplayer:
        match = font.render(match, 1, COLOR_MENU_POINTS)
        screen.blit(match, (GameController.screen_width-(PADDING + match.get_size()[0]), PADDING + 3*BLOCK_SIZE))


def get_recommended_font_size(screen_object,screen_percentage,text):
    """
        Método que calcula o maior tamanho de fonte possível para um texto em uma parte da janela
    :param screen_object: objeto da janela para renderizar o texto
    :param screen_percentage: porcentagem da tela que o texto deve aparecer
    :param text: texto a ser renderizado
    :return: tamanho máximo recomendado de fonte
    """
    width = int(screen_object.get_width()*screen_percentage/100)

    font = pygame.font.Font('fonts/UbuntuMono.ttf', HUGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return HUGE_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', EXTRA_LARGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return EXTRA_LARGE_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', LARGE_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return LARGE_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', NORMAL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return NORMAL_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', SMALL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return SMALL_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', EXTRA_SMALL_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return EXTRA_SMALL_FONT_SIZE

    font = pygame.font.Font('fonts/UbuntuMono.ttf', TINY_FONT_SIZE)
    render = font.render(text, 1, BLACK)
    if width > render.get_width():
        return TINY_FONT_SIZE

    return TINY_FONT_SIZE

def wait_for_space_key_message(screen):
    """
        Método que espera que a barra de espaço seja pressionada para uma partida começar
        Exibe uma mensagem enquanto estiver sendo executado
    :param screen: objeto que representa a tela/janela onde outros objetos são desenhados
    :return: nada
    """
    message = 'PRESS SPACE TO START MATCH'
    font = pygame.font.Font(None, min(EXTRA_LARGE_FONT_SIZE,get_recommended_font_size(screen,95,message)))
    wait = font.render(message, 1, BLACK)
    screen.blit(wait, ((GameController.screen_width - wait.get_size()[0]) / 2,
                (GameController.screen_height + TITLE_AND_SCORE_SIZE - wait.get_size()[1]) / 2))
    pygame.display.flip()

    set_up_new_match() # Partida se torna conectável
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                    start_match()
                elif event.key == pygame.K_ESCAPE:
                    GameController.round_is_finished = True
                    GameController.done = True
                    done = True
                    delete_match()
            elif event.type == pygame.QUIT:
                GameController.round_is_finished = True
                GameController.done = True
                done = True
                delete_match()



def wait_for_match_message(screen):
    """
        Método que exibe uma mensagem para esperar a partid começar
    :param screen: objeto que representa a tela/janela onde outros objetos são desenhados
    :return: nada
    """
    message = 'WAIT FOR MATCH TO START'
    font = pygame.font.Font(None, min(EXTRA_LARGE_FONT_SIZE,get_recommended_font_size(screen,95,message)))
    wait = font.render(message, 1, BLACK)
    screen.blit(wait, ((GameController.screen_width - wait.get_size()[0]) / 2,
                (GameController.screen_height + TITLE_AND_SCORE_SIZE - wait.get_size()[1]) / 2))
    pygame.display.flip()

def match_has_started_message(screen):
    """
        Método que exibe uma mensagem que a partida já terminou
    :param screen: objeto que representa a tela/janela onde outros objetos são desenhados
    :return: nada
    """
    message = 'SORRY, MATCH IS UNAVALAIBLE :('
    font = pygame.font.Font(None, min(EXTRA_LARGE_FONT_SIZE,get_recommended_font_size(screen,95,message)))
    wait = font.render(message, 1, BLACK)
    screen.blit(wait, ((GameController.screen_width - wait.get_size()[0]) / 2,
                       (GameController.screen_height + TITLE_AND_SCORE_SIZE - wait.get_size()[1]) / 2))
    pygame.display.flip()

    pygame.time.delay(3000)

def match_has_finished_message(screen):
    """
        Método que exibe uma mensagem que a partida já terminou
    :param screen: objeto que representa a tela/janela onde outros objetos são desenhados
    :return: nada
    """
    message = 'SORRY, MATCH WAS FINISHED BY HOST :('
    font = pygame.font.Font(None, min(EXTRA_LARGE_FONT_SIZE,get_recommended_font_size(screen,95,message)))
    wait = font.render(message, 1, BLACK)
    screen.blit(wait, ((GameController.screen_width - wait.get_size()[0]) / 2,
                       (GameController.screen_height + TITLE_AND_SCORE_SIZE - wait.get_size()[1]) / 2 + 2*BLOCK_SIZE))
    pygame.display.flip()

    pygame.time.delay(3000)

def show_global_score(screen):
    """
        Método que exibe o score global para partidas single player
        Mostra em branco scores de outros usuários
        Mostra em azul scores do usuário atual
        Mostra em verde o score da última partida
        Exibe o score conseguido na posição exata dentre os 5 melhores ou após todos eles

    :param screen: objeto que representa a tela/janela onde outros objetos são desenhados
    :return: nada
    """
    #Pega a lista com os resultados
    scores = get_global_score()
    # Altura inicial do primeiro score
    height = BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE
    step = BLOCK_SIZE*GameController.rows/float(7)
    font = pygame.font.Font('fonts/UbuntuMonoBold.ttf', SMALL_FONT_SIZE)

    # Exibe a descrição da tabela de acordo com o tamanho da tela
    if GameController.columns >= 20:
        message = '%-12s %5s %7s %5s %7s %5s %8s' % tuple('USERNAME ROWS COLUMNS BOMBS SCORE MOVS TOTAL'.split())
    elif GameController.columns >= 15:
        message = '%-12s %5s %5s %8s' % tuple('USERNAME SCORE MOVS TOTAL'.split())
    else:
        message = '%-12s %8s' % tuple('USERNAME TOTAL'.split())

    wait = font.render(message, 1, COLOR_TITLE)
    screen.blit(wait, ((GameController.screen_width - wait.get_width())/2 , height))
    pygame.display.flip()

    has_scored = False # Variável de controle para saber se usuário conseguiu um dos 5 melhores
    for score in scores:
        height += step
        # score = (total, username, rows, cols, bombs, score, movs)
        if GameController.columns >= 20:
            message = '%-12s %5d %7d %5s %7d %5d %8d' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
        elif GameController.columns >= 15:
            message = '%-12s %5d %5d %8d' % (score[1], score[5], score[6], score[0])
        else:
            message = '%-12s %8d' % (score[1], score[0])
        if score[1] == GameController.username  \
            and score[5] == GameController.score \
            and score[6] == GameController.movs:
            wait = font.render(message, 1, COLOR_THIS_SCORE)
            # Score atual é o Score da última partida
            has_scored = True
        elif score[1] == GameController.username:
            wait = font.render(message, 1, COLOR_MY_SCORE)
        else:
            wait = font.render(message, 1, COLOR_OTHER_SCORE)
        screen.blit(wait, ((GameController.screen_width - wait.get_width())/2, height))
        pygame.time.wait(100)
        pygame.display.flip()



    if not has_scored:
        # Calcula o score da última partida localmente
        total = compute_total(GameController.rows, GameController.columns, GameController.bombs_percentage,
                              GameController.score, GameController.movs)
        score = (total, GameController.username, GameController.rows,
                 GameController.columns, GameController.bombs_percentage,
                 GameController.score, GameController.movs)
        if GameController.columns >= 20:
            message = '%-12s %5d %7d %5s %7d %5d %8d' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
        elif GameController.columns >= 15:
            message = '%-12s %5d %5d %8d' % (score[1], score[5], score[6], score[0])
        else:
            message = '%-12s %8d' % (score[1], score[0])
        wait = font.render(message, 1, COLOR_THIS_SCORE)
        screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + step))
        pygame.time.wait(100)
        pygame.display.flip()

    # Exibe mensagem do cálculo do score final
    message = 'TOTAL = SCORE + (ROWS*COLS/50)% - (MOVS-BOMBS)%'
    font = pygame.font.Font('fonts/UbuntuMono.ttf', min(NORMAL_FONT_SIZE,get_recommended_font_size(screen,100,message)))
    wait = font.render(message, 1, COLOR_RESULT)
    screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + 2*step))
    pygame.time.wait(100)
    pygame.display.flip()

def show_match_score(screen):
    """
        Método que exibe o score de uma partida multiplayer
        Mostra em branco scores de outros usuários
        Mostra em azul scores do usuário atual
        Mostra em verde o score da última partida
        Exibe o score conseguido na posição exata dentre os 5 melhores ou após todos eles
        Exibe um score temporário para usuários que ainda não terminaram a partida
        Não tem delay entre scores

    :param screen: objeto que representa a tela/janela onde outros objetos são desenhados
    :return: nada
    """
    scores = get_match_score()
    all_players = get_match_players()
    # Pega o nome de usuário de todos os usuários que já tem score registrado
    finished_players = [score[1] for score in scores]

    all_players.sort()
    for player in all_players:
        if player not in finished_players:
            scores.append(('?????', player, 0, 0, 0, 0, 0))

    # Comportamento igual que show_global_score()
    height = BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE
    step = BLOCK_SIZE*GameController.rows/float(7)
    font = pygame.font.Font('fonts/UbuntuMonoBold.ttf', SMALL_FONT_SIZE)

    if GameController.columns >= 20:
        message = '%-12s %5s %7s %5s %7s %5s %8s' % tuple('USERNAME ROWS COLUMNS BOMBS SCORE MOVS TOTAL'.split())
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
            message = '%-12s %5d %7d %5s %7d %5d %8s' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
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
            message = '%-12s %5d %7d %5s %7d %5d %8d' % (score[1], score[2], score[3], str(score[4])+'%', score[5], score[6], score[0])
        elif GameController.columns >= 15:
            message = '%-12s %5d %5d %8d' % (score[1], score[5], score[6], score[0])
        else:
            message = '%-12s %8d' % (score[1], score[0])
        wait = font.render(message, 1, COLOR_THIS_SCORE)
        screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + step))
        pygame.time.wait(100)
        pygame.display.flip()

    message = 'TOTAL = SCORE + (ROWS*COLS/50)% - (MOVS-BOMBS)%'
    font = pygame.font.Font('fonts/UbuntuMono.ttf', min(NORMAL_FONT_SIZE,get_recommended_font_size(screen,100,message)))
    wait = font.render(message, 1, COLOR_RESULT)
    screen.blit(wait, ((GameController.screen_width - wait.get_width()) / 2, height + 2*step))
