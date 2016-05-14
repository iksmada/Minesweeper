import pygame
import random
from constants import *

#TODO colocar que tem q erelevar todos blocos, revelar envolta dos gray

MINA_SIZE   = 25 # tamanho de uma mina
BLOCK_SIZE  = 30 # tamanho de um bloco que contem uma mina
COLUMNS     = 10
ROWS        = 10
BOMBS       = 2

PADDING = (BLOCK_SIZE - MINA_SIZE) # espaco entre tabuleiro e minas

# Criando matriz ROWS+1 por COLUMNS+1
# Neste caso, nao sera gerado IndexError quando elemento esta fora da matriz
matrix = [[0 for x in range(COLUMNS + 1)] for y in range(ROWS + 1)]
# Fila de elementos que precisam ser atualizados a cada clique
blocks_to_reveal = []

class Block(pygame.sprite.Sprite):
    """
        Classe Bloco:
            representa uma caixa que contem os elementos do jogo:
            minas (subclasse), avisos de minas ou vazio
    """

    def __init__(self, posX, posY, neighbors=10):
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
        self.rect.y = BLOCK_SIZE * posY + PADDING
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

    def reveal(self, first=False):
        """
            Revela um bloco e adiciona seus vizinhos na lista de blocos para serem revelados
            :param first: indica se este e o primeiro elemento da chamada dessa funcao
            :return: nada
        """

        if self.revealed:
            return

        if first:
            blocks_to_reveal.append(self)

        self.revealed = True
        pygame.time.wait(1)
        all_sprites_list.draw(screen)
        pygame.display.flip()

        if self.neighbors>0:
            # Atualiza numero de bombas no tabuleiro
            self.next_image = pygame.image.load("images/number"+str(self.neighbors)+".png").convert_alpha()
        else:
            # Adiciona vizinhos na lista de blocos para serem revelados
            self.next_image = ACTION_FILL_CLICKED

            bloco = matrix[self.posX + 1][self.posY]
            if type(bloco) is Block and bloco.revealed==False:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX][self.posY + 1]
            if type(bloco) is Block and bloco.revealed == False:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX - 1][self.posY]
            if type(bloco) is Block and bloco.revealed == False:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX + 1][self.posY + 1]
            if type(bloco) is Block and bloco.revealed == False:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX - 1][self.posY + 1]
            if type(bloco) is Block and bloco.revealed == False:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX + 1][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False:
                blocks_to_reveal.append(bloco)

            bloco = matrix[self.posX - 1][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False:
                blocks_to_reveal.append(bloco)

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
            self.next_image = pygame.image.load("images/mark1.png").convert_alpha()
            self.marked=True
            self.update_image()


class Mina(Block):

    def reveal(self, first=False):

        if not self.revealed:
            self.next_image = pygame.image.load("images/mina.png").convert_alpha()

        if first:
            blocks_to_reveal.append(self)

        self.revealed = True

    def __str__(self):
        return "mina"

# Initialize Pygame
pygame.init()

#tamanho da janela depende do numero de columas linhas e do tamanho de cada celula da matrix
screen_width  = COLUMNS * BLOCK_SIZE + PADDING
screen_height =    ROWS * BLOCK_SIZE + PADDING
screen = pygame.display.set_mode([screen_width, screen_height])

#grupo dos elementos de minas e total
mines = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


#cria bombas
i=0
while i < BOMBS:

    empty=True
    posX=random.randrange(COLUMNS)
    posY=random.randrange(ROWS)
   # print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
    if matrix[posX][posY]==0:
        mina = Mina(posX,posY)
        matrix[posX][posY]=mina
    # Add the block to the list of objects
        mines.add(mina)
        all_sprites_list.add(mina)
        i+=1
       # print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

for posX in range(COLUMNS):
    for posY in range(ROWS):
        #print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
        if matrix[posX][posY] == 0:
            neighbors = 0
            if type(matrix[posX + 1][posY]) is Mina:
                neighbors += 1
            if type(matrix[posX][posY + 1]) is Mina:
                neighbors += 1
            if type(matrix[posX - 1][posY]) is Mina:
                neighbors += 1
            if type(matrix[posX][posY - 1]) is Mina:
                neighbors += 1
            if type(matrix[posX + 1][posY + 1]) is Mina:
                neighbors += 1
            if type(matrix[posX - 1][posY + 1]) is Mina:
                neighbors += 1
            if type(matrix[posX + 1][posY - 1]) is Mina:
                neighbors += 1
            if type(matrix[posX - 1][posY - 1]) is Mina:
                neighbors += 1

            block = Block(posX,posY,neighbors)
            matrix[posX][posY] = block
            all_sprites_list.add(block)
            #print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

# Create a red player block
#player = Player(RED, 20, 20)
#all_sprites_list.add(player)

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done=True

        if event.type == pygame.MOUSEBUTTONDOWN:
            button1, button2, button3 = pygame.mouse.get_pressed()
            x, y = event.pos
            bombMarked=0
            blocksRevealed=0
            for block in all_sprites_list:
                if block.rect.collidepoint(x, y):
                    if button1:
                        block.reveal(True)
                        while len(blocks_to_reveal) > 0:
                            block.update_image()
                            block = blocks_to_reveal.pop(0)
                            block.reveal()
                # usa colisao:
                # vantagem -> ignora se clicar entre dois quadrados

                    elif button3:
                #print "matrix[" + str(x / MATRIXSIZE) + "][" + str(y / MATRIXSIZE) + "] = " + str(matrix[x / MATRIXSIZE][y / MATRIXSIZE])
                        block.mark()
                    #se for Mina
                if type(block)==Mina:
                        #revelou uma mina
                    if block.revealed == True:
                        #PERDEU
                        done=True
                        #marcou uma mina
                    if block.marked == True:
                        bombMarked+=1
                    #se for bloco normal ese revelou o bloco
                elif block.revealed == True:
                        blocksRevealed+=1
                    #se marcou todas as bombas e revelou todos os blocos
                #print "bombas marcadas:"+str(bombMarked)+" e blocos revelados:"+ str(blocksRevealed)
            if bombMarked==BOMBS and blocksRevealed==(COLUMNS*ROWS-BOMBS):
                        #GANHOU
                done=True;

        # Clear the screen
    screen.fill(GRAYDARK)

    #for block in all_sprites_list: block.reveal()
    all_sprites_list.draw(screen)
    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
