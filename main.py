import pygame
from game.game_engine import GameEngine

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT, debug=False)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

        if engine.game_over:
            engine.show_game_over_screen(SCREEN)
            new_target = engine.show_replay_menu(SCREEN)
            if new_target is None:
                running = False
            else:
                engine.reset_game(new_target)

    pygame.quit()

if __name__ == "__main__":
    main()
