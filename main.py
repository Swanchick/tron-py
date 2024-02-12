import pygame
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(RES)
        self.run_game = True
        self.clock = pygame.time.Clock()
    
    def run(self):
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False

            self.update()
            
            self.display.fill((0, 0, 0))
            self.draw(self.display)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def update(self):
        pass
    
    def draw(self, display):
        pygame.draw.rect(display, (255, 255, 255), (100, 100, 100, 100))
        
game = Game()

if __name__ == "__main__":
    game.run()