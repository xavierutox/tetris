from settings import WINDOWS_WIDTH, WINDOWS_HEIGHT, BACKGROUND_COLOR
import pygame
from sys import exit
from random import choice

# Panels
from panels.game import Game
from panels.score import Score
from panels.store import Store
from panels.preview import Preview

class Main:
    def __init__(self):
        
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")
        
        # score
        
        self.level_counter = 1
        self.lines_counter = 0
        self.score_counter = 0
        self.combo_counter = -1
        self.max_score = 0
        
        # panels
        self.pieces = self.random_bag()
        self.preview = Preview(self.pieces)
        self.game = Game(self.random_bag, self.pieces, self.get_level, self.get_combo, self.get_lines, self.update_level, self.update_lines, self.update_score, self.update_combo, self.get_stored_piece, self.set_stored_piece, self.set_max_score, self.get_max_score,self.restart, self.get_score, self.stop_music)
        self.score = Score(self.get_level, self.get_lines, self.get_score, self.get_combo, self.get_max_score)
        self.store = Store(self.get_stored_piece)
        
        # loop music
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)
        
        # Store
        self.stored_piece = None
        
        
    def stop_music(self):
        pygame.mixer.music.stop()
        
        
    
    def random_bag(self, stored_piece=None):
        bag = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        bag.remove(stored_piece) if stored_piece is not None else None
        selected = []
        while len(bag) > 0:
            selected.append(choice(bag))
            bag.remove(selected[-1])
        self.pieces = selected
        return selected

    def get_score(self):
        return self.score_counter
    
    def get_level(self):
        return self.level_counter
    
    def get_lines(self):
        return self.lines_counter
    
    def get_combo(self):
        return self.combo_counter
    
    def update_score(self, score):
        self.score_counter += score
        
    def update_level(self, level):
        self.level_counter += level
        
    def update_lines(self, lines):
        self.lines_counter += lines
    
    def update_combo(self, combo):
        self.combo_counter = combo
    
    def get_stored_piece(self):
        return self.stored_piece
    
    def set_stored_piece(self, piece):
        self.stored_piece = piece
        
    def get_max_score(self):
        return self.max_score
    
    def set_max_score(self, score):
        self.max_score = score


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.display_surface.fill(BACKGROUND_COLOR)
            
            self.game.run()
            self.score.run()
            self.store.run()
            self.preview.run()
            self.preview.update_pieces(self.pieces)
            
            self.input()
            
            pygame.display.update()
            self.clock.tick()
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.restart()
    
    def restart(self):
        self.level_counter = 1
        self.lines_counter = 0
        self.score_counter = 0
        self.combo_counter = -1
        self.pieces = self.random_bag()
        self.preview = Preview(self.pieces)
        self.game = Game(self.random_bag, self.pieces, self.get_level, self.get_combo, self.get_lines, self.update_level, self.update_lines, self.update_score, self.update_combo, self.get_stored_piece, self.set_stored_piece, self.set_max_score, self.get_max_score,self.restart, self.get_score, self.stop_music)
        self.score = Score(self.get_level, self.get_lines, self.get_score, self.get_combo, self.get_max_score)
        self.store = Store(self.get_stored_piece)
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)
        
if __name__ == "__main__":
    main = Main()
    main.run()