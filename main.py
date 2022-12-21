import time
import random
import pygame
from tkinter import simpledialog, messagebox
from tkinter import *

def sprites():
    global case, sprite
    liste = ['normal', 'press', 'bomb', '1', '2', '3', '4', '5', '6', '7', '8', 'flag']
    sprite = []
    for i in liste:
        img = pygame.image.load('Sprites/' + i + '.png')
        img = pygame.transform.scale(img, (case, case))
        sprite.append(img)

def diff():
    global width, height, case, ans
    root = Tk().withdraw()
    ans = 'val'
    while not ans in ['simple', 'normal', 'difficile']:
        ans = simpledialog.askstring("Jouer", "Choisissez entre Simple, Normal et Difficile")
        ans = str(ans.lower())
    if ans == 'simple':
        width, height, case = 9, 9, 115
    elif ans == 'normal':
        width, height, case = 16, 16, 65
    else:
        width, height, case = 30, 16, 63
    create()

def create():
    global width, height, grid
    grid = []
    for i in range(width * height):
        grid.append(0)

def f(x):
    return int(round(4.23469 * x - 27.9694, 0) + 1)

def test(x):
    global grid
    if x < 0:
        return 0
    try:
        if grid[x] != -1:
            grid[x] += 1
    except:
        pass

def mine():
    global grid, width, height, mouseX, mouseY
    mouse = mouseY * width + mouseX
    for i in range(f(width)):
        done = 0
        while done != 1:
            nbr = random.randint(0, len(grid) - 1)
            if grid[nbr] != -1 and nbr != mouse:
                done = 1
                grid[nbr] = -1
                if (nbr + 1) % width == 0:
                    test(nbr - 1)
                    test(nbr - width)
                    test(nbr - width - 1)
                    test(nbr + width)
                    test(nbr + width - 1)
                elif nbr % width == 0:
                    test(nbr + 1)
                    test(nbr - width)
                    test(nbr - width + 1)
                    test(nbr + width)
                    test(nbr + width + 1)
                else:
                    test(nbr - 1)
                    test(nbr + 1)
                    test(nbr - width)
                    test(nbr - width - 1)
                    test(nbr - width + 1)
                    test(nbr + width)
                    test(nbr + width - 1)
                    test(nbr + width + 1)

def disp():
    global grid, surface, width, case, sprite
    x = 0
    y = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    t = 0
    for i in grid:
        surface.blit(sprite[0], (case * x, case * y))
        '''text = font.render(str(i), True, (255, 255, 255))
        surface.blit(text, (case * x, case * y))'''
        x += 1
        t += 1
        if x == width:
            x = 0
            y += 1

def mouse():
    global mouseX, mouseY, case
    for event in pygame.event.get():
        if True:
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseX //= case
            mouseY //= case

def rest():
    global sprite, surface, grid, pressed, width, case, hover
    for x, y in hover:
        surface.blit(sprite[0], (x * case, y * case))
    hover.pop(0)
    pygame.display.update()

def press():
    global sprite, surface, mouseX, mouseY, case, pressed
    test = mouseY * width + mouseX
    if test not in pressed:
        surface.blit(sprite[1], (mouseX * case, mouseY * case))
        pygame.display.update()

def click():
    global mouseX, mouseY, width, surface, sprite, case, pressed
    win()
    nbr = mouseY * width + mouseX
    if nbr not in pressed:
        if grid[nbr] == -1:
            loose()
        if grid[nbr] > 0:
            surface.blit(sprite[grid[nbr] + 2], (mouseX * case, mouseY * case))
            pressed.append(nbr)
        if grid[nbr] == 0:
            surface.blit(sprite[1], (mouseX * case, mouseY * case))
            find(mouseX, mouseY)

def premier():
    first = 0
    pr = 0
    while first == 0:
        mouse()
        if pygame.mouse.get_pressed()[0]:
            pr = 1
        if pr == 1 and not pygame.mouse.get_pressed()[0]:
            pr = 0
            mine()
            click()
            first = 1

def find(x, y):
    global width, surface, sprite, case, pressed
    nbr = y * width + x
    if nbr not in pressed:
        try:
            if nbr >= 0 and grid[nbr] != -1:
                pressed.append(nbr)
                if (nbr + 1) % width == 0:
                    if grid[nbr] != 0:
                        surface.blit(sprite[grid[nbr] + 2], (x * case, y * case))
                    else:
                        surface.blit(sprite[1], (x * case, y * case))
                        find(x - 1, y)
                        find(x, y - 1)
                        find(x - 1, y - 1)
                        find(x, y + 1)
                        find(x - 1, y + 1)
                elif nbr % width == 0:
                    if grid[nbr] != 0:
                        surface.blit(sprite[grid[nbr] + 2], (x * case, y * case))
                    else:
                        surface.blit(sprite[1], (x * case, y * case))
                        find(x + 1, y)
                        find(x, y - 1)
                        find(x + 1, y - 1)
                        find(x, y + 1)
                        find(x + 1, y + 1)
                else:
                    if grid[nbr] != 0:
                        surface.blit(sprite[grid[nbr] + 2], (x * case, y * case))
                    else:
                        surface.blit(sprite[1], (x * case, y * case))
                        find(x - 1, y)
                        find(x + 1, y)
                        find(x, y - 1)
                        find(x - 1, y - 1)
                        find(x + 1, y - 1)
                        find(x, y + 1)
                        find(x - 1, y + 1)
                        find(x + 1, y + 1)
        except:
            pass

def win():
    global pressed, grid, width, fin, surface
    if len(pressed) == len(grid) - f(width):
        fin = 1

def loose():
    global grid, surface, width, case, fin
    x = 0
    y = 0
    for i in grid:
        if 1 <= i:
            surface.blit(sprite[i + 2], (x * case, y * case))
        if i == -1:
            surface.blit(sprite[2], (x * case, y * case))
        if i == 0:
            surface.blit(sprite[1], (x * case, y * case))
        x += 1
        if x == width:
            x = 0
            y += 1
    pygame.display.update()
    fin = 2

def right():
    global mouseX, mouseY, sprite, surface, pressed, width, case
    nbr = mouseY * width + mouseX
    if nbr not in pressed:
        surface.blit(sprite[-1], (mouseX * case, mouseY * case))

def gauche():
    global pr
    if pygame.mouse.get_pressed()[0]:
        pr = 1
    if pr == 1 and not pygame.mouse.get_pressed()[0]:
        pr = 0
        click()

def droite():
    global rp
    if pygame.mouse.get_pressed()[2]:
        rp = 1
    if rp == 1 and not pygame.mouse.get_pressed()[2]:
        rp = 0
        right()

def tour():
    mouse()
    gauche()
    droite()
    win()

pygame.init()

pressed = []
diff()
sprites()
surface = pygame.display.set_mode([width * case, height * case])
surface.fill((255, 255, 255))
disp()
pygame.display.update()
fin = 0
pr = 0
rp = 0
hover = []
deb = time.time()
first = 0
premier()
pygame.display.update()
while fin == 0:
    tour()
    pygame.display.update()

fin = round(time.time() - deb, 2)
if fin == 1:
    msg = "Félicitation, vous avez gagné en difficulté " + ans + ", en " + str(fin) + " secondes"
else:
    msg = "Malheureusement vous avez échouez en difficulté " + ans + ", en " + str(fin) + " secondes"

messagebox.showinfo('Résultat', msg)
