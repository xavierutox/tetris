from settings import *

class Store:
    def __init__(self):
        
        self.surface = pygame.Surface((BOTTOM_LET_PANEL_WIDTH, BOTTOM_LET_PANEL_HEIGHT))
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, BOTTOM_LET_PANEL_WIDTH, BOTTOM_LET_PANEL_HEIGHT), 1)
        self.display_surface = pygame.display.get_surface()
        
    def run(self):
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.display_surface.blit(self.surface, (PADDING, PADDING + GAME_HEIGHT + PADDING))
