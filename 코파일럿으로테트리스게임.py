#cmd
#pip install pygame

import pygame
import random

# 게임 설정
WINDOW_WIDTH, WINDOW_HEIGHT = 300, 600
BLOCK_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE

# 색상
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (128, 0, 128)   # T
]

# 블록 모양
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],        # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 0], [1, 1, 1]]   # T
]

class Tetromino:
    def __init__(self):
        self.type = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.type]
        self.color = COLORS[self.type]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_board():
    return [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def check_collision(board, tetromino, dx, dy, rotated_shape=None):
    shape = rotated_shape if rotated_shape else tetromino.shape
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx = tetromino.x + x + dx
                ny = tetromino.y + y + dy
                if nx < 0 or nx >= BOARD_WIDTH or ny >= BOARD_HEIGHT:
                    return True
                if ny >= 0 and board[ny][nx] != BLACK:
                    return True
    return False

def merge_board(board, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                ny = tetromino.y + y
                nx = tetromino.x + x
                if 0 <= ny < BOARD_HEIGHT and 0 <= nx < BOARD_WIDTH:
                    board[ny][nx] = tetromino.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == BLACK for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [BLACK for _ in range(BOARD_WIDTH)])
    return new_board, lines_cleared

def draw_board(screen, board, tetromino):
    screen.fill(GRAY)
    # Draw board
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            color = board[y][x]
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    # Draw tetromino
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = tetromino.x + x
                ny = tetromino.y + y
                if ny >= 0:
                    pygame.draw.rect(screen, tetromino.color, (nx * BLOCK_SIZE, ny * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(screen, BLACK, (nx * BLOCK_SIZE, ny * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("테트리스")
    clock = pygame.time.Clock()
    board = create_board()
    tetromino = Tetromino()
    fall_time = 0
    fall_speed = 500
    score = 0
    running = True

    while running:
        dt = clock.tick(60)
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, tetromino, -1, 0):
                        tetromino.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, tetromino, 1, 0):
                        tetromino.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, tetromino, 0, 1):
                        tetromino.y += 1
                elif event.key == pygame.K_UP:
                    rotated = [list(row) for row in zip(*tetromino.shape[::-1])]
                    if not check_collision(board, tetromino, 0, 0, rotated):
                        tetromino.shape = rotated

        if fall_time > fall_speed:
            fall_time = 0
            if not check_collision(board, tetromino, 0, 1):
                tetromino.y += 1
            else:
                merge_board(board, tetromino)
                board, lines = clear_lines(board)
                score += lines * 100
                tetromino = Tetromino()
                if check_collision(board, tetromino, 0, 0):
                    running = False  # 게임 오버

        draw_board(screen, board, tetromino)
        pygame.display.flip()

    print("게임 오버! 점수:", score)
    pygame.quit()

if __name__ == "__main__":
    main()

