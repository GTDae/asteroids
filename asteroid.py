import pygame
import random
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = int(self.radius / ASTEROID_MIN_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        score_to_add = self.points
        self.kill()

        Explosion(self.position.x, self.position.y, self.radius)

        if self.radius > ASTEROID_MIN_RADIUS:
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            random_angle = random.uniform(20, 50)
            velocity_one = self.velocity.rotate(random_angle)
            velocity_two = self.velocity.rotate(-random_angle)

            asteroid_one = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid_one.velocity = velocity_one * 1.2

            asteroid_two = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid_two.velocity = velocity_two * 1.2
        
        return score_to_add