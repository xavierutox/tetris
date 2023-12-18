from settings import *
from sys import exit

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
        self.game = Game()
        self.score = Score()
        self.store = Store()
        self.preview = Preview()
        
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
            
            
            pygame.display.update()
            self.clock.tick(60)
        
if __name__ == "__main__":
    main = Main()
    main.run()