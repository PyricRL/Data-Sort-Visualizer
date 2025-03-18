import pygame
import random
import time
pygame.init()

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 1000

swaps = 0
comparisons = 0

clock = pygame.time.Clock()

def createData(amount, maxValue):
    factor = maxValue / amount
    data = [int(i * factor) for i in range(1, amount + 1)]
    random.shuffle(data)
    return data

def drawData(data, heightOffset, swapIndex=None, compareIndex=None):
    SCREEN.fill("black")

    gap = WIDTH // len(data)

    scaleFactor = (HEIGHT - heightOffset) / max(data)

    for x in range(len(data)):
        if x == swapIndex:
            color = "green"
        elif x == compareIndex:
            color = "red"
        else:
            color = "white"
        height = data[x] * scaleFactor
        rect = pygame.Rect(gap * x, HEIGHT - height, gap, height)
        pygame.draw.rect(SCREEN, color, rect)

def displayStats(sort_time, visual_time, swaps, comparisons):
    font = pygame.font.SysFont('Times New Roman', 20)
    stats_text = font.render(f"Visual Time: {visual_time:.2f}s | Sort Time: {sort_time:.10f}s | Swaps: {swaps} | Comparisons: {comparisons}", True, (255, 255, 255))
    SCREEN.fill("black", (10, 10, 1000, 30))
    SCREEN.blit(stats_text, (10, 10))

def bubbleSort(data, visualize=True):
    global swaps, comparisons
    for x in range(len(data)):
        for y in range(len(data) - x - 1):
            comparisons += 1
            swapIndex = None
            compareIndex = y
            if data[y] > data[y + 1]:
                t = data[y]
                data[y] = data[y + 1]
                data[y + 1] = t
                swaps += 1
                swapIndex = y + 1
                if visualize:
                    yield data, swapIndex, compareIndex
    yield data, None, None

def main():
    running = True
    sortGenerator = None
    startTime = 0
    visualTime = 0
    sortTime = 0

    data = createData(128, 1000)

    drawData(data, 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and sortGenerator is None:
                    sortGenerator = bubbleSort(data)
                    startTime = time.time()
                    timingArray = data.copy()
                    startTimeReal = time.time()
                    bubbleSort(timingArray, visualize=False)
                    sortTime = time.time() - startTimeReal
    
        if sortGenerator:
            try:
                data, swapIndex, compareIndex = next(sortGenerator)
                drawData(data, 20, swapIndex, compareIndex)
                visualTime = time.time() - startTime
            except StopIteration:
                sortGenerator = None
        
        displayStats(sortTime, visualTime, swaps, comparisons)

        pygame.display.flip()
        clock.tick(FPS)
    
if __name__ == "__main__":
    main()