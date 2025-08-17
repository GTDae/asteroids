import sys
import pygame
import json
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def load_scores():
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_scores(scores):
    with open("scores.json", "w") as f:
        json.dump(scores, f)

def add_new_score(scores, new_score, new_time):
    scores.append(new_score)
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:10]

def main():
    pygame.init()
    
    score_font = pygame.font.SysFont(None, 48)
    top_scores_font = pygame.font.SysFont(None, 30)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0
    session_time = 0.0
    top_scores = load_scores()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                top_scores = add_new_score(top_scores, score, session_time)
                save_scores(top_scores)
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                top_scores = add_new_score(top_scores, score, session_time)
                save_scores(top_scores)
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    points_earned = asteroid.split()
                    score += points_earned
                    shot.kill()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        score_text = score_font.render(f"Score: {score:04}", True, "white")
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(score_text, score_rect)

        header_text = top_scores_font.render("Top Scores:", True, "white")
        screen.blit(header_text, (20, 20))

        for i, top_score in enumerate(top_scores[:3]):
            time = top_score['time']
            hours = int(time // 3600)
            minutes = int((time % 3600) // 60)
            seconds = int(time % 60)
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}"


            score_line = top_scores_font.render(f"{i + 1}: {top_score['score']}({time_string})", True, "white")
            screen.blit(score_line, (20, 50 + i * 30))

        session_time += dt

        hours = int(session_time // 3600)
        minutes = int((session_time % 3600) // 60)
        seconds = int(session_time % 60)

        time_string = f"{hours:02}:{minutes:02}:{seconds:02}"

        time_text = top_scores_font.render(f"Time: {time_string}", True, "white")
        screen.blit(time_text, (20, 140))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
