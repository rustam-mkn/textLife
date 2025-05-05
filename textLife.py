import pygame
import numpy as np

CELL_SIZE = 2 # <--------- настроить размер
WIDTH, HEIGHT = 1000, 600 # <--------- настроить окно
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

def text_to_grid(text, font_size=300): # <--------- настроить масштаб
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.uint8)
    font = pygame.font.SysFont('Arial', font_size)

    text_surface = font.render(text, True, (255, 255, 255))
    surface = pygame.Surface(text_surface.get_size())
    surface.fill((0, 0, 0))
    surface.blit(text_surface, (0, 0))

    pixel_array = pygame.surfarray.pixels3d(surface)
    w, h = surface.get_size()

    offset_x = (GRID_WIDTH - w // CELL_SIZE) // 2
    offset_y = (GRID_HEIGHT - h // CELL_SIZE) // 2

    for x in range(0, w, CELL_SIZE):
        for y in range(0, h, CELL_SIZE):
            r, g, b = pixel_array[x][y]
            if int(r) + int(g) + int(b) > 100:
                gx = offset_x + x // CELL_SIZE
                gy = offset_y + y // CELL_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    grid[gy, gx] = 1

    return grid

def count_neighbors(grid):
    neighbors = np.zeros_like(grid)
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbors += np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
    return neighbors

def update(grid):
    neighbors = count_neighbors(grid)
    birth = (grid == 0) & (neighbors == 3)
    survive = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
    grid[:, :] = 0
    grid[birth | survive] = 1

def draw_grid(screen, grid):
    # Преобразуем в 3D RGB-массив и растягиваем до пикселей
    img = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3), dtype=np.uint8)
    img[grid == 1] = [255, 255, 255]
    img = np.repeat(np.repeat(img, CELL_SIZE, axis=0), CELL_SIZE, axis=1)
    surf = pygame.surfarray.make_surface(np.transpose(img, (1, 0, 2)))
    screen.blit(surf, (0, 0))

def run_simulation(user_text, speed=20): # <--------- настроить скорость
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Text to Cellular Automata")

    clock = pygame.time.Clock()
    grid = text_to_grid(user_text)

    show_time = 2000  # миллисекунд
    start_time = pygame.time.get_ticks()
    phase = "show_text"

    running = True
    while running:
        screen.fill((0, 0, 0))

        current_time = pygame.time.get_ticks()

        if phase == "show_text":
            draw_grid(screen, grid)
            if current_time - start_time > show_time:
                phase = "automaton"
        elif phase == "automaton":
            update(grid)
            draw_grid(screen, grid)

        pygame.display.flip()
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    user_text = input("Введите текст: ")
    run_simulation(user_text)
