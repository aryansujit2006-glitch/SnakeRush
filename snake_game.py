import pygame
import random

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
GRID = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BG = (170, 215, 81)
GRID_COLOR = (162, 209, 73)
SNAKE = (50, 90, 255)
HEAD = (30, 60, 220)
APPLE = (255, 50, 50)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()
FPS = 10

# Snake
snake = [(200, 200)]
direction = (GRID, 0)

# Food
food = (
    random.randrange(0, WIDTH, GRID),
    random.randrange(0, HEIGHT, GRID)
)

score = 0


def draw_grid():
    for x in range(0, WIDTH, GRID):
        for y in range(0, HEIGHT, GRID):
            rect = pygame.Rect(x, y, GRID, GRID)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def reset_game():
    """Reset and return initial game state."""
    return {
        'snake': [(200, 200)],
        'direction': (GRID, 0),
        'food': (
            random.randrange(0, WIDTH, GRID),
            random.randrange(0, HEIGHT, GRID)
        ),
        'score': 0
    }


def draw_button(rect, text, bg=(50, 150, 50), fg=(255, 255, 255)):
    pygame.draw.rect(screen, bg, rect)
    label = font.render(text, True, fg)
    lx = rect[0] + (rect[2] - label.get_width()) // 2
    ly = rect[1] + (rect[3] - label.get_height()) // 2
    screen.blit(label, (lx, ly))


state = reset_game()

while True:
    # Main gameplay loop
    playing = True
    while playing:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and state['direction'] != (0, GRID):
                    state['direction'] = (0, -GRID)

                elif event.key == pygame.K_DOWN and state['direction'] != (0, -GRID):
                    state['direction'] = (0, GRID)

                elif event.key == pygame.K_LEFT and state['direction'] != (GRID, 0):
                    state['direction'] = (-GRID, 0)

                elif event.key == pygame.K_RIGHT and state['direction'] != (-GRID, 0):
                    state['direction'] = (GRID, 0)

        # Move snake
        head_x, head_y = state['snake'][0]
        new_head = (
            head_x + state['direction'][0],
            head_y + state['direction'][1]
        )

        # Wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            playing = False
            break

        # Self collision
        if new_head in state['snake']:
            playing = False
            break

        state['snake'].insert(0, new_head)

        # Eat food
        if new_head == state['food']:
            state['score'] += 1
            state['food'] = (
                random.randrange(0, WIDTH, GRID),
                random.randrange(0, HEIGHT, GRID)
            )
        else:
            state['snake'].pop()

        # Draw
        screen.fill(BG)
        draw_grid()

        # Apple
        pygame.draw.circle(
            screen,
            APPLE,
            (state['food'][0] + GRID // 2, state['food'][1] + GRID // 2),
            GRID // 2
        )

        # Snake body
        for segment in state['snake'][1:]:
            pygame.draw.rect(
                screen,
                SNAKE,
                (segment[0], segment[1], GRID, GRID)
            )

        # Head
        pygame.draw.rect(
            screen,
            HEAD,
            (state['snake'][0][0], state['snake'][0][1], GRID, GRID)
        )

        # Eyes
        pygame.draw.circle(
            screen,
            WHITE,
            (state['snake'][0][0] + 6, state['snake'][0][1] + 6),
            2
        )
        pygame.draw.circle(
            screen,
            WHITE,
            (state['snake'][0][0] + 14, state['snake'][0][1] + 6),
            2
        )

        # Score
        score_text = font.render(
            "Score: {}".format(state['score']),
            True,
            (0, 0, 0)
        )
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    # Game Over screen with Restart and Quit buttons
    while True:
        screen.fill((0, 0, 0))

        game_over = font.render(
            "Game Over! Score: {}".format(state['score']),
            True,
            (255, 255, 255)
        )
        gx = WIDTH // 2 - game_over.get_width() // 2
        gy = HEIGHT // 2 - 60
        screen.blit(game_over, (gx, gy))

        # Buttons
        btn_w, btn_h = 140, 40
        restart_rect = (WIDTH // 2 - btn_w - 10, HEIGHT // 2, btn_w, btn_h)
        quit_rect = (WIDTH // 2 + 10, HEIGHT // 2, btn_w, btn_h)

        draw_button(restart_rect, "Restart", bg=(70, 130, 180))
        draw_button(quit_rect, "Quit", bg=(180, 70, 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Restart clicked
                rx, ry, rw, rh = restart_rect
                qx, qy, qw, qh = quit_rect
                if rx <= mx <= rx + rw and ry <= my <= ry + rh:
                    state = reset_game()
                    playing = True
                    break
                if qx <= mx <= qx + qw and qy <= my <= qy + qh:
                    pygame.quit()
                    raise SystemExit

        else:
            # continue waiting on game over screen
            clock.tick(FPS)
            continue

        # if we broke from event loop due to restart, break out to main loop
        break