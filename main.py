import pygame
import random
import time
pygame.init()

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 900

swaps = 0
comparisons = 0

clock = pygame.time.Clock()

def createData(amount, maxValue):
    factor = maxValue / amount
    data = [int(i * factor) for i in range(1, amount + 1)]
    random.shuffle(data)
    return data

def drawData(data, heightOffset, highlight = []):
    SCREEN.fill("black")

    gap = WIDTH // len(data)

    scaleFactor = (HEIGHT - heightOffset) / max(data)

    for x in range(len(data)):
        color = "green" if x in highlight else "white"
        height = data[x] * scaleFactor
        rect = pygame.Rect(gap * x, HEIGHT - height, gap - 1, height)
        pygame.draw.rect(SCREEN, color, rect)

def displayStats(sort_time, visual_time, swaps, comparisons):
    font = pygame.font.SysFont('Times New Roman', 20)
    stats_text = font.render(f"Visual Time: {visual_time:.2f}s | Sort Time: {sort_time:.10f}s | Swaps: {swaps} | Comparisons: {comparisons}", True, (255, 255, 255))
    SCREEN.blit(stats_text, (10, 10))

def bubbleSort(data, visualize=True):
    global swaps, comparisons
    for x in range(len(data)):
        for y in range(len(data) - x - 1):
            comparisons += 1
            if data[y] > data[y + 1]:
                t = data[y]
                data[y] = data[y + 1]
                data[y + 1] = t
                swaps += 1
                if visualize:
                    yield data, [y, y + 1]

def main():
    highlightedIndices = []
    running = True
    sortGenerator = None
    startTime = 0
    visualTime = 0
    sortTime = 0

    data = createData(128, 1000)

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
                data, highlightedIndices = next(sortGenerator)
                visualTime = time.time() - startTime
            except StopIteration:
                sortGenerator = None

        drawData(data, 50, highlightedIndices)
        displayStats(sortTime, visualTime, swaps, comparisons)

        pygame.display.flip()
        clock.tick(FPS)
    
if __name__ == "__main__":
    main()