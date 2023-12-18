from settings import *

class Score:
    def __init__(self, get_level, get_lines, get_score):
        
        self.surface = pygame.Surface((TOP_LEFT_PANEL_WIDTH, TOP_LEFT_PANEL_HEIGHT))
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.display_surface = pygame.display.get_surface()
        self.level = get_level
        self.lines = get_lines
        self.score = get_score
        
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, TOP_LEFT_PANEL_WIDTH, TOP_LEFT_PANEL_HEIGHT), 1)
        
        
    def run(self):
        self.display_surface.blit(self.surface, (PADDING, PADDING))