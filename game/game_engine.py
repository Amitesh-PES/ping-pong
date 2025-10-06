import pygame
from .paddle import Paddle
from .ball import Ball

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class GameEngine:
    def __init__(self, width, height, debug=False, winning_score=5):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)

        self.debug = debug
        self.winning_score = winning_score
        self.game_over = False
        self.winner_text = None
        self.showing_menu = False  # NEW

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over or self.showing_menu:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        self.check_game_over()

    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.winner_text = "PLAYER WINS!"
            self.game_over = True
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI WINS!"
            self.game_over = True

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.debug:
            pygame.draw.rect(screen, RED, self.ball.rect(), 1)
            pygame.draw.rect(screen, GREEN, self.player.rect(), 1)
            pygame.draw.rect(screen, GREEN, self.ai.rect(), 1)

        if self.game_over and self.winner_text:
            text_surface = self.large_font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)

    def show_game_over_screen(self, screen):
        pygame.display.flip()
        pygame.time.delay(1500)
        self.showing_menu = True

    def show_replay_menu(self, screen):
        """Display replay options and return chosen winning score or None if exiting."""
        screen.fill((0, 0, 0))
        title = self.large_font.render("Play Again?", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 150)))

        options = [
            ("3 - Best of 3", 2),
            ("5 - Best of 5", 3),
            ("7 - Best of 7", 4),
            ("ESC - Exit", None),
        ]

        y = 300
        for text, _ in options:
            surf = self.font.render(text, True, WHITE)
            rect = surf.get_rect(center=(self.width // 2, y))
            screen.blit(surf, rect)
            y += 60

        pygame.display.flip()

        # Wait for input
        waiting = True
        new_score = None
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        new_score = 2
                        waiting = False
                    elif event.key == pygame.K_5:
                        new_score = 3
                        waiting = False
                    elif event.key == pygame.K_7:
                        new_score = 4
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        return None
        return new_score

    def reset_game(self, new_winning_score=None):
        """Reset everything for replay."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner_text = None
        self.showing_menu = False
        if new_winning_score:
            self.winning_score = new_winning_score
