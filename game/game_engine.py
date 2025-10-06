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

        # Debug mode toggle
        self.debug = debug
        self.winning_score = winning_score
        self.game_over = False
        self.winner_text = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Skip updates if game is over
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI paddle tracking
        self.ai.auto_track(self.ball, self.height)

        # Check for game over
        self.check_game_over()

    def check_game_over(self):
        """Check if either player reached the winning score."""
        if self.player_score >= self.winning_score:
            self.winner_text = "PLAYER WINS!"
            self.game_over = True
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI WINS!"
            self.game_over = True

    def render(self, screen):
        # Clear screen and draw objects
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        # Debug outlines
        if self.debug:
            pygame.draw.rect(screen, RED, self.ball.rect(), 1)
            pygame.draw.rect(screen, GREEN, self.player.rect(), 1)
            pygame.draw.rect(screen, GREEN, self.ai.rect(), 1)

        # Game Over screen
        if self.game_over and self.winner_text:
            text_surface = self.large_font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)

    def show_game_over_screen(self, screen):
        """Display Game Over for 3 seconds before quitting."""
        pygame.display.flip()
        pygame.time.delay(3000)
