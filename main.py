import pygame
import random
from constants import *

MINA_SIZE   = 20 # tamanho de uma mina
BLOCK_SIZE  = 24 # tamanho de um bloco que contem uma mina
COLUMNS     = 10
ROWS        = 10
BOMBS       = 10

PADDING = (BLOCK_SIZE - MINA_SIZE) # espaco entre tabuleiro e minas

#criando matriz ROWS+1 por COLUMNS+1
matrix = [[0 for x in range(COLUMNS)] for y in range(ROWS)] #+1 para poder verificar do lado

class Block(pygame.sprite.Sprite):

    def __init__(self, posX, posY, neighbors=10):
        # type: (int, int, int) -> Block
        super(Block,self).__init__()
        self.image = pygame.Surface([MINA_SIZE, MINA_SIZE])
        self.image.fill(GRAYLIGHT)
        self.posX=posX
        self.posY=posY
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE * posX + PADDING
        self.rect.y = BLOCK_SIZE * posY + PADDING
        self.neighbors = neighbors
        self.revealed=False

    @staticmethod
    def check_interval(a,b):
        if 0 <= a < ROWS and 0 <= b < COLUMNS:
            return True
        else:
            return False

    def reveal(self):

        if self.neighbors>0:
            self.image = pygame.image.load("images/number"+str(self.neighbors)+".png").convert_alpha()
        else:
            self.image.fill(GRAYDARK)
            self.revealed = True
            #pygame.time.wait(50)
            #acorda os vizinhos sem bombas pertos

            bloco = matrix[self.posX + 1][self.posY] \
                if self.check_interval(self.posX + 1,self.posY) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed==False:
                bloco.reveal()

            bloco = matrix[self.posX][self.posY + 1] \
                if self.check_interval(self.posX,self.posY + 1) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed == False:
                bloco.reveal()

            bloco = matrix[self.posX - 1][self.posY] \
                if self.check_interval(self.posX - 1,self.posY) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed == False:
                bloco.reveal()

            bloco = matrix[self.posX][self.posY - 1] \
                if self.check_interval(self.posX,self.posY - 1) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed == False:
                bloco.reveal()

            bloco = matrix[self.posX + 1][self.posY + 1] \
                if self.check_interval(self.posX + 1,self.posY + 1) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed == False:
                bloco.reveal()

            bloco = matrix[self.posX - 1][self.posY + 1] \
                if self.check_interval(self.posX - 1,self.posY + 1) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed == False:
                bloco.reveal()

            bloco = matrix[self.posX + 1][self.posY - 1] \
                if self.check_interval(self.posX + 1,self.posY - 1) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed == False:
                bloco.reveal()

            bloco = matrix[self.posX - 1][self.posY - 1] \
                if self.check_interval(self.posX - 1,self.posY -1) else None
            if type(bloco) is Block and bloco.neighbors == 0 and bloco.revealed == False:
                bloco.reveal()

    def __str__(self):
        return "bloco"

    def mark(self):
        self.image = pygame.image.load("images/mark1.png").convert_alpha()


class Mina(Block):

    def reveal(self):
        self.image=pygame.image.load("images/mina.png").convert_alpha()

    def __str__(self):
        return "mina"

# Initialize Pygame
pygame.init()

#tamanho da janela depende do numero de columas linhas e do tamanho de cada celula da matrix
screen_width = COLUMNS * BLOCK_SIZE + PADDING
screen_height = ROWS * BLOCK_SIZE + PADDING
screen = pygame.display.set_mode([screen_width, screen_height])

#grupo dos elementos de minas e total
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
        all_sprites_list.add(mina)
        i+=1
       # print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

for posX in range(COLUMNS):
    for posY in range(ROWS):
        #print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
        if matrix[posX][posY] == 0:
            neighbors = 0
            if Block.check_interval(posX + 1,posY) and type(matrix[posX + 1][posY]) is Mina:
                neighbors += 1
            if Block.check_interval(posX,posY + 1) and type(matrix[posX][posY + 1]) is Mina:
                neighbors += 1
            if Block.check_interval(posX - 1,posY) and type(matrix[posX - 1][posY]) is Mina:
                neighbors += 1
            if Block.check_interval(posX,posY - 1) and type(matrix[posX][posY - 1]) is Mina:
                neighbors += 1
            if Block.check_interval(posX + 1,posY + 1) and type(matrix[posX + 1][posY + 1]) is Mina:
                neighbors += 1
            if Block.check_interval(posX - 1,posY + 1) and type(matrix[posX - 1][posY + 1]) is Mina:
                neighbors += 1
            if Block.check_interval(posX + 1,posY - 1) and type(matrix[posX + 1][posY - 1]) is Mina:
                neighbors += 1
            if Block.check_interval(posX - 1,posY - 1) and type(matrix[posX - 1][posY - 1]) is Mina:
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
            button1, button2, button3=pygame.mouse.get_pressed()
            x, y = event.pos
            if button1:
                # usa colisao:
                # vantagem -> ignora se clicar entre dois quadrados
                for block in all_sprites_list:
                    if block.rect.collidepoint(x, y):
                        block.reveal()
            elif button3:
                block = matrix[x / BLOCK_SIZE][y / BLOCK_SIZE]
                #print "matrix[" + str(x / MATRIXSIZE) + "][" + str(y / MATRIXSIZE) + "] = " + str(matrix[x / MATRIXSIZE][y / MATRIXSIZE])
                block.mark()


        # Clear the screen
    screen.fill(GRAYDARK)

    #for block in all_sprites_list: block.reveal()
    all_sprites_list.draw(screen)
    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
