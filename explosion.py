import pygame
import random
from circleshape import CircleShape
from constants import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__(self.containers)
            
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.lifetime = 0.0
        self.particles = []

        num_particles = random.randint(5, EXPLOSION_MAX_PARTICLES)
        for _ in range(num_particles):
            particle_size = random.choice([
                EXPLOSION_PARTICLE_MAX_RADIUS, 
                EXPLOSION_PARTICLE_MEDIUM_RADIUS, 
                EXPLOSION_PARTICLE_MIN_RADIUS
            ])
            
            particle = CircleShape(self.position.x, self.position.y, particle_size)
            
            random_angle = random.uniform(0, 360)
            particle.velocity = pygame.Vector2(1, 0).rotate(random_angle) * EXPLOSION_SPEED_SCALE
            
            self.particles.append(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        
        self.lifetime += dt
        
        if self.lifetime >= EXPLOSION_DURATION:
            self.kill()