"""

Lab_14 completed by VladimirDaGreat
Started: 19/05/2018
Finished: 00/00/0000/

A game demonstrating the game class and using sprites. Task was to modify
chapter 13's example.

"""
 
import pygame
import random
 
# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
 
# --- Classes ---
 
 
class Block(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
 
    def __init__(self):
        """ Constructor, create the image of the block. """
        super().__init__()
        
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
 
        """ position of block. """
        self.rect.y = 0
        self.rect.x = 0
  
class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
 
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
        
        # Set height, width
        self.player_x = 20
        self.player_y = 20
        
        self.image = pygame.Surface([self.player_x, self.player_y])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
 
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.x >= (SCREEN_WIDTH + 2) - self.player_x:
            self.rect.x -= 10
        if self.rect.x <= 0:
            self. rect.x += 10
        if self.rect.y >= 0:
            self.rect.y -= 10
        if self.rect.y <= (SCREEN_HEIGHT + 2) - self.player_y:
            self.rect.y  += 10
        
        
class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
 
        self.score = 0
        self.game_over = False
 
        # Create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.good_blocks_list = pygame.sprite.Group()
        self.bad_blocks_list = pygame.sprite.Group()
 
        # Create the good block sprites
        for i in range(50):
            block = Block()
            block.image.fill(GREEN)
 
            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(SCREEN_HEIGHT)
 
            self.good_blocks_list.add(block)
            self.all_sprites_list.add(block)

        # Create the bad block sprites
        for i in range(50):
            block = Block()
            block.image.fill(RED)
 
            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(SCREEN_HEIGHT)
 
            self.bad_blocks_list.add(block)
            self.all_sprites_list.add(block)   
 
        # Create the player
        self.player = Player(5, 5)
        self.all_sprites_list.add(self.player)
 
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

            # Set the speed based on the key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.changespeed(-3, 0)
                elif event.key == pygame.K_RIGHT:
                    self.player.changespeed(3, 0)
                elif event.key == pygame.K_UP:
                   self. player.changespeed(0, -3)
                elif event.key == pygame.K_DOWN:
                    self.player.changespeed(0, 3)
     
            # Reset speed when key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.changespeed(3, 0)
                elif event.key == pygame.K_RIGHT:
                    self.player.changespeed(-3, 0)
                elif event.key == pygame.K_UP:
                    self.player.changespeed(0, 3)
                elif event.key == pygame.K_DOWN:
                    self.player.changespeed(0, -3)
               
        return False
 
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()
 
            # See if the player block has collided with good blocks.
            blocks_hit_good_list = pygame.sprite.spritecollide(self.player, self.good_blocks_list, True)
 
            # Check the list of collisions.
            for block in blocks_hit_good_list:
                self.score += 1
                print(self.score)
                # You can do something with "block" here.

            # See if the player block has collided with bad blocks.
            blocks_hit_bad_list = pygame.sprite.spritecollide(self.player, self.bad_blocks_list, True)
 
            # Check the list of collisions.
            for block in blocks_hit_bad_list:
                self.score -= 1
                print(self.score)
                # You can do something with "block" here.    
 
            if len(self.good_blocks_list) == 0:
                self.game_over = True

            print(self.good_blocks_list)   
 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)
 
        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
 
        if not self.game_over:
            self.all_sprites_list.draw(screen)

            font_2 = pygame.font.SysFont("serif", 25)
            text_2 = font_2.render("SCORE: " + str(self.score), True, BLACK)
            center_x_2 = (SCREEN_WIDTH // 2) - (text_2.get_width() // 2)
            center_y_2 = (SCREEN_HEIGHT // 2) - (text_2.get_height() // 2)
            screen.blit(text_2, [center_x_2, center_y_2])
 
        pygame.display.flip()
 
 
def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)
 
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    game = Game()
 
    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
 
        # Update object positions, check for collisions
        game.run_logic()
 
        # Draw the current frame
        game.display_frame(screen)
 
        # Pause for the next frame
        clock.tick(60)
 
    # Close window and exit
    pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()
