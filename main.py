import pygame
import random
from constants import *
#colocar que tem q erelevar todos blocos, revelar envolta dos gray
MINA_SIZE   = 20 # tamanho de uma mina
BLOCK_SIZE  = 24 # tamanho de um bloco que contem uma mina
COLUMNS     = 10
ROWS        = 10
BOMBS       = 2

PADDING = (BLOCK_SIZE - MINA_SIZE) # espaco entre tabuleiro e minas

# Criando matriz ROWS+1 por COLUMNS+1
matrix = [[0 for x in range(COLUMNS + 1)] for y in range(ROWS + 1)]
animations_to_update = []

class Block(pygame.sprite.Sprite):

    def __init__(self, posX, posY, neighbors=10):
        # type: (int, int, int) -> Block
        super(Block,self).__init__()
        self.image = pygame.Surface([MINA_SIZE, MINA_SIZE])
        self.image.fill(GRAYLIGHT)
        self.next_image = None
        self.posX=posX
        self.posY=posY
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE * posX + PADDING
        self.rect.y = BLOCK_SIZE * posY + PADDING
        self.neighbors = neighbors
        self.revealed=False
        self.marked = False

    def __repr__(self):
        return str(self.posX) + ' ' + str(self.posY) + ' ' + str(self.neighbors) + ' ' + str(self.revealed)

    def reveal(self, first=False):

        if self.revealed:
            return

        if first:
            animations_to_update.append(self)

        self.revealed = True
        #pygame.time.wait(10)
        all_sprites_list.draw(screen)
        pygame.display.flip()

        if self.neighbors>0:
            # Atualiza numero de bombas no tabuleiro
            self.next_image = pygame.image.load("images/number"+str(self.neighbors)+".png").convert_alpha()
            #self.image = pygame.image.load("images/number"+str(self.neighbors)+".png").convert_alpha()
        else:
            self.next_image = FILL_DARK_GRAY
            #self.image.fill(GRAYDARK)
            # Acorda os vizinhos sem bombas pertos

            bloco = matrix[self.posX + 1][self.posY]
            if type(bloco) is Block and bloco.revealed==False:
                animations_to_update.append(bloco)
                #bloco.reveal()

            bloco = matrix[self.posX][self.posY + 1]
            if type(bloco) is Block and bloco.revealed == False:
                animations_to_update.append(bloco)
                # bloco.reveal()

            bloco = matrix[self.posX - 1][self.posY]
            if type(bloco) is Block and bloco.revealed == False:
                animations_to_update.append(bloco)
                # bloco.reveal()

            bloco = matrix[self.posX][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False:
                animations_to_update.append(bloco)
                # bloco.reveal()

            bloco = matrix[self.posX + 1][self.posY + 1]
            if type(bloco) is Block and bloco.revealed == False:
                animations_to_update.append(bloco)
                # bloco.reveal()

            bloco = matrix[self.posX - 1][self.posY + 1]
            if type(bloco) is Block and bloco.revealed == False:
                animations_to_update.append(bloco)
                # bloco.reveal()

            bloco = matrix[self.posX + 1][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False:
                animations_to_update.append(bloco)
                # bloco.reveal()

            bloco = matrix[self.posX - 1][self.posY - 1]
            if type(bloco) is Block and bloco.revealed == False:
                animations_to_update.append(bloco)
                # bloco.reveal()

    def update_image(self):
        if self.next_image is not None:
            if self.next_image == FILL_DARK_GRAY:
                self.image.fill(GRAYDARK)
            else:
                self.image = self.next_image

        self.next_image = None

    def __str__(self):
        return "bloco"

    def mark(self):
        self.image = pygame.image.load("images/mark1.png").convert_alpha()
        self.marked=True


class Mina(Block):

    def reveal(self, first=False):

        if not self.revealed:
            self.next_image = pygame.image.load("images/mina.png").convert_alpha()

        if first:
            animations_to_update.append(self)

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
                        while len(animations_to_update) > 0:
                            block.update_image()
                            block = animations_to_update.pop(0)
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
                pygame.time.wait(2000)

        # Clear the screen
    screen.fill(GRAYDARK)

    #for block in all_sprites_list: block.reveal()
    all_sprites_list.draw(screen)
    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
