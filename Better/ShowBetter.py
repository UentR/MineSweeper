import pygame
from screeninfo import get_monitors

class Screen:
    pygame.init()
    # In Order: 
    # 		 Normal   Flaged     Pressed   Bomb		 1		   2		 3		   4		 5		   6		 7		   8
    liste = ['000000', '010000', '100000', '101111', '100001', '100010', '100011', '100100', '100101', '100110', '100111', '101000']
    
    def __init__(self, SizeX: int, SizeY: int, /, *, Fullscreen:bool = None) -> None:
        self.CellSize = min(get_monitors()[0].width/SizeX-1, get_monitors()[0].height/SizeY-1)
        self.sprite = {i: pygame.transform.scale(pygame.image.load(f"Better Sprites/{i}.png"), (self.CellSize, self.CellSize)) for i in self.liste} 

        size = (self.CellSize*SizeX, self.CellSize*SizeY)
        
        if Fullscreen:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN, pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
        
        pygame.display.update()
          
    def __call__(self, CurrentState):
        self.screen.fill((0, 0, 0))
        for x, row in enumerate(CurrentState):
            for y, value in enumerate(row):
                self.__ShowPixel(x, y, value)
        self.__Show()
    
    def __ShowPixel(self, x, y, value):
        if value>>5:
            Sprite = self.sprite[bin(value)[2:]]
        elif value>>4:
            Sprite = self.sprite[f'0{bin(value&16)[2:]}']
        else:
            Sprite = self.sprite['000000']
        self.screen.blit(Sprite, (x*self.CellSize, y*self.CellSize))
        
    def __Show(self):
        pygame.display.update()