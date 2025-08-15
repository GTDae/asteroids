import pygame
from constants import *
from player import Player


def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    # Create a Player object, spawning it in the center of the screen.
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update the player's state based on input and delta time.
        player.update(dt)

        screen.fill("black")

        # Draw the player on the screen.
        player.draw(screen)
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
