
import pygame
import random

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GRAYDARK = ( 167, 167, 167)
GRAYLIGHT= ( 205, 205, 205)

class Mina(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, img,posX, posY):

        super(Mina,self).__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 20 * posX
        self.rect.y = 20 * posY
class Block(pygame.sprite.Sprite):

    def __init__(self, color, posX, posY):
        super(Block,self).__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 20 * posX
        self.rect.y = 20 * posY

    def update(self):
        """ Called each frame. """

        # Move block down one pixel
        self.rect.y += 1

        # If block is too far down, reset to top of screen.
        if self.rect.y > 400:
            self.reset_pos()


class Player(Block):
    """ The player class derives from Block, but overrides the 'update'
    functionality with new a movement function that will move the block
    with the mouse. """
    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Fetch the x and y out of the list,
        # just like we'd fetch letters out of a string.
        # Set the player object to the mouse location
        self.rect.x = pos[0]
        self.rect.y = pos[1]

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 200
screen_height = 200
screen = pygame.display.set_mode([screen_width, screen_height])

#criando matriz 10 por 10
matrix = [[0 for x in range(10)] for y in range(10)]
#gupo dos elementos no campo
field = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    # This represents a block
    posX=random.randrange(10)
    posY=random.randrange(10)
    mina = Mina("mina.png",posX,posY)
    # Add the block to the list of objects
    field.add(mina)
    all_sprites_list.add(mina)



# Create a red player block
player = Player(RED, 20, 20)
all_sprites_list.add(player)

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
            for block in field:
                if block.rect.collidepoint(x, y):
                    score += 1
                    print score

        # Clear the screen
    screen.fill(GRAYDARK)

    # Draw all the spites
    field.draw(screen)

    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
