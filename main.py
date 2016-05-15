import pygame
import random
from constants import *

#TODO Placa e wait avisando se ganho uo perdeu e quantos pontos
#TODO pintar de vermelho bomba que clicou e fez perde

MINA_SIZE   = 20 # tamanho de uma mina
BLOCK_SIZE  = 22 # tamanho de um bloco que contem uma mina
COLUMNS     = 10
ROWS        = 10
BOMBS       = 2

PADDING = (BLOCK_SIZE - MINA_SIZE) # espaco entre tabuleiro e minas
TITLE_AND_SCORE_SIZE = BLOCK_SIZE
# tamanho da janela depende do numero de columas linhas e do tamanho de cada celula da matrix
SCREEN_WIDTH  = COLUMNS * BLOCK_SIZE + PADDING
SCREEN_HEIGHT = ROWS * BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE

class Block(pygame.sprite.Sprite):
    """
        Classe Bloco:
            representa uma caixa que contem os elementos do jogo:
            minas (subclasse), avisos de minas ou vazio
    """

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
        vizinhos = 'N:' + str(neighbors)
        revelado = 'REVELADO' if self.revealed else 'NAO_REVELADO'
        marcado = 'MARCADO' if self.marked else 'NAO_MARCADO'

        return posicao + ' ' + vizinhos + ' ' + revelado + ' ' + marcado

    def reveal(self):
        """
            Revela um bloco e adiciona seus vizinhos na lista de blocos para serem revelados
            :param first: indica se este e o primeiro elemento da chamada dessa funcao
            :return: nada
        """

        if self.revealed:
            return

        title_score.score += block.neighbors
        self.revealed = True

        if self.neighbors>0:
            # Atualiza numero de bombas no tabuleiro
            self.next_image = pygame.image.load("images/number"+str(self.neighbors)+".png").convert_alpha()
        else:
            # Adiciona vizinhos na lista de blocos para serem revelados
            self.next_image = ACTION_FILL_CLICKED

            bloco = matrix[self.posX + 1][self.posY]
            if type(bloco) is Block and not bloco.revealed \
                    and blocks_to_reveal.count(bloco)==0: #se ja estiver na lista nao coloca denovo
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX][self.posY + 1]
            if type(bloco) is Block and not bloco.revealed  \
                    and blocks_to_reveal.count(bloco) == 0:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX - 1][self.posY]
            if type(bloco) is Block and not bloco.revealed \
                    and blocks_to_reveal.count(bloco) == 0:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX][self.posY - 1]
            if type(bloco) is Block and not bloco.revealed \
                    and blocks_to_reveal.count(bloco) == 0:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX + 1][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False \
                    and blocks_to_reveal.count(bloco) == 0:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX + 1][self.posY + 1]
            if type(bloco) is Block and not bloco.revealed  \
                    and blocks_to_reveal.count(bloco) == 0:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX - 1][self.posY + 1]
            if type(bloco) is Block and not bloco.revealed \
                    and blocks_to_reveal.count(bloco) == 0:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX - 1][self.posY - 1]
            if type(bloco) is Block and not bloco.revealed \
                    and blocks_to_reveal.count(bloco) == 0:
                blocks_to_reveal.append(bloco)

        self.update_image()
        all_sprites_list.draw(screen)
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
            title_score.movs += 1

            #muda imagem para marcacao
            self.next_image = pygame.image.load("images/mark1.png").convert_alpha()
            self.marked=True
            self.update_image()


class Mine(Block):

    def reveal(self):

        if not self.revealed:
            self.next_image = pygame.image.load("images/mina.png").convert_alpha()

        self.revealed = True

        self.update_image()
        all_sprites_list.draw(screen)
        pygame.display.flip()

    def __repr__(self):
        return "Mine" + super(Mine,self).__repr__()

class Title_and_Score:

    def __init__(self,score=0):
        #super(Title,self).__init__()
        self.score = score
        self.movs = 0
        self.font = pygame.font.Font(None, SCREEN_WIDTH/15)

    def draw(self,top="MINESWEEPER",color=COLOR_TITLE):
        title = self.font.render(top, 1, color)
        screen.blit(title, (SCREEN_WIDTH/2 - (PADDING + title.get_size()[0])/2, PADDING/2))
        movs = self.font.render("MOVS: %3d" % self.movs, 1, COLOR_SCORE)
        screen.blit(movs, (PADDING,PADDING/2))
        score = self.font.render("SCORE: %3d" % self.score, 1, COLOR_SCORE)
        screen.blit(score, (SCREEN_WIDTH - (PADDING + score.get_size()[0]), PADDING/2))

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

title_score = Title_and_Score()

done = False

#score = 0

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

    i=0
    while i < BOMBS:

        posX=random.randrange(COLUMNS)
        posY=random.randrange(ROWS)
       # print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
        if matrix[posX][posY]==0:
            mine = Mine(posX,posY)
            matrix[posX][posY]=mine
        # Add the block to the list of objects
            mines.add(mine)
            all_sprites_list.add(mine)
            i+=1
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

                block = Block(posX,posY,neighbors)
                matrix[posX][posY] = block
                all_sprites_list.add(block)
                #print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

    #Loop until the user clicks the close button.
    round_is_finished = False
    win=False
    title_score.movs=0

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not round_is_finished:
        for event in pygame.event.get(): # User did something

            if event.type == pygame.MOUSEBUTTONDOWN:
                button1, button2, button3 = pygame.mouse.get_pressed()
                x, y = event.pos
                bombsMarked=0
                blocksRevealed=0
                for block in all_sprites_list:
                    if block.rect.collidepoint(x, y):
                        if button1:
                            if not block.revealed: title_score.movs+=1
                            block.reveal()
                            while len(blocks_to_reveal) > 0:
                                block = blocks_to_reveal.pop(0)
                                block.reveal()
                    # usa colisao:
                    # vantagem -> ignora se clicar entre dois quadrados

                        elif button3:
                            block.mark()
                        #se for mina
                    if type(block)==Mine:
                            #revelou uma mina
                        if block.revealed:
                            #PERDEU
                            round_is_finished=True
                            #marcou uma mina
                        if block.marked:
                            bombsMarked+=1
                    #se for bloco normal e se revelou o bloco
                    elif block.revealed:
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

pygame.quit()
