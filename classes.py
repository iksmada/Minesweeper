import pygame
from constants import *

class Block(pygame.sprite.Sprite):
    """
        Classe Bloco:
            representa uma caixa que contem os elementos do jogo:
            minas (subclasse), avisos de minas ou vazio
    """

    # Atributos estaticos atualizados no main()
    matrix = None
    blocks_to_reveal = None
    all_sprites_list = None
    screen = None

    def __init__(self, posX, posY, neighbors=-10):
        # Chama o construtor do Pai
        super(Block,self).__init__()
        # image representa o elemento interno da caixa
        self.image = pygame.Surface([MINA_SIZE, MINA_SIZE])
        self.image.fill(COLOR_UNCLICKED_BLOCK)
        # next_image representa o image depois que uma atualizacao acontece
        self.next_image = None
        # posX e posY sao as posicoes do elemento na matriz. Utilizados para encontrar os vizinhos
        self.posX=posX
        self.posY=posY
        # objeto retangulo que contem o bloco
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE * posX + PADDING
        self.rect.y = BLOCK_SIZE * posY + PADDING + TITLE_AND_SCORE_SIZE
        # neighbors e o numero de minas vizinhas desse bloco
        self.neighbors = neighbors
        # revealed representa se este bloco ja foi revelado pelo/ao usuario
        self.revealed=False
        # marked representa se o usuario marcou este bloco com uma bandeira
        self.marked = False

    def __repr__(self):
        """
            Cria uma string com posicao, vizinhos, se ja foi revelado ou marcado
            :return: string com informacao
        """

        posicao = '(%d,%d)' % (self.posX, self.posY)
        vizinhos = 'N:' + str(self.neighbors)
        revelado = 'REVELADO' if self.revealed else 'NAO_REVELADO'
        marcado = 'MARCADO' if self.marked else 'NAO_MARCADO'

        return posicao + ' ' + vizinhos + ' ' + revelado + ' ' + marcado

    def reveal(self):
        """
            Revela um bloco e adiciona seus vizinhos na lista de blocos para serem revelados
            :return: nada
        """

        if self.revealed:
            return

        self.revealed = True
        #GameController.score += self.neighbors
        GameController.revealedBlocks += 1

        if self.neighbors>0:
            # Atualiza numero de bombas no tabuleiro
            self.next_image = pygame.image.load("images/number_"+str(self.neighbors)+".png").convert_alpha()
        else:
            # Adiciona vizinhos na lista de blocos para serem revelados
            self.next_image = ACTION_FILL_CLICKED

            bloco = self.matrix[self.posX + 1][self.posY]
            if type(bloco) is Block and not bloco.revealed \
                    and self.blocks_to_reveal.count(bloco)==0: #se ja estiver na lista nao coloca denovo
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

        self.update_image()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
        pygame.time.wait(1)

    def update_image(self):
        """
            Atualiza image para a imagem previamente carregada em next_image
            :return: nada
        """

        if self.next_image is not None:
            if self.next_image == ACTION_FILL_CLICKED:
                self.image.fill(GRAYDARK)
            else:
                self.image = pygame.transform.scale(self.next_image,[MINA_SIZE,MINA_SIZE])

        self.next_image = None

    def mark(self):
        """
            Marca um bloco se ele nao foi revelado ou marcado
            :return: nada
        """
        if not self.revealed and not self.marked:
            #conta movimentos, ja faz a checagem pra nao checar mais de uma vez
            #GameController.score -= 10
            #muda imagem para marcacao
            self.next_image = pygame.image.load("images/mark_red.png").convert_alpha()
            self.marked=True
            self.update_image()
            self.all_sprites_list.draw(self.screen)
            pygame.display.flip()


class Mine(Block):

    def reveal(self):

        if not self.revealed and not self.marked:
            self.next_image = pygame.image.load("images/mine_exploded.png").convert_alpha()
            self.revealed = True
            #GameController.score -= 10

        self.update_image()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def reveal_unrevealed(self):

        if not self.revealed and not self.marked:
            self.next_image = pygame.image.load("images/mine.png").convert_alpha()
            self.revealed = True

        self.update_image()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def mark(self):
        if not self.marked:
            # Chamando o pai, entao 10 pontos sao removidos e entao mais -10 +20 sao adicionados
            #GameController.score += 20
            super(Mine,self).mark()


    def __repr__(self):
        return "Mine" + super(Mine,self).__repr__()

class GameController:

    # Atributos estaticos atualizados no main()
    is_multiplayer = False
    rows = 10
    columns = 20
    bombs = 10  # 10% do tabuleiro sao bombas
    screen_width = columns * BLOCK_SIZE + PADDING
    screen_height = rows * BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE
    done = False
    round_is_finished = False
    score = 0
    movs = None
    markedBombs = None
    revealedBlocks = None
    totalBlocks = rows*columns
    username = ''
    player_ID = 0
    match_ID = ''

    def __init__(self):
        raise AssertionError('Classe GameController nao tem instancias.')

    @staticmethod
    def draw(screen,top="MINESWEEPER",color=COLOR_TITLE):
        if GameController.screen_width/15>BLOCK_SIZE:
            font = pygame.font.Font(None, NORMAL_FONT_SIZE)
        else:
            font = pygame.font.Font(None, GameController.screen_width / 15)
        title = font.render(top, 1, color)
        screen.blit(title, (GameController.screen_width/2 - (PADDING + title.get_size()[0])/2, PADDING + BLOCK_SIZE/2))
        score_text = font.render("SCORE: %05d" % GameController.score, 1, COLOR_SCORE)
        screen.blit(score_text, (PADDING, PADDING))
        movs = font.render("MOVS: %03d " % GameController.movs, 1, COLOR_SCORE)
        screen.blit(movs, (PADDING, PADDING + BLOCK_SIZE))
        username = font.render("USERNAME: %s " % GameController.username, 1, COLOR_SCORE)
        screen.blit(username, (GameController.screen_width-(PADDING + username.get_size()[0]),PADDING))
        if GameController.is_multiplayer:
            match = font.render("MATCH: %s " % GameController.match_ID, 1, COLOR_SCORE)
            screen.blit(match, (GameController.screen_width-(PADDING + match.get_size()[0]), PADDING + BLOCK_SIZE))