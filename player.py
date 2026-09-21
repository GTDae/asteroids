import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


def _point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def _distance_point_to_segment(point, a, b):
    ap = point - a
    ab = b - a
    ab_len_sq = ab.length_squared()
    if ab_len_sq == 0:
        return ap.length()
    t = max(0, min(1, ap.dot(ab) / ab_len_sq))
    closest = a + ab * t
    return point.distance_to(closest)


def _circle_intersects_polygon(circle_center, circle_radius, polygon):
    if _point_in_polygon(circle_center, polygon):
        return True
    n = len(polygon)
    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]
        if _distance_point_to_segment(circle_center, a, b) <= circle_radius:
            return True
    return False


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0.0
        self.invulnerable_timer = 0.0

    def draw(self, screen):
        # Blink while invulnerable (5 times/second) instead of drawing solid
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        pygame.draw.polygon(screen, SIGNAL_GREEN, self.ship_shape(), 2)

    def collides_with(self, other):
        # Ship's hitbox matches its actual drawn silhouette rather than a circle
        return _circle_intersects_polygon(other.position, other.radius, self.ship_shape())

    def respawn(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.invulnerable_timer = PLAYER_RESPAWN_INVULNERABILITY

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
        self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)
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
