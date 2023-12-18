from settings import *

class Score:
    def __init__(self):
        
        self.surface = pygame.Surface((TOP_LEFT_PANEL_WIDTH, TOP_LEFT_PANEL_HEIGHT))
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.display_surface = pygame.display.get_surface()
        
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, TOP_LEFT_PANEL_WIDTH, TOP_LEFT_PANEL_HEIGHT), 1)
        
        
    def run(self):
        self.display_surface.blit(self.surface, (PADDING, PADDING))