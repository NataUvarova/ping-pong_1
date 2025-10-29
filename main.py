import pygame
import sys

# --- Ініціалізація ---
pygame.init()
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG 2025 by ChatGPT")

# --- Музика ---
try:
    pygame.mixer.music.load("music.mp3")   # твій файл з музикою
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # -1 = грає постійно
except:
    print("⚠️ Музику не знайдено. Поклади файл music.mp3 поруч із кодом.")

# --- Кольори ---
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GRAY = (60, 60, 60)
BLUE = (0, 200, 255)

# --- Шрифти ---
font = pygame.font.SysFont("Consolas", 40)
big_font = pygame.font.SysFont("Consolas", 80)

# --- Параметри гри ---
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 120
BALL_SIZE = 20

WIN_SCORE = 10

# --- Об’єкти ---
paddle_left = pygame.Rect(40, HEIGHT // 2 - 60, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(WIDTH - 55, HEIGHT // 2 - 60, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_speed_x = 7
ball_speed_y = 7
paddle_speed = 9

score_left = 0
score_right = 0
paused = False
game_started = False

clock = pygame.time.Clock()

# --- Малювання тексту ---
def draw_text(text, size, color, x, y, center=True):
    fnt = pygame.font.SysFont("Consolas", size, True)
    surf = fnt.render(text, True, color)
    rect = surf.get_rect(center=(x, y)) if center else (x, y)
    WIN.blit(surf, rect)

# --- Початковий екран ---
def start_screen():
    WIN.fill(BLACK)
    draw_text("PONG 2025", 80, BLUE, WIDTH // 2, HEIGHT // 2 - 80)
    draw_text("Натисни ENTER щоб почати", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    draw_text("W / S — Ліва ракетка   ↑ / ↓ — Права", 25, GRAY, WIDTH // 2, HEIGHT - 80)
    pygame.display.flip()

# --- Малювання сцени ---
def draw():
    WIN.fill(BLACK)
    pygame.draw.aaline(WIN, GRAY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    pygame.draw.ellipse(WIN, BLUE, ball)
    pygame.draw.rect(WIN, WHITE, paddle_left)
    pygame.draw.rect(WIN, WHITE, paddle_right)
    draw_text(str(score_left), 60, WHITE, WIDTH // 4, 50)
    draw_text(str(score_right), 60, WHITE, WIDTH * 3 // 4, 50)
    if paused:
        draw_text("ПАУЗА", 60, GRAY, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()

def victory_screen(winner):
    WIN.fill(BLACK)
    draw_text(f"Переміг {winner} гравець!", 60, BLUE, WIDTH // 2, HEIGHT // 2 - 60)
    draw_text("Натисни ENTER, щоб почати заново", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 40)
    pygame.display.flip()

# --- Основний цикл ---
running = True
while running:
    if not game_started:
        start_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_RETURN:
                game_started = True
            elif event.key == pygame.K_ESCAPE:
                paused = not paused

    if not game_started or paused:
        continue

    keys = pygame.key.get_pressed()
    # Ліва ракетка
    if keys[pygame.K_w] and paddle_left.top > 0:
        paddle_left.y -= paddle_speed
    if keys[pygame.K_s] and paddle_left.bottom < HEIGHT:
        paddle_left.y += paddle_speed
    # Права ракетка
    if keys[pygame.K_UP] and paddle_right.top > 0:
        paddle_right.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_right.bottom < HEIGHT:
        paddle_right.y += paddle_speed

    # Рух м’яча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Відбивання від країв
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Відбивання від ракеток
    if ball.colliderect(paddle_left):
        ball_speed_x *= -1
        ball.x = paddle_left.right + 5
    if ball.colliderect(paddle_right):
        ball_speed_x *= -1
        ball.x = paddle_right.left - BALL_SIZE - 5

    # Голи
    if ball.left <= 0:
        score_right += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x *= -1
    if ball.right >= WIDTH:
        score_left += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x *= -1

    if score_left >= WIN_SCORE or score_right >= WIN_SCORE:
        game_over = True
        winner = "Лівий" if score_left >= WIN_SCORE else "Правий"
        victory_screen(winner)
        continue

    draw()
    clock.tick(FPS)
