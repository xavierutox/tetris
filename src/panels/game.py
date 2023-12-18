from settings import GAME_HEIGHT, GAME_WIDTH, GRID_COLOR, PANEL_BACKGROUND_COLOR, TOP_LEFT_PANEL_WIDTH, PADDING, SQUARE_SIZE, OFFSET, COLUMNS, LINES, MOVE_SLEEP_TIME, TETROMINOS
import pygame
from timer import Timer

class Game:
    def __init__(self, random_bag, pieces, get_level, get_combo, get_lines, update_level, update_lines, update_score, update_combo, get_stored_piece, set_stored_piece, set_max_score, get_max_score, restart, get_score):
        
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.ghost_sprites = pygame.sprite.Group()
        self.get_level = get_level()
        self.update_level = update_level
        self.update_lines = update_lines
        self.update_score = update_score
        self.update_combo = update_combo
        self.set_max_score = set_max_score
        self.get_max_score = get_max_score
        self.get_score = get_score
        self.restart = restart
        self.random_bag = random_bag
        self.next_pieces = pieces
        self.get_combo = get_combo
        self.get_lines = get_lines
        self.get_stored_piece = get_stored_piece
        self.set_stored_piece = set_stored_piece
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(LINES)]
        self.time = (0.8 - ((self.get_level - 1) * 0.007)) ** (self.get_level - 1) * 1000
        self.spawn_tetromino()
        self.combo = -1
        self.store_lock = False
        
        self.timers = {
            'vertical_move_timer': Timer(self.time, True, self.move_down),
            'key_timer': Timer(MOVE_SLEEP_TIME),
        }
        self.timers['vertical_move_timer'].activate()
        
    def draw_grid(self):
        pygame.draw.rect(self.surface, GRID_COLOR, (0, 0, GAME_WIDTH, GAME_HEIGHT), 1)
        for column in range(1, COLUMNS):
            for line in range(1, LINES):
                pygame.draw.line(self.surface, GRID_COLOR, (column * SQUARE_SIZE, 0), (column * SQUARE_SIZE, GAME_HEIGHT))
                pygame.draw.line(self.surface, GRID_COLOR, (0, line * SQUARE_SIZE), (GAME_WIDTH, line * SQUARE_SIZE))
    
    def move_down(self):
        self.tetromino.move_down()

    def run(self):
        self.surface.fill(PANEL_BACKGROUND_COLOR)
        self.sprites.draw(self.surface)
        self.ghost_sprites.draw(self.surface)
        
        self.draw_grid()
        self.display_surface.blit(self.surface, (TOP_LEFT_PANEL_WIDTH + 2*PADDING, PADDING))
        self.input()
        self.timer_update()
        self.sprites.update()
        self.ghost_sprites.update()
        
        # if tetrnimo is in the vertical pos 0
        if all([block.pos.y >= 0 for block in self.tetromino.blocks]):
            self.tetromino.hard_drop_ghost()
        
        self.check_game_over()
        
    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
    
    def spawn_tetromino(self):
        self.check_finished_lines()
        if len(self.next_pieces) == 0:
            self.next_pieces = self.random_bag(self.get_stored_piece())
        self.tetromino = Tetromino(self.next_pieces.pop(), self.sprites, self.ghost_sprites, self.spawn_tetromino, self.field_data, self.update_score)
    
    def input(self):
        if not self.timers['key_timer'].active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.tetromino.move_down()
                self.update_score(1)
                self.timers['key_timer'].activate()
            elif keys[pygame.K_LEFT]:
                self.tetromino.move_left()
                self.timers['key_timer'].activate()
            elif keys[pygame.K_RIGHT]:
                self.tetromino.move_right()
                self.timers['key_timer'].activate()
            elif keys[pygame.K_SPACE]:
                self.tetromino.hard_drop()
                self.timers['key_timer'].activate()
            elif keys[pygame.K_z] or keys[pygame.K_LCTRL]:
                self.tetromino.counter_clock_wise_rotation()
                self.timers['key_timer'].activate()
            elif keys[pygame.K_UP]:
                self.tetromino.clock_wise_rotation()
                self.timers['key_timer'].activate()
            elif keys[pygame.K_c] or keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                self.handle_store()
                self.timers['key_timer'].activate()
    
    def check_finished_lines(self):
        # delete ghost blocks
        self.store_lock = False
        
        for block in self.ghost_sprites:
            block.kill()
        
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)
                
        if delete_rows:
            for delete_row in delete_rows:
                self.update_combo(self.get_combo() + 1)
                for block in self.sprites:
                    if block.pos.y == delete_row * SQUARE_SIZE:
                        block.kill()

                # move down blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row * SQUARE_SIZE:
                            block.pos.y += SQUARE_SIZE

            # rebuild field_data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(LINES)]
            for blocks in self.sprites:
                self.field_data[int(blocks.pos.y/SQUARE_SIZE)][int(blocks.pos.x/SQUARE_SIZE)] = block
                
        else:
            self.update_combo(-1)
        
        # update lines
        self.update_lines(len(delete_rows))
        if self.get_lines() % 10 == 0 and self.get_lines() != 0 and len(delete_rows) != 0:
            self.update_level(1)
            self.time = (0.8 - ((self.get_level - 1) * 0.007)) ** (self.get_level - 1) * 1000
            self.timers['vertical_move_timer'].time = self.time
            self.timers['vertical_move_timer'].activate()
            
        # check if field is empty
        perfect_clear = True
        for line in self.field_data:
            if any(line):
                perfect_clear = False
        
        if perfect_clear:
            if len(delete_rows) == 1:
                self.update_score(800 * self.get_level)
            elif len(delete_rows) == 2:
                self.update_score(1200 * self.get_level)
            elif len(delete_rows) == 3:
                self.update_score(1800 * self.get_level)
            elif len(delete_rows) == 4:
                self.update_score(2000 * self.get_level)
        else:
        
            if len(delete_rows) == 1:
                self.update_score(100 * self.get_level)
            elif len(delete_rows) == 2:
                self.update_score(300 * self.get_level)
            elif len(delete_rows) == 3:
                self.update_score(500 * self.get_level)
            elif len(delete_rows) == 4:
                self.update_score(800 * self.get_level)
        
        # combo
        if self.get_combo() > 0:
            self.update_score(50 * self.get_combo() * self.get_level)
    
    def handle_store(self):
        if not self.store_lock:
            self.store_lock = True
            for block in self.ghost_sprites:
                block.kill()
                
            if self.get_stored_piece() == None:
                self.set_stored_piece(self.tetromino.shape)
                for block in self.tetromino.blocks:
                    block.kill()
                
                self.spawn_tetromino()
            else: 
                temp = self.tetromino.shape
                for block in self.tetromino.blocks:
                    block.kill()
                self.tetromino = Tetromino(self.get_stored_piece(), self.sprites, self.ghost_sprites, self.spawn_tetromino, self.field_data, self.update_score)
                self.set_stored_piece(temp)
    
    
    def check_game_over(self):
        first_row = self.field_data[0]
        center = int(len(first_row)/2)
        if any(first_row[center-1:center+2]):
            if self.get_score() > self.get_max_score():
                self.set_max_score(self.get_score())
            self.restart()
            
        

class Tetromino:
    def __init__(self, shape, group, ghost_group, spawn_tetromino, field_data,update_score):
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.blocks = [Block(group, pos, self.color, field_data) for pos in self.block_positions]
        self.preview = [Block(ghost_group, pos, self.color, field_data, True) for pos in self.block_positions]
        self.spawn_tetromino = spawn_tetromino
        self.field_data = field_data
        self.shape = shape
        self.update_score = update_score
    
    def move_down(self):
        if not self.vertical_collision():
            for block in self.blocks:
                block.pos.y += SQUARE_SIZE
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE)] = block
            self.spawn_tetromino()
    
    def hard_drop(self):
        while not self.vertical_collision():
            self.update_score(2)
            self.move_down()
    
    
    def move_left(self):
        if not self.horizontal_collision('left'):
            self.reset_ghost_height()
            for block in self.blocks:
                block.pos.x -= SQUARE_SIZE
            for block in self.preview:
                block.pos.x -= SQUARE_SIZE
    
    def move_right(self):
        self.reset_ghost_height()
        if not self.horizontal_collision('right'):
            for block in self.blocks:
                block.pos.x += SQUARE_SIZE
            for block in self.preview:
                block.pos.x += SQUARE_SIZE
                
            
    def horizontal_collision(self, direction):
        for block in self.blocks:
            if direction == 'left':
                if block.pos.x - SQUARE_SIZE < 0:
                    return True
                # field_data collition
                if self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE) - 1]:
                    return True
            elif direction == 'right':
                if block.pos.x + SQUARE_SIZE >= GAME_WIDTH:
                    return True
                # field_data collition
                if self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE) + 1]:
                    return True
    
    def vertical_collision(self):
        for block in self.blocks:
            if block.pos.y + SQUARE_SIZE >= GAME_HEIGHT:
                return True
            # field_data collition
            if self.field_data[int(block.pos.y/SQUARE_SIZE) + 1][int(block.pos.x/SQUARE_SIZE)] and block.pos.y >= 0:
                return True
        return False

    def ghost_collision(self):
        for block in self.preview:
            if block.pos.y + SQUARE_SIZE >= GAME_HEIGHT:
                return True
            # field_data collition
            if self.field_data[int(block.pos.y/SQUARE_SIZE) + 1][int(block.pos.x/SQUARE_SIZE)] and block.pos.y >= 0:
                return True
        return False
    
    def move_down_ghost(self):
        if not self.ghost_collision():
            for block in self.preview:
                block.pos.y += SQUARE_SIZE
        else:
            for block in self.preview:
                block.pos.y -= SQUARE_SIZE
            return True
    
    def hard_drop_ghost(self):
        while not self.ghost_collision():
            self.move_down_ghost()
    
    def reset_ghost_height(self):
        for block in self.preview:
            block.pos.y = self.blocks[self.preview.index(block)].pos.y
    
    
    def clock_wise_rotation(self):
        self.reset_ghost_height()
        if self.shape == 'O':
            return
            
        # check if rotation is possible
        for block in self.blocks:
            # field_data collition
            if self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE)]:
                return
            
        for block in self.blocks:
            x = block.pos.x
            y = block.pos.y
            
            # check if rotation is possible
            if block.pos.x + self.blocks[0].pos.y - y < 0 or block.pos.x + self.blocks[0].pos.y - y >= GAME_WIDTH:
                return
            if block.pos.y - self.blocks[0].pos.x + x < 0 or block.pos.y - self.blocks[0].pos.x + x >= GAME_HEIGHT:
                return
        
        for block in self.blocks:
            x = block.pos.x
            y = block.pos.y

            block.pos.x = self.blocks[0].pos.x + self.blocks[0].pos.y - y
            block.pos.y = self.blocks[0].pos.y - self.blocks[0].pos.x + x
        self.update_ghost()
    
    def counter_clock_wise_rotation(self):
        self.reset_ghost_height()
        if self.shape == 'O':
            return
        
        # check if rotation is possible
        for block in self.blocks:
            # field_data collition
            if self.field_data[int(block.pos.y/SQUARE_SIZE)][int(block.pos.x/SQUARE_SIZE)]:
                return
            
        for block in self.blocks:
            x = block.pos.x
            y = block.pos.y
            # check if rotation is possible
            if block.pos.x - self.blocks[0].pos.y + y < 0 or block.pos.x - self.blocks[0].pos.y + y >= GAME_WIDTH:
                return
            if block.pos.y + self.blocks[0].pos.x - x < 0 or block.pos.y + self.blocks[0].pos.x - x >= GAME_HEIGHT:
                return
        
        for block in self.blocks:
            x = block.pos.x
            y = block.pos.y
            
            block.pos.x = self.blocks[0].pos.x - self.blocks[0].pos.y + y
            block.pos.y = self.blocks[0].pos.y + self.blocks[0].pos.x - x
        self.update_ghost()
    
    def update_ghost(self):
        for block in self.preview:
            block.pos.x = self.blocks[self.preview.index(block)].pos.x
            block.pos.y = self.blocks[self.preview.index(block)].pos.y
        while not self.ghost_collision():
            self.move_down_ghost()
        for block in self.preview:
            block.pos.y -= SQUARE_SIZE
            
            
    
        
    
    
class Block(pygame.sprite.Sprite):
        def __init__(self, group, pos, color, field_data, ghost=False):
            super().__init__(group)
            self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            self.image.fill(color)
            self.ghost = ghost
            if self.ghost:
                self.image.set_alpha(30)
            self.pos = pygame.Vector2(pos)*SQUARE_SIZE + OFFSET
            self.rect = self.image.get_rect(topleft=(self.pos.x,self.pos.y))
            self.field_data = field_data
        
        def update(self):
            self.rect.topleft = self.pos.x, self.pos.y