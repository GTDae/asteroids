import pygame  # Import the main Pygame library to use its functions.
from constants import * # Import all constants (like SCREEN_WIDTH) from constants.py.


def main():
    """
    This is the main function where the game loop runs.
    """
    # Initialize all imported Pygame modules. This is required before any Pygame functions can be used.
    pygame.init()
    
    # Create the game window (or "screen") using the dimensions from constants.py.
    # This returns a Surface object that we can draw on.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # The main game loop. 'while True' makes it run indefinitely until the user quits.
    while True:
        # Event handling loop. This checks for any events from the user (like key presses, mouse clicks, or closing the window).
        for event in pygame.event.get():
            # Check if the event type is pygame.QUIT. This happens when the user clicks the 'X' button on the window.
            if event.type == pygame.QUIT:
                # If the quit event is detected, 'return' exits the main() function, ending the program.
                return

        # Draw the game world. First, fill the entire screen with a solid black color.
        # This is done at the beginning of each frame to clear the previous frame's drawings.
        screen.fill("black")
        
        # Update the full display Surface to the screen. This makes everything we've drawn visible to the user.
        # This should always be the last drawing call in the game loop.
        pygame.display.flip()


# This is a standard Python entry point. It ensures that the main() function is called only when the script is run directly.
if __name__ == "__main__":
    main()
