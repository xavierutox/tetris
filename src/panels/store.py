from settings import *

class Store:
    def __init__(self):
        
        self.surface = pygame.Surface((BOTTOM_LET_PANEL_WIDTH, BOTTOM_LET_PANEL_HEIGHT))
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.display_surface = pygame.display.get_surface()
        
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, BOTTOM_LET_PANEL_WIDTH, BOTTOM_LET_PANEL_HEIGHT), 1)
        
    def run(self):
        self.display_surface.blit(self.surface, (PADDING, PADDING + GAME_HEIGHT - BOTTOM_LET_PANEL_HEIGHT))