from Better.Better import Board
from Better.ShowBetter import Screen
import pygame

class Game:
    def __init__(self, diff) -> None:
        self.Difficulty = diff
        self.T = Board(self.Difficulty)
        self.Show = Screen(self.T.x, self.T.y)
        self.Show(self.T.Grid)
        self.Cell = self.Show.CellSize

    def Run(self):
        while True:
            for event in pygame.event.get():
                pass
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            X, Y = pygame.mouse.get_pos()
            X, Y = int(X//self.Cell), int(Y//self.Cell)
            if keys[pygame.K_ESCAPE]:
                break
            if keys[pygame.K_DOWN]:
                self.Difficulty -= 1
                pygame.time.delay(200)
            if keys[pygame.K_UP]:
                self.Difficulty += 1
                pygame.time.delay(200)
            if keys[pygame.K_SPACE]:
                pygame.quit()
                self.T = Board(self.Difficulty)
                self.Show = Screen(self.T.x, self.T.y)
                self.Show(self.T.Grid)
                self.Cell = self.Show.CellSize
                pygame.time.delay(200)
            if mouse[0]:
                self.T.GuideClick(X, Y, 0)
                self.Show(self.T.Grid)
            if mouse[1]:
                self.T.GuideClick(X, Y, 1)
                self.Show(self.T.Grid)
            if mouse[2]:
                self.T.GuideClick(X, Y, 2)
                self.Show(self.T.Grid)
                pygame.time.delay(100)