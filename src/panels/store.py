from settings import BOTTOM_LET_PANEL_HEIGHT, BOTTOM_LET_PANEL_WIDTH, GAME_HEIGHT, GRID_COLOR, PANEL_BACKGROUND_COLOR, PADDING, TETROMINOS, SQUARE_SIZE, TEXT_COLOR, FONT_SIZE
import pygame

class Store:
    def __init__(self, get_stored_piece):
        
        self.surface = pygame.Surface((BOTTOM_LET_PANEL_WIDTH, BOTTOM_LET_PANEL_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.get_stored_piece = get_stored_piece
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)
        
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, BOTTOM_LET_PANEL_WIDTH, BOTTOM_LET_PANEL_HEIGHT), 1)
        
        
    def run(self):
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.display_text()
        self.sprites.draw(self.surface)
        self.display_surface.blit(self.surface, (PADDING, GAME_HEIGHT - BOTTOM_LET_PANEL_HEIGHT + PADDING))
        self.update_stored_piece()
    
    def update_stored_piece(self):
        self.delete_stored_piece()
        if self.get_stored_piece() is not None:
            self.tetromino = Tetromino(self.get_stored_piece() , self.sprites)
    
    def delete_stored_piece(self):
        for block in self.sprites:
            block.kill()
    
    def display_text(self):
        text_surface = self.font.render("Stored", True, TEXT_COLOR)
        pos = pygame.Vector2(5, 1) * PADDING
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)
class Tetromino:
    def __init__(self, shape, group):
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(color)
        self.OFFSET = pygame.Vector2(4,6)
        self.pos = pygame.Vector2(pos)*SQUARE_SIZE + self.OFFSET * PADDING
        self.rect = self.image.get_rect(center=(self.pos.x,self.pos.y))
