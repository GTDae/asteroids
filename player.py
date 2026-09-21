import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0.0

    def draw(self, screen):
        pygame.draw.polygon(screen, SIGNAL_GREEN, self.ship_shape(), 2)

    def ship_shape(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)

        nose = self.position + forward * self.radius
        left_wingtip = self.position - forward * self.radius * 0.6 - right * self.radius * 0.9
        left_notch = self.position - forward * self.radius * 0.2 - right * self.radius * 0.35
        tail = self.position - forward * self.radius * 0.5
        right_notch = self.position - forward * self.radius * 0.2 + right * self.radius * 0.35
        right_wingtip = self.position - forward * self.radius * 0.6 + right * self.radius * 0.9

        return [nose, left_wingtip, left_notch, tail, right_notch, right_wingtip]

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt)
        self.wrap_position()

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
