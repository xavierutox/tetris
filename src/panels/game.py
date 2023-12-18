from settings import *
from random import choice
from timer import Timer

class Game:
    def __init__(self):
        
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.level = 1
        self.next_pieces = self.random_bag()
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(LINES)]
        self.time = (0.8 - ((self.level - 1) * 0.007)) ** (self.level - 1) * 1000
        self.spawn_tetromino()
        
        self.timers = {
            'vertical move': Timer(self.time, True, self.move_down),
            'horizontal move': Timer(MOVE_SLEEP_TIME),
        }
        self.timers['vertical move'].activate()
        
    def draw_grid(self):
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, GAME_WIDTH, GAME_HEIGHT), 1)
        for column in range(1, COLUMNS):
            for line in range(1, LINES):
                pygame.draw.line(self.surface, GRID_COLOR, (column * SQUARE_SIZE, 0), (column * SQUARE_SIZE, GAME_HEIGHT))
                pygame.draw.line(self.surface, GRID_COLOR, (0, line * SQUARE_SIZE), (GAME_WIDTH, line * SQUARE_SIZE))
    
    def move_down(self):
        self.tetromino.move_down()
    
    def random_bag(self):
        bag = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        selected = []
        while len(bag) > 0:
            selected.append(choice(bag))
            bag.remove(selected[-1])
        
        return selected
        
        
    def run(self):
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.sprites.draw(self.surface)
        
        self.draw_grid()
        self.display_surface.blit(self.surface, (TOP_LEFT_PANEL_WIDTH + 2*PADDING, PADDING))
        self.input()
        self.timer_update()
        self.sprites.update()
        
    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
    
    def spawn_tetromino(self):
        if len(self.next_pieces) == 0:
            self.next_pieces = self.random_bag()
        self.tetromino = Tetromino(self.next_pieces.pop(), self.sprites, self.spawn_tetromino, self.field_data)
    
    def input(self):
        if not self.timers['horizontal move'].active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.tetromino.move_down()
                self.timers['horizontal move'].activate()
            elif keys[pygame.K_LEFT]:
                self.tetromino.move_left()
                self.timers['horizontal move'].activate()
            elif keys[pygame.K_RIGHT]:
                self.tetromino.move_right()
                self.timers['horizontal move'].activate()
            elif keys[pygame.K_SPACE]:
                self.tetromino.hard_drop()
                self.timers['horizontal move'].activate()
            elif keys[pygame.K_z] or keys[pygame.K_LCTRL]:
                self.timers['horizontal move'].activate()
                pass
            elif keys[pygame.K_c] or keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                self.timers['horizontal move'].activate()
                pass
        
        
        
class Tetromino:
    def __init__(self, shape, group, spawn_tetromino, field_data):
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.blocks = [Block(group, pos, self.color, field_data) for pos in self.block_positions]
        self.spawn_tetromino = spawn_tetromino
        self.field_data = field_data
    
    def move_down(self):
        if not self.vertical_collision():
            for block in self.blocks:
                block.pos.y += SQUARE_SIZE
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE)] = 1
            self.spawn_tetromino()
    
    def hard_drop(self):
        if not self.vertical_collision():
            while not self.vertical_collision():
                self.move_down()
    
    def move_left(self):
        if not self.horizontal_collision('left'):
            for block in self.blocks:
                block.pos.x -= SQUARE_SIZE
    
    def move_right(self):
        if not self.horizontal_collision('right'):
            for block in self.blocks:
                block.pos.x += SQUARE_SIZE
            
    def horizontal_collision(self, direction):
        for block in self.blocks:
            if direction == 'left':
                if block.pos.x - SQUARE_SIZE < 0:
                    return True
                # field_data collition
                if self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE) - 1] == 1:
                    return True
            elif direction == 'right':
                if block.pos.x + SQUARE_SIZE >= GAME_WIDTH:
                    return True
                # field_data collition
                if self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE) + 1] == 1:
                    return True
    
    def vertical_collision(self):
        for block in self.blocks:
            if block.pos.y + SQUARE_SIZE >= GAME_HEIGHT:
                return True
            # field_data collition
            if self.field_data[int(block.pos.y/SQUARE_SIZE) + 1][int(block.pos.x/SQUARE_SIZE)] == 1:
                return True
        return False
    
    
class Block(pygame.sprite.Sprite):
        def __init__(self, group, pos, color, field_data):
            super().__init__(group)
            self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            self.image.fill(color)
            self.pos = pygame.Vector2(pos)*SQUARE_SIZE + OFFSET
            self.rect = self.image.get_rect(topleft=(self.pos.x,self.pos.y))
            self.field_data = field_data
        
        def update(self):
            self.rect.topleft = self.pos.x, self.pos.y