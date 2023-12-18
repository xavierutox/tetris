from settings import TOP_LEFT_PANEL_HEIGHT, TOP_LEFT_PANEL_WIDTH, GRID_COLOR, PANEL_BACKGROUND_COLOR, PADDING, TEXT_COLOR, FONT_SIZE
import pygame

class Score:
    def __init__(self, get_level, get_lines, get_score, get_combo, get_max_score):
        
        self.surface = pygame.Surface((TOP_LEFT_PANEL_WIDTH, TOP_LEFT_PANEL_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.get_score = get_score
        self.get_level = get_level
        self.get_lines = get_lines
        self.get_combo = get_combo
        self.get_max_score = get_max_score
        
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, TOP_LEFT_PANEL_WIDTH, TOP_LEFT_PANEL_HEIGHT), 1)
        
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)
        self.increment_height = self.surface.get_height() // 5
        
        
    def run(self):
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        
        for i, text in enumerate([('Max Score', str(self.get_max_score())), ('Score', str(self.get_score())), ('Level', str(self.get_level())), ('Lines', str(self.get_lines())), ('Combo', 0 if self.get_combo() <= 0 else str(self.get_combo()))]):
            x = self.surface.get_width() / 2
            y = self.increment_height * i + self.increment_height - 2 * PADDING
            
            self.display_text(text, (x, y))
        
        self.display_surface.blit(self.surface, (PADDING, PADDING))
    
    def display_text(self, text, pos):
        text_surface = self.font.render(f'{text[0]}: {text[1]}', True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)
        
    