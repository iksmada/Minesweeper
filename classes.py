# -*- coding: utf-8
import pygame
from constants import *

class GameController:
    """
        Classe estática que faz o controle das variáveis do jogo.
        Todo o acesso é feito por meio de variáveis estáticas da classe

        A classe não pode ser instanciada
    """

    # Atributos estáticos da classe
    rows =                  None # número de linhas do tabuleiro
    columns =               None # número de colunas do tabuleiro
    bombs =                 None # número de bombas de uma partida
    bombs_percentage =      None # porcentagem de bombas de uma partida

    screen_width =          None # tamanho de comprimento da tela
    screen_height =         None # tamanho de largura da tela
    is_multiplayer =        None # booleano para controle se é uma partida multiplayer

    done =                  None # booleano para controle se o jogo acabou
    round_is_finished =     None # booleano para controle se uma partida acabou

    score =                 None # contador de pontos de uma partida
    movs =                  None # contador de cliques de uma partida
    markedBombs =           None # contador de bombas marcadas
    revealedBlocks =        None # contador de blocos revelados (foram clicados ou vizinhos de clicados)
    totalBlocks =           None # contador de blocos totais no tabuleiro

    username =              None # nome do usuário
    player_ID =             None # identificador local de um usuário usado nas partidas multiplayer
    match =                 None # nome do usuário que criou a sala
    player_color =          None # cor de bandeira selecionada pelo usuário

    def __init__(self):
        raise AssertionError('Classe GameController não é instanciável.')

class Block(pygame.sprite.Sprite):
    """
        Classe Bloco:
        Representa um container para os elementos do jogo:
        Blocos (vazios ou com vizinhos) ou Minas (subclasse)
    """

    # Atributos estáticos da classe (e compartilhados com game.py)
    matrix =            None
    blocks_to_reveal =  None
    all_sprites_list =  None
    screen =            None

    def __init__(self, posX, posY, neighbors=0):
        """
            Construtor da classe
        :param posX: inteiro da posição x de 0 a rows-1 do Bloco no tabuleiro
        :param posY: inteiro da posição y de 0 a colums-1 do Bloco no tabuleiro
        :param neighbors: número de minas vizinhas desse Bloco
        """
        # Chama o construtor do Pai
        super(Block,self).__init__()

        self.image = pygame.Surface([MINA_SIZE, MINA_SIZE]) # Conteúdo do bloco
        self.image.fill(COLOR_UNCLICKED_BLOCK)
        self.next_image = None         # Representa o image depois que uma atualizacao acontece

        self.posX=posX                 # Posições do elemento na matriz do tabuleiro
        self.posY=posY

        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE * posX + PADDING + BLOCK_SIZE
        self.rect.y = BLOCK_SIZE * posY + PADDING + TITLE_AND_SCORE_SIZE + BLOCK_SIZE

        self.neighbors = neighbors      # Número de minas vizinhas desse bloco

        self.revealed = False           # Representa se este bloco já foi revelado pelo/ao usuário
        self.marked = False             # Representa se o usuario marcou este bloco com uma bandeira

    def __repr__(self):
        """
            Cria uma represetação de um bloco com posição, vizinhos, se já foi revelado ou marcado
            :return: string criada
        """

        posicao = '(%d,%d)' % (self.posX, self.posY)
        vizinhos = 'N:' + str(self.neighbors)
        revelado = 'REVELADO' if self.revealed else 'NAO_REVELADO'
        marcado = 'MARCADO' if self.marked else 'NAO_MARCADO'

        return posicao + ' ' + vizinhos + ' ' + revelado + ' ' + marcado

    def reveal(self):
        """
            Revela o conteúdo de um bloco e adiciona seus vizinhos na lista de blocos para serem revelados
            :return: nada
        """

        if self.revealed:
            return

        # Revela e adiciona contador de blocos revelados
        self.revealed = True
        GameController.revealedBlocks += 1

        if self.neighbors > 0:
            # Atualiza imagem do número de bombas no tabuleiro
            self.next_image = pygame.image.load("images/number_"+str(self.neighbors)+".png").convert_alpha()
        else:
            # Muda de cor e adiciona vizinhos na lista de blocos para serem revelados
            # PS: se já estiver na lista, não insere de novo
            self.next_image = ACTION_FILL_CLICKED

            bloco = self.matrix[self.posX + 1][self.posY]
            if type(bloco) is Block and not bloco.revealed \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

            bloco = self.matrix[self.posX][self.posY + 1]
            if type(bloco) is Block and not bloco.revealed  \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

            bloco = self.matrix[self.posX - 1][self.posY]
            if type(bloco) is Block and not bloco.revealed \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

            bloco = self.matrix[self.posX][self.posY - 1]
            if type(bloco) is Block and not bloco.revealed \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

            bloco = self.matrix[self.posX + 1][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

            bloco = self.matrix[self.posX + 1][self.posY + 1]
            if type(bloco) is Block and not bloco.revealed  \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

            bloco = self.matrix[self.posX - 1][self.posY + 1]
            if type(bloco) is Block and not bloco.revealed \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

            bloco = self.matrix[self.posX - 1][self.posY - 1]
            if type(bloco) is Block and not bloco.revealed \
                    and self.blocks_to_reveal.count(bloco) == 0:
                self.blocks_to_reveal.append(bloco)

        # Atualiza gráficos de todos os blocos alterados
        self.update_image()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
        pygame.time.wait(1)

    def update_image(self):
        """
            Atualiza imagem do bloco para a imagem previamente carregada em next_image
            :return: nada
        """

        if self.next_image is not None:
            if self.next_image == ACTION_FILL_CLICKED:
                # Objeto imagem é preenchido completamente com uma única cor
                self.image.fill(COLOR_CLICKED_BLOCK)
            else:
                self.image = pygame.transform.scale(self.next_image,[MINA_SIZE,MINA_SIZE])

        self.next_image = None

    def mark(self, color):
        """
            Marca um bloco se ele não foi revelado ou marcado
            :return: nada
        """
        # Se o bloco ainda não foi revelado ou marcado
        if not self.revealed and not self.marked:
            # Altera para o gráfico de um bloco marcado
            self.next_image = pygame.image.load("images/mark_" + str(color) + ".png").convert_alpha()
            self.marked=True
            self.update_image()
            self.all_sprites_list.draw(self.screen)
            pygame.display.flip()


class Mine(Block):
    """
        Classe Mina (filha de Bloco):
        Representa uma mina/bomba no jogo. Sobrescreve alguns métodos de Bloco
    """

    def reveal(self):
        """
            Revela o conteúdo de uma Mina que explodiu
        :return: nada
        """

        if not self.revealed: #and not self.marked:
            self.next_image = pygame.image.load("images/mine_exploded.png").convert_alpha()
            self.revealed = True

        self.update_image()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def reveal_unrevealed(self):
        """
            Revela o conteúdo de uma Mina que não explodiu
        :return:
        """
        if not self.revealed and not self.marked:
            self.next_image = pygame.image.load("images/mine.png").convert_alpha()
            self.revealed = True

        self.update_image()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def __repr__(self):
        """
            Cria uma representação literal de uma mina
        :return: string criada
        """
        return "Mine " + super(Mine,self).__repr__()
