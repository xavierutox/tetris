import pygame

COLUMNS = 10
LINES = 20
SQUARE_SIZE = 40
OFFSET = pygame.Vector2(COLUMNS // 2, -1) * SQUARE_SIZE

# Tetris panel
GAME_WIDTH = COLUMNS * SQUARE_SIZE
GAME_HEIGHT = LINES * SQUARE_SIZE

# Top Left panel (score, level and lines)
TOP_LEFT_PANEL_WIDTH = 150
TOP_LEFT_PANEL_FRACTION = 0.3
TOP_LEFT_PANEL_HEIGHT = GAME_HEIGHT * TOP_LEFT_PANEL_FRACTION

# Bottom left panel (stored piece)
BOTTOM_LET_PANEL_WIDTH = 150
BOTTOM_LET_PANEL_FRACTION = 0.2
BOTTOM_LET_PANEL_HEIGHT = GAME_HEIGHT * BOTTOM_LET_PANEL_FRACTION

# Right panel (piece preview)

RIGHT_PANEL_WIDTH = 150

PADDING = 20
WINDOWS_WIDTH = GAME_WIDTH + TOP_LEFT_PANEL_WIDTH + RIGHT_PANEL_WIDTH + 4 * PADDING
WINDOWS_HEIGHT = GAME_HEIGHT + 2 * PADDING

MOVE_SLEEP_TIME = 100

# Colors
BACKGROUND_COLOR = (20, 20, 20)
PANEL_BACKGROUND_COLOR = (40, 40, 40)
GRID_COLOR = (80, 80, 80)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

TETROMINOS = {
    'I': {'shape': [(-1, 0), (0, 0), (1, 0), (2, 0)], 'color': CYAN},
    'J': {'shape': [(-1, -1), (-1, 0), (0, 0), (1, 0)], 'color': BLUE},
    'L': {'shape': [(-1, 0), (0, 0), (1,0), (1, -1)], 'color': ORANGE},
    'O': {'shape': [(0, 0), (1, 0), (0, 1), (1, 1)], 'color': YELLOW},
    'S': {'shape': [(-1, 1), (0, 1), (0, 0), (1, 0)], 'color': GREEN},
    'Z': {'shape': [(-1, 0), (0, 0), (0, 1), (1, 1)], 'color': RED},
    'T': {'shape': [(-1, 0), (0, 0), (0, -1), (1, 0)], 'color': PURPLE}
}