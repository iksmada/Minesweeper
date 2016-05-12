
import pygame
import random

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GRAYDARK = ( 167, 167, 167)
GRAYLIGHT= ( 205, 205, 205)
BLOCKSIZE= 20 #tamanho do lado de cada block
MATRIXSIZE=21 #tamanho do lado da matrix, se for igual BLOCKSIZE nao da pra ver grade, diferente aparece grade no fundo
COLUMNS  = 10
ROWS     = 10
BOMBS    = 10

class Block(pygame.sprite.Sprite):

    def __init__(self, posX, posY):
        super(Block,self).__init__()
        self.image = pygame.Surface([BLOCKSIZE, BLOCKSIZE])
        self.image.fill(GRAYLIGHT)
        self.rect = self.image.get_rect()
        self.rect.x = MATRIXSIZE * posX
        self.rect.y = MATRIXSIZE * posY
        self.neighbors = 0
        self.changed=False
    def reveal(self):
        if not self.changed:
            for block in mines:
                if block.rect.collidepoint((self.rect.x + MATRIXSIZE, self.rect.y)):
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x + MATRIXSIZE, self.rect.y):  # tem alguem a direita
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x - MATRIXSIZE, self.rect.y):  # esqueda
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x, self.rect.y + MATRIXSIZE):  # baixo
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x, self.rect.y - MATRIXSIZE):  # cima
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x + MATRIXSIZE, self.rect.y - MATRIXSIZE):  # direta superior
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x - MATRIXSIZE, self.rect.y - MATRIXSIZE):  # esquerda superior
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x - MATRIXSIZE, self.rect.y + MATRIXSIZE):  # esquerda inferior
                    self.neighbors += 1
                elif block.rect.collidepoint(self.rect.x + MATRIXSIZE, self.rect.y + MATRIXSIZE):  # direita inferior
                    self.neighbors += 1
            if self.neighbors>0:
                self.image = pygame.image.load("number"+str(self.neighbors)+".png").convert_alpha()
            else:
                self.image.fill(GRAYDARK)
            self.changed=True


class Mina(Block):

    def reveal(self):
        self.image=pygame.image.load("mina.png").convert_alpha()

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = COLUMNS*MATRIXSIZE
screen_height = ROWS*MATRIXSIZE
screen = pygame.display.set_mode([screen_width, screen_height])

#criando matriz 10 por 10
matrix = [[0 for x in range(10)] for y in range(10)]
#gupo dos elementos no campo
mines = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(BOMBS):
    # This represents a block
    empty=True
    posX=random.randrange(COLUMNS)
    posY=random.randrange(ROWS)
    for block in all_sprites_list:
        if block.rect.collidepoint(posX*MATRIXSIZE, posY*MATRIXSIZE):
            empty=False
    if empty:
        mina = Mina(posX,posY)
    # Add the block to the list of objects
        mines.add(mina)
        all_sprites_list.add(mina)

for posX in range(COLUMNS):
    for posY in range(ROWS):
        empty=True
        for block in all_sprites_list:
            if block.rect.collidepoint(posX * MATRIXSIZE, posY * MATRIXSIZE):
                empty = False
        if empty:
            bloco = Block(posX,posY)
            all_sprites_list.add(bloco)



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

    for block in all_sprites_list: block.reveal()
    all_sprites_list.draw(screen)
    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
