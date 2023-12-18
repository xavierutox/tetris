from settings import *
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
        
        # panels
        self.pieces = self.random_bag()
        self.preview = Preview(self.pieces)
        self.game = Game(self.random_bag, self.pieces)
        self.score = Score()
        self.store = Store()
        
    
    def random_bag(self):
        bag = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        selected = []
        while len(bag) > 0:
            selected.append(choice(bag))
            bag.remove(selected[-1])
        self.pieces = selected
        return selected
        
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
            
            
            pygame.display.update()
            self.clock.tick()
        
if __name__ == "__main__":
    main = Main()
    main.run()