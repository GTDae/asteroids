import pygame

# Base class for game objects that are treated as circles for collision detection.
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # The __init__ method for this class takes a position (x, y) and a radius.
        
        # This checks if the class has a 'containers' attribute, which is a Pygame Group.
        # It's used to automatically add the new sprite to a group when it's created.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            # If no containers are specified, we call the parent class's constructor with no arguments.
            super().__init__()

        # Create a 2D vector for the position and velocity of the object.
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # This method is meant to be overridden by subclasses.
        # It handles drawing the shape to the screen.
        pass

    def update(self, dt):
        # This method is also meant to be overridden by subclasses.
        # It handles the game logic, such as updating position based on velocity.
        pass

