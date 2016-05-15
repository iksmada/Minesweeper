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
        GameController.score += self.neighbors
        GameController.revealedBlocks += 1

        if self.neighbors>0:
            # Atualiza numero de bombas no tabuleiro
            self.next_image = pygame.image.load("images/number"+str(self.neighbors)+".png").convert_alpha()
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
            GameController.score -= 10
            #muda imagem para marcacao
            self.next_image = pygame.image.load("images/mark1.png").convert_alpha()
            self.marked=True
            self.update_image()


class Mine(Block):

    def reveal(self):

        if not self.revealed:
            self.next_image = pygame.image.load("images/mina.png").convert_alpha()

        self.revealed = True
        GameController.score -= 10
        GameController.movs += 1

        self.update_image()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def mark(self):
        if not self.marked:
            super(Mine,self).mark()
            # Chamando o pai, entao 10 pontos sao removidos e entao mais 10 + 10 sao adicionados
            GameController.score += 20

    def __repr__(self):
        return "Mine" + super(Mine,self).__repr__()

class GameController:

    # Atributos estaticos atualizados no main()
    score = None
    movs = None
    markedBombs = None
    revealedBlocks = None

    def __init__(self):
        raise AssertionError('Classe GameController nao tem instancias.')

    @staticmethod
    def draw(screen,top="MINESWEEPER",color=COLOR_TITLE):
        font = pygame.font.Font(None, BLOCK_SIZE)
        title = font.render(top, 1, color)
        screen.blit(title, (SCREEN_WIDTH/2 - (PADDING + title.get_size()[0])/2, PADDING/2))
        movs = font.render("MOVS: %3d" % GameController.movs, 1, COLOR_SCORE)
        screen.blit(movs, (PADDING,PADDING/2))
        score = font.render("SCORE: %3d" % GameController.score, 1, COLOR_SCORE)
        screen.blit(score, (SCREEN_WIDTH - (PADDING + score.get_size()[0]), PADDING/2))