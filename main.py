
import pygame
import random

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GRAYDARK = ( 167, 167, 167)
GRAYLIGHT= ( 205, 205, 205)
BLOCKSIZE= 20 #tamanho do lado de cada block
MATRIXSIZE=25 #tamanho do lado da matrix, se for igual BLOCKSIZE nao da pra ver grade, diferente aparece grade no fundo
COLUMNS  = 10
ROWS     = 10
BOMBS    = 50

class Block(pygame.sprite.Sprite):

    def __init__(self, posX, posY):
        super(Block,self).__init__()
        self.image = pygame.Surface([BLOCKSIZE, BLOCKSIZE])
        self.image.fill(GRAYLIGHT)
        self.posX=posX
        self.posY=posY
        self.rect = self.image.get_rect()
        self.rect.x = MATRIXSIZE * posX
        self.rect.y = MATRIXSIZE * posY
        self.neighbors = 0

    def reveal(self):
        print "matrix[" + str(self.posX+1) + "][" + str(self.posY) + "] = " + str(matrix[self.posX+1][self.posY])
        if   type(matrix[self.posX + 1][self.posY    ]) is Mina:
            self.neighbors += 1
        if type(matrix[self.posX    ][self.posY + 1]) is Mina:
            self.neighbors += 1
        if type(matrix[self.posX - 1][self.posY    ]) is Mina:
            self.neighbors += 1
        if type(matrix[self.posX    ][self.posY - 1] ) is Mina:
            self.neighbors += 1
        if type(matrix[self.posX + 1][self.posY + 1] ) is Mina:
            self.neighbors += 1
        if type(matrix[self.posX - 1][self.posY + 1] ) is Mina:
            self.neighbors += 1
        if type(matrix[self.posX + 1][self.posY - 1] ) is Mina:
            self.neighbors += 1
        if type(matrix[self.posX - 1][self.posY - 1] ) is Mina:
            self.neighbors += 1

        if self.neighbors>0:
            self.image = pygame.image.load("number"+str(self.neighbors)+".png").convert_alpha()
        else:
            self.image.fill(GRAYDARK)

        self.neighbors = 0


    def __str__(self):
        return "bloco"


class Mina(Block):

    def reveal(self):
        self.image=pygame.image.load("mina.png").convert_alpha()

    def __str__(self):
        return "mina"

# Initialize Pygame
pygame.init()

#tamanho da janela depende do numero de columas linhas e do tamanho de cada celula da matrix
screen_width = COLUMNS*MATRIXSIZE
screen_height = ROWS*MATRIXSIZE
screen = pygame.display.set_mode([screen_width, screen_height])

#criando matriz 10 por 10
matrix = [[0 for x in range(COLUMNS+1)] for y in range(ROWS+1)] #+1 para poder verificar do lado
#grupo dos elementos de minas e total
mines = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

#cria bombas
for i in range(BOMBS):

    empty=True
    posX=random.randrange(COLUMNS)
    posY=random.randrange(ROWS)
    print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
    if matrix[posX][posY]==0:
        mina = Mina(posX,posY)
        matrix[posX][posY]=mina
    # Add the block to the list of objects
        mines.add(mina)
        all_sprites_list.add(mina)
        print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

for posX in range(COLUMNS):
    for posY in range(ROWS):
        print "antes matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])
        if matrix[posX][posY] == 0:
            bloco = Block(posX,posY)
            all_sprites_list.add(bloco)
            print "depois matrix[" + str(posX) + "][" + str(posY) + "] = " + str(matrix[posX][posY])

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
            if event.key == K_ESCAPE:
                done=True

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for block in all_sprites_list:
                if block.rect.collidepoint(x, y):
                    block.reveal()

        # Clear the screen
    screen.fill(GRAYDARK)

    #for block in all_sprites_list: block.reveal()
    all_sprites_list.draw(screen)
    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
