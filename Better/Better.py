import numpy as np
from random import randint as rd

class Board:
    __First = True
    __Dir = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

    def __init__(self, Difficulty) -> None:
        if Difficulty in [0, "Simple", "simple"]:
            self.x, self.y = 9, 9
            self.__Difficulty = 0
        elif Difficulty in [1, "Normal", "normal"]:
            self.x, self.y = 16, 16
            self.__Difficulty = 1
        elif Difficulty in [2, "Difficile", "difficile"]:
            self.x, self.y = 30, 16
            self.__Difficulty = 2
        else:
            self.x, self.y = 3, 3
            self.__Difficulty = 3
        self.Grid = np.zeros((self.x, self.y), dtype=np.ubyte)
        self.Total = self.x*self.y
            
    def GuideClick(self, x, y, Mouse):
        if self.__First and Mouse==0:
            self.__HandleFirstClick(x, y)
            return
        if Mouse==1 and self.Grid[x][y]>>4==2:
            self.__ClickAll(x, y)
            return 
        if Mouse==2:
            self.__Flag(x, y)
            return
        if self.Grid[x][y]>>5: return
        self.__HandleClick(x, y)
    
    def __ClickAll(self, x, y):
        count = self.Grid[x][y]&15
        for Dx, Dy in self.__Dir:
            Nx, Ny = x+Dx, y+Dy
            if 0 <= Nx < self.x and 0 <= Ny < self.y and self.Grid[Nx][Ny]&16 == 16:
                count -= 1
        if count: return
        
        for Dx, Dy in self.__Dir:
            Nx, Ny = x+Dx, y+Dy
            if 0 <= Nx < self.x and 0 <= Ny < self.y and self.Grid[Nx][Ny]&16 != 16:
                self.GuideClick(Nx, Ny, 0)
        
       
    def __HandleClick(self, x, y):
        if self.Grid[x][y]&15==15:
            self.Continue = False
            self.__ShowMine()
            return
        elif self.Grid[x][y]|16 == 16:
            self.__RecursiveOpening(x, y)
            return 
        else:
            self.Total -= 1
            self.Grid[x][y] = (self.Grid[x][y]|48)^16 # Unflag the tile and see it
            return 
    
    def __RecursiveOpening(self, _x, _y):
        Blank = [(_x, _y)]
        while Blank:
            x, y = Blank.pop(0)
            self.Total -= 1
            self.Grid[x][y] = (self.Grid[x][y]|48)^16 # Unflag the tile and see it
            for Dx, Dy in self.__Dir:
                Nx, Ny = x+Dx, y+Dy
                if 0 <= Nx < self.x and 0 <= Ny < self.y:
                    if self.Grid[Nx][Ny]|16 == 16:
                        Blank.append((Nx, Ny))
                    elif self.Grid[Nx][Ny]&15 != 15:
                        self.Total -= 1
                        self.Grid[Nx][Ny] = (self.Grid[Nx][Ny]|48)^16 # Unflag the tile and see it
            
    def __Flag(self, x, y):
        # The two leftmost bits represent visibility and flag
        # We can only flag unseen tile so 00 or 01 bits
        if (self.Grid[x][y]>>4) == 1:
            self.Grid[x][y] -= 16
        elif (self.Grid[x][y]>>4) == 0:
            self.Grid[x][y] += 16
    
    def __HandleFirstClick(self, x, y):
        self.__Generate(x, y)
        # The leftmost bit represents visibility
        # A 1 mean that it is visible
        # So we add 32 or 2^5 on the first click
        self.Grid[x][y] += 32
        self.__First = False
        if self.Grid[x][y] == 32:
            self.__RecursiveOpening(x, y)
            
    def __Generate(self, x, y):
        MineDiff = [11, 40, 100, 2]
        NbrMine = 0
        Try = 0
        while NbrMine < MineDiff[self.__Difficulty]:
            _x, _y = rd(0, self.x-1), rd(0, self.y-1)
            if self.Grid[_x][_y] != 15 and (np.sqrt((x-_x)**2+(y-_y)**2) > 2 or (Try > 200 and (_x, _y) != (x, y))):
                # A mine is represented by XX1111 which can't be the number of neighbors 
                self.Grid[_x][_y] += 15 
                NbrMine += 1
            else:
                Try += 1
            if Try > 1000:
                print('impossible')
                break
        self.Total -= NbrMine
        self.__CalculateMine()
    
    def __CalculateMine(self):
        for x, row in enumerate(self.Grid):
            for y, value in enumerate(row):
                if value == 15: continue # If it is a mine we don't calculate the number of neighbors
                
                count = 0
                for Dx, Dy in self.__Dir:
                    Nx, Ny = x+Dx, y+Dy
                    if 0 <= Nx < self.x and 0 <= Ny < self.y and self.Grid[Nx][Ny]==15:
                        count += 1
                self.Grid[x][y] = count
    
    def __ShowMine(self):
        for x, row in enumerate(self.Grid):
            for y, value in enumerate(row):
                if value&15 == 15:
                    self.Grid[x][y] = 47
    
    def __repr__(self):
        msg = ''
        for x in self.Grid:
            for y in x:
                msg += f"{bin(y)[2:]:0>6}\t"
            msg += '\n'
        return msg
        

if __name__ == "__main__":
    T = Board(10)
    print(T.GuideClick(0, 0, 1))
    print(T)
    print()

    x, y = int(input()), int(input())
    T.GuideClick(x, y, 0)
    print(T)

    x, y = int(input()), int(input())
    T.GuideClick(x, y, 1)
    print(T)