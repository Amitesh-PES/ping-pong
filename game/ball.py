import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        # Store previous positon for better collision handling
        prev_x, prev_y = self.x, self.y

        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        """More reliable collision check that prevents tunneling."""
        ball_rect = self.rect()

        # Check collision with player
        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width  # move ball just outside paddle
            self.velocity_x = abs(self.velocity_x)  # ensure ball moves right
            self.add_random_angle()

        # Check collision with AI
        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width  # move ball just outside paddle
            self.velocity_x = -abs(self.velocity_x)  # ensure ball moves left
            self.add_random_angle()

    def add_random_angle(self):
        """Add a small random Y velocity to make gameplay less predictable."""
        self.velocity_y += random.choice([-1, 0, 1])
        # Limit Y speed so it doesn't get too fast
        self.velocity_y = max(-5, min(self.velocity_y, 5))

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)