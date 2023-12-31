from settings import RIGHT_PANEL_WIDTH, GAME_HEIGHT, GRID_COLOR, PANEL_BACKGROUND_COLOR, PADDING, TETROMINOS, SQUARE_SIZE, PREVIEW_1_POS_OFFSET, PREVIEW_2_POS_OFFSET, PREVIEW_3_POS_OFFSET, TOP_LEFT_PANEL_WIDTH, GAME_WIDTH
import pygame

class Preview:
    def __init__(self, pieces):
        
        self.surface = pygame.Surface((RIGHT_PANEL_WIDTH, GAME_HEIGHT))
        
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, RIGHT_PANEL_WIDTH, GAME_HEIGHT), 1)
        
        self.pieces = pieces
        self.previous_length = len(self.pieces)
        self.tetromino1 = Tetromino(self.pieces[-2], self.sprites, 0)
        self.tetromino2 = Tetromino(self.pieces[-3], self.sprites, 1)
        self.tetromino3 = Tetromino(self.pieces[-4], self.sprites, 2)
        
    def run(self):
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.sprites.draw(self.surface)
        self.display_surface.blit(self.surface, (3*PADDING + GAME_WIDTH + TOP_LEFT_PANEL_WIDTH, PADDING))
        self.delete_preview()
        
        
    def update_pieces(self, pieces):
        self.pieces = pieces
    
    def has_modified_pieces(self):
        if len(self.pieces) != self.previous_length:
            self.previous_length = len(self.pieces)
            return True
        return False
    
    def delete_preview(self):
        if self.has_modified_pieces():
            for block in self.sprites:
                block.kill()
            if len(self.pieces) > 0:
                self.tetromino1 = Tetromino(self.pieces[-1], self.sprites, 0)
            if len(self.pieces) > 1:
                self.tetromino2 = Tetromino(self.pieces[-2], self.sprites, 1)
            if len(self.pieces) > 2:
                self.tetromino3 = Tetromino(self.pieces[-3], self.sprites, 2)
    
    
class Tetromino:
    def __init__(self, shape, group, index):
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.index = index
        self.blocks = [Block(group, pos, self.color, index) for pos in self.block_positions]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color, index):
        super().__init__(group)
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(color)
        self.OFFSET = pygame.Vector2(0, 0)
        self.index = index
        if index == 0:
            self.OFFSET = PREVIEW_1_POS_OFFSET + pygame.Vector2(1, 3)*PADDING
        elif index == 1:
            self.OFFSET = PREVIEW_2_POS_OFFSET + pygame.Vector2(1, 3)*PADDING
        elif index == 2:
            self.OFFSET = PREVIEW_3_POS_OFFSET + pygame.Vector2(1, 3)*PADDING
        self.pos = pygame.Vector2(pos)*SQUARE_SIZE + self.OFFSET
        self.rect = self.image.get_rect(topleft=(self.pos.x,self.pos.y))