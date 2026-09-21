import pygame
import random
from circleshape import CircleShape
from explosion import Explosion
from constants import *

ASTEROID_LUMP_POINTS = 10
ASTEROID_LUMP_VARIANCE = 0.25  # each point sits +/- 25% off the base radius


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = int(self.radius / ASTEROID_MIN_RADIUS)
        self.shape_offsets = self._generate_lumpy_shape()

    def _generate_lumpy_shape(self):
        # Precomputed once so the asteroid keeps a consistent lumpy silhouette
        # as it moves, instead of a new random shape every frame.
        offsets = []
        angle_step = 360 / ASTEROID_LUMP_POINTS
        for i in range(ASTEROID_LUMP_POINTS):
            angle = i * angle_step + random.uniform(-angle_step * 0.3, angle_step * 0.3)
            lump_radius = self.radius * random.uniform(
                1 - ASTEROID_LUMP_VARIANCE, 1 + ASTEROID_LUMP_VARIANCE
            )
            offsets.append(pygame.Vector2(lump_radius, 0).rotate(angle))
        return offsets

    def draw(self, screen):
        points = [self.position + offset for offset in self.shape_offsets]
        pygame.draw.polygon(screen, FLARE_AMBER, points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position(margin=ASTEROID_MAX_RADIUS)

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