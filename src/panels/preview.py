from settings import *

class Preview:
    def __init__(self):
        
        self.surface = pygame.Surface((RIGHT_PANEL_WIDTH, GAME_HEIGHT))
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.display_surface = pygame.display.get_surface()
        
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, RIGHT_PANEL_WIDTH, GAME_HEIGHT), 1)
        
        
    def run(self):
        self.display_surface.blit(self.surface, (3*PADDING + GAME_WIDTH + TOP_LEFT_PANEL_WIDTH, PADDING))
       