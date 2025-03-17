import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 1280, 700

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

def createData(amount, maxValue):
    factor = maxValue / amount
    data = [int(i * factor) for i in range(1, amount + 1)]
    random.shuffle(data)
    return data

def bubbleSort(data):
    for x in range(len(data)):
        for y in range(len(data) - x - 1):
            if data[y] > data[y + 1]:
                t = data[y]
                data[y] = data[y + 1]
                data[y + 1] = t

data = createData(1024, 1000)

def displayData(list):
    SCREEN.fill("white")

    gap = WIDTH / len(list)

    scaleFactor = (HEIGHT) / max(list)

    for x in range(len(list)):
        height = list[x] * scaleFactor
        rect = pygame.Rect(gap * x, HEIGHT - height, gap, height)
        pygame.draw.rect(SCREEN, "gray", rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    SCREEN.fill("white")

    displayData(data)
    bubbleSort(data)

    pygame.display.flip()