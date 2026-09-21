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
        with open("score.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_scores(scores):
    with open("score.json", "w") as f:
        json.dump(scores, f)


def add_new_score(scores, new_score, new_time):
    new_entry = {"score": new_score, "time": new_time}
    updated = scores + [new_entry]
    updated.sort(key=lambda x: x['score'], reverse=True)
    updated = updated[:10]
    made_high_score = new_entry in updated
    return updated, made_high_score


def draw_lives(screen, lives, max_lives, x, y):
    icon_size = 12
    spacing = 32
    for i in range(max_lives):
        cx = x + i * spacing
        points = [
            (cx, y - icon_size),
            (cx - icon_size * 0.7, y + icon_size * 0.6),
            (cx, y + icon_size * 0.2),
            (cx + icon_size * 0.7, y + icon_size * 0.6),
        ]
        if i < lives:
            pygame.draw.polygon(screen, SIGNAL_GREEN, points, 2)
        else:
            pygame.draw.polygon(screen, PANEL, points, 2)
            pygame.draw.line(screen, FLARE_AMBER, (cx - icon_size, y - icon_size), (cx + icon_size, y + icon_size), 2)
            pygame.draw.line(screen, FLARE_AMBER, (cx - icon_size, y + icon_size), (cx + icon_size, y - icon_size), 2)


def main():
    pygame.init()

    score_font = pygame.font.Font(FONT_HEADING_BOLD, 48)
    top_scores_font = pygame.font.Font(FONT_BODY_REGULAR, 30)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    avatar_image = pygame.image.load(AVATAR_IMAGE).convert_alpha()
    avatar_image = pygame.transform.smoothscale(avatar_image, (160, 160))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0
    session_time = 0.0
    lives = PLAYER_MAX_LIVES
    top_scores = load_scores()
    post_game_message = None

    current_state = GameState.INTRO
    intro_start_time = pygame.time.get_ticks()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                top_scores, _ = add_new_score(top_scores, score, session_time)
                save_scores(top_scores)
                return

        if current_state == GameState.PLAYING:
            updatable.update(dt)

            if player.invulnerable_timer <= 0:
                for asteroid in asteroids:
                    if player.collides_with(asteroid):
                        lives -= 1
                        if lives > 0:
                            player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        else:
                            top_scores, made_high_score = add_new_score(top_scores, score, session_time)
                            save_scores(top_scores)
                            if made_high_score:
                                post_game_message = f"New high score! You scored {score} points."
                            else:
                                post_game_message = f"Game over! You scored {score} points."
                            current_state = GameState.HIGH_SCORES
                        break

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        points_earned = asteroid.split()
                        score += points_earned
                        shot.kill()

            screen.fill(INK_BLACK)

            for obj in drawable:
                obj.draw(screen)

            score_text = score_font.render(f"Score: {score:04}", True, SIGNAL_GREEN)
            score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
            screen.blit(score_text, score_rect)

            session_time += dt
            hours = int(session_time // 3600)
            minutes = int((session_time % 3600) // 60)
            seconds = int(session_time % 60)
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
            time_text = top_scores_font.render(f"Time: {time_string}", True, SIGNAL_GREEN)
            screen.blit(time_text, (20, 140))

            lives_label = top_scores_font.render("Lives:", True, SIGNAL_GREEN)
            screen.blit(lives_label, (20, 175))
            draw_lives(screen, lives, PLAYER_MAX_LIVES, 105, 190)

            header_text = top_scores_font.render("Top Scores:", True, SIGNAL_GREEN)
            screen.blit(header_text, (20, 20))

            for i, top_score in enumerate(top_scores[:3]):
                time_string = f"{int(top_score['time'] // 3600):02}:{int((top_score['time'] % 3600) // 60):02}:{int(top_score['time'] % 60):02}"
                score_line = top_scores_font.render(f"{i + 1}: {top_score['score']} ({time_string})", True, SIGNAL_GREEN)
                screen.blit(score_line, (20, 50 + i * 30))

        elif current_state == GameState.INTRO:
            screen.fill(INK_BLACK)

            time_elapsed = (pygame.time.get_ticks() - intro_start_time) / 1000

            if time_elapsed < 3:
                alpha = min(255, int(255 * (time_elapsed / 1.5)))

                avatar_frame = avatar_image.copy()
                avatar_frame.set_alpha(alpha)
                avatar_rect = avatar_frame.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130))
                screen.blit(avatar_frame, avatar_rect)

                gtd_text = score_font.render("GTDaeAvgJoe", True, SIGNAL_GREEN)
                presents_text = top_scores_font.render("Presents...", True, SIGNAL_GREEN)

                gtd_text.set_alpha(alpha)
                presents_text.set_alpha(alpha)

                gtd_rect = gtd_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
                presents_rect = presents_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

                screen.blit(gtd_text, gtd_rect)
                screen.blit(presents_text, presents_rect)

            elif time_elapsed >= 3:
                title_text = score_font.render("ASTEROID HUNTER", True, SIGNAL_GREEN)
                title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                space_prompt_text = top_scores_font.render("Hit Space To Continue...", True, SIGNAL_GREEN)
                space_prompt_rect = space_prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

                screen.blit(title_text, title_rect)
                screen.blit(space_prompt_text, space_prompt_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                current_state = GameState.MENU

        elif current_state == GameState.MENU:
            screen.fill(INK_BLACK)

            # Get mouse position and button clicks
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            for event in events:
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
                option_text = score_font.render(text, True, SIGNAL_GREEN)
                text_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))

                # Check if the mouse is hovering over an option
                if text_rect.collidepoint(mouse_pos):
                    option_text = score_font.render(text, True, FLARE_AMBER)  # Highlight the text
                    if mouse_clicked:
                        new_state = state

                screen.blit(option_text, text_rect)
                y_offset += 60  # Spacing between options

            # Starting a fresh game - reset the world so a previous run doesn't carry over
            if new_state == GameState.PLAYING:
                updatable.empty()
                drawable.empty()
                asteroids.empty()
                shots.empty()
                explosions.empty()
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                asteroid_field = AsteroidField()
                score = 0
                session_time = 0.0
                lives = PLAYER_MAX_LIVES
                post_game_message = None

            # Transition to the new state
            current_state = new_state

        elif current_state == GameState.HIGH_SCORES:
            screen.fill(INK_BLACK)

            title_text = score_font.render("HIGH SCORES", True, SIGNAL_GREEN)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(title_text, title_rect)

            if post_game_message:
                message_color = FLARE_AMBER if "New high score" in post_game_message else SIGNAL_GREEN
                message_text = top_scores_font.render(post_game_message, True, message_color)
                message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
                screen.blit(message_text, message_rect)

            if top_scores:
                for i, top_score in enumerate(top_scores[:10]):
                    time_string = f"{int(top_score['time'] // 3600):02}:{int((top_score['time'] % 3600) // 60):02}:{int(top_score['time'] % 60):02}"
                    line_text = top_scores_font.render(
                        f"{i + 1}: {top_score['score']} ({time_string})", True, SIGNAL_GREEN
                    )
                    line_rect = line_text.get_rect(center=(SCREEN_WIDTH // 2, 180 + i * 35))
                    screen.blit(line_text, line_rect)
            else:
                empty_text = top_scores_font.render("No scores yet", True, SIGNAL_GREEN)
                empty_rect = empty_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
                screen.blit(empty_text, empty_rect)

            back_text = top_scores_font.render("Press ESC to return to menu", True, SIGNAL_GREEN)
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            screen.blit(back_text, back_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                current_state = GameState.MENU

        elif current_state == GameState.README:
            screen.fill(INK_BLACK)

            title_text = score_font.render("README", True, SIGNAL_GREEN)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(title_text, title_rect)

            readme_lines = [
                "Survive as long as possible by navigating a spaceship",
                "through an asteroid field and shooting down incoming threats.",
                "",
                "Large asteroids split into two medium ones, medium ones",
                "split into two small ones. Small asteroids are destroyed on impact.",
                "",
                "Controls: W forward, S backward, A/D turn, Spacebar to fire.",
            ]
            for i, line in enumerate(readme_lines):
                line_text = top_scores_font.render(line, True, SIGNAL_GREEN)
                line_rect = line_text.get_rect(center=(SCREEN_WIDTH // 2, 160 + i * 35))
                screen.blit(line_text, line_rect)

            back_text = top_scores_font.render("Press ESC to return to menu", True, SIGNAL_GREEN)
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            screen.blit(back_text, back_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                current_state = GameState.MENU

        elif current_state == GameState.CREDITS:
            screen.fill(INK_BLACK)

            title_text = score_font.render("CREDITS", True, SIGNAL_GREEN)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(title_text, title_rect)

            credit_lines = [
                "Asteroid Hunter",
                "Guided project via Boot.dev",
                "Extended and maintained by GTDae",
                "Built with Python and Pygame",
            ]
            for i, line in enumerate(credit_lines):
                line_text = top_scores_font.render(line, True, SIGNAL_GREEN)
                line_rect = line_text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 40))
                screen.blit(line_text, line_rect)

            back_text = top_scores_font.render("Press ESC to return to menu", True, SIGNAL_GREEN)
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            screen.blit(back_text, back_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                current_state = GameState.MENU

        elif current_state == GameState.QUIT:
            top_scores, _ = add_new_score(top_scores, score, session_time)
            save_scores(top_scores)
            return

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
