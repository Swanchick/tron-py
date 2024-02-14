import pygame
from settings import *
from utils import RegisterManager
from object import *

class Game:
    def __init__(self, resolution):
        pygame.init()
        pygame.display.set_caption("Tron py")
        self.display = pygame.display.set_mode(resolution)
        self.run_game = True
        self.clock = pygame.time.Clock()
        self.resolution = resolution
    
    def find_objects_by_name(self, classname):
        objects = []
        
        for object in self.objects:
            if object.classname == classname:
                objects.append(object)
                
        return objects
    
    def get_objects(self):
        return self.objects
    
    def create_object(self, classname):
        object = RegisterManager.initialize_object(self, classname)
        
        self.objects.append(object)
    
    def close(self):
        self.run_game = False
    
    def run(self):
        self.objects = RegisterManager.initialize_all(self)
        
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    break

            self.update()
            
            self.display.fill((0, 0, 0))
            self.draw(self.display)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def update(self):
        for object in self.objects:
            object.update()
    
    def draw(self, display):
        for object in self.objects:
            object.draw(display)
        
game = Game(RES)

if __name__ == "__main__":
    game.run()