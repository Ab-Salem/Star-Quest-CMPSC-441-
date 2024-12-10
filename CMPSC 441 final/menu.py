import pygame
from constants import WIDTH, HEIGHT, BLACK, WHITE


def draw_text(surface, text, font, color, x, y):
    """Draw text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)


def algorithm_menu(screen):
    """Display a menu to select the enemy algorithm."""
    font = pygame.font.Font(None, 50)
    running = True

    while running:
        screen.fill(BLACK)

        draw_text(screen, "Select Enemy Algorithm", font, WHITE, WIDTH // 2, HEIGHT // 5)

        # Algorithm options
        draw_text(screen, "1. A* Algorithm", font, WHITE, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text(screen, "2. BFS Algorithm", font, WHITE, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text(screen, "3. DFS Algorithm", font, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
        draw_text(screen, "4. Greedy Algorithm", font, WHITE, WIDTH // 2, HEIGHT // 2 + 60)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "a_star_search"
                elif event.key == pygame.K_2:
                    return "bfs"
                elif event.key == pygame.K_3:
                    return "dfs"
                elif event.key == pygame.K_4:
                    return "greedy"


def difficulty_menu(screen):
    """Display a menu to select the difficulty level."""
    font = pygame.font.Font(None, 50)
    running = True

    while running:
        screen.fill(BLACK)

        # Title text
        draw_text(screen, "Select Difficulty", font, WHITE, WIDTH // 2, HEIGHT // 5)

        # Difficulty options
        draw_text(screen, "1. Easy", font, WHITE, WIDTH // 3, HEIGHT // 2 - 40)
        draw_text(screen, "2. Medium", font, WHITE, WIDTH // 3, HEIGHT // 2)
        draw_text(screen, "3. Hard", font, WHITE, WIDTH // 3, HEIGHT // 2 + 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"


def show_end_screen(screen, message):
    """Display a message when the game ends and wait for restart or quit."""
    font = pygame.font.Font(None, 75)
    small_font = pygame.font.Font(None, 30)
    running = True

    while running:
        screen.fill(BLACK)
        text = font.render(message, True, WHITE)
        restart_text = small_font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(text, (WIDTH // 4, HEIGHT // 3))
        screen.blit(restart_text, (WIDTH // 5, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    return True
                if event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    exit()
