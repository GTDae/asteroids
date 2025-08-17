import sys
import pygame
import json
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from gamestates import GameState


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
    scores.append({"score": new_score, "time": new_time})
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
    explosions = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0
    session_time = 0.0
    top_scores = load_scores()

    current_state = GameState.INTRO
    intro_start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                top_scores = add_new_score(top_scores, score, session_time)
                save_scores(top_scores)
                return

        if current_state == GameState.PLAYING:
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

            session_time += dt
            hours = int(session_time // 3600)
            minutes = int((session_time % 3600) // 60)
            seconds = int(session_time % 60)
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
            time_text = top_scores_font.render(f"Time: {time_string}", True, "white")
            screen.blit(time_text, (20, 140))

            header_text = top_scores_font.render("Top Scores:", True, "white")
            screen.blit(header_text, (20, 20))

            for i, top_score in enumerate(top_scores[:3]):
                time_string = f"{int(top_score['time'] // 3600):02}:{int((top_score['time'] % 3600) // 60):02}:{int(top_score['time'] % 60):02}"
                score_line = top_scores_font.render(f"{i + 1}: {top_score['score']} ({time_string})", True, "white")
                screen.blit(score_line, (20, 50 + i * 30))

        elif current_state == GameState.INTRO:
            screen.fill("black")

            time_elapsed = (pygame.time.get_ticks() - intro_start_time) / 1000

            if time_elapsed < 3:
                alpha = min(255, int(255 * (time_elapsed / 1.5)))
                
                gtd_text = score_font.render("GTDaeAvgJoe", True, (255, 255, 255))
                presents_text = top_scores_font.render("Presents...", True, (255, 255, 255))

                gtd_text.set_alpha(alpha)
                presents_text.set_alpha(alpha)

                gtd_rect = gtd_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                presents_rect = presents_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

                screen.blit(gtd_text, gtd_rect)
                screen.blit(presents_text, presents_rect)

            elif time_elapsed >= 3:
                title_text = score_font.render("ASTEROID HUNTER", True, (255, 255, 255))
                title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                space_prompt_text = top_scores_font.render("Hit Space To Continue...", True, (255, 255, 255))
                space_prompt_rect = space_prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

                screen.blit(title_text, title_rect)
                screen.blit(space_prompt_text, space_prompt_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                current_state = GameState.MENU

        elif current_state == GameState.MENU:
            screen.fill("black")

            # Get mouse position and button clicks
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True
            
            # Draw the menu options
            menu_options = [
                ("START GAME", GameState.PLAYING),
                ("HIGH SCORES", GameState.HIGH_SCORES),
                ("README", GameState.README),
                ("CREDITS", GameState.CREDITS),
                ("QUIT", GameState.QUIT),
            ]

            y_offset = SCREEN_HEIGHT // 2 - 100
            new_state = current_state

            for text, state in menu_options:
                option_text = score_font.render(text, True, "white")
                text_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                
                # Check if the mouse is hovering over an option
                if text_rect.collidepoint(mouse_pos):
                    option_text = score_font.render(text, True, "gold") # Highlight the text
                    if mouse_clicked:
                        new_state = state

                screen.blit(option_text, text_rect)
                y_offset += 60 # Spacing between options
            
            # Transition to the new state
            current_state = new_state

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()