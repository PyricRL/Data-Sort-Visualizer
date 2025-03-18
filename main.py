import pygame
import random
import time
pygame.init()

WIDTH, HEIGHT = 1280, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 9999999999999999999999999999

swaps = 0
comparisons = 0

complexity = ""

clock = pygame.time.Clock()

def createData(amount, maxValue):
    factor = maxValue / amount
    data = [int(i * factor) for i in range(1, amount + 1)]
    random.shuffle(data)
    return data

def drawData(data, heightOffset, swapIndex=None, compareIndex=None, compareIndex2=None):
    SCREEN.fill("black")

    gap = WIDTH // len(data)

    scaleFactor = (HEIGHT - heightOffset) / max(data)

    for x in range(len(data)):
        if x == swapIndex:
            color = "green"
        elif x == compareIndex or x == compareIndex2:
            color = "red"
        else:
            color = "white"
        height = data[x] * scaleFactor
        rect = pygame.Rect(gap * x, HEIGHT - height, gap, height)
        pygame.draw.rect(SCREEN, color, rect)

def displayStats(sortTime, visualTime, swaps, comparisons, complexity):
    font = pygame.font.SysFont('Times New Roman', 20)
    stats_text = font.render(f"Visual Time: {visualTime:.2f}s | Sort Time: {(sortTime * 1000):.10f}ms | Swaps: {swaps} | Comparisons: {comparisons} | Complexity: {complexity}", True, (255, 255, 255))
    SCREEN.fill("black", (10, 10, 1000, 30))
    SCREEN.blit(stats_text, (10, 10))

def bubbleSort(data, visualize=True):
    global swaps, comparisons, complexity
    startSortTime = time.time() if not visualize else None
    for x in range(len(data)):
        for y in range(len(data) - x - 1):
            comparisons += 1
            swapIndex = None
            compareIndex = y
            if data[y] > data[y + 1]:
                swap(data, y, y + 1)
                swapIndex = y + 1
                if visualize:
                    yield data, swapIndex, compareIndex, None

    if not visualize:
        return time.time() - startSortTime
    
    yield data, None, None, None

def mergeSort(data, left, right, visualize=False):
    global swaps, comparisons
    startSortTime = time.time() if not visualize else None
    if left < right:
        mid = (left + right) // 2

        yield from mergeSort(data, left, mid)
        yield from mergeSort(data, mid + 1, right)
        yield from merge(data, left, mid, right)
    if not visualize:
        return time.time() - startSortTime

def merge(data, left, mid, right, visualize=True):
    global swaps, comparisons
    n1 = mid - left + 1
    n2 = right - mid

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = data[left + i]

    for j in range(n2):
        R[j] = data[mid + 1 + j]

    i = 0 
    j = 0
    k = left 

    while i < n1 and j < n2:
        swapIndex = None

        compareIndexL = left + i
        compareIndexR = mid + 1 + j

        comparisons += 1
        if L[i] <= R[j]:
            data[k] = L[i]
            i += 1
        else:
            data[k] = R[j]
            j += 1
            swaps += 1
        k += 1
        if visualize:
            yield data, swapIndex, compareIndexL, compareIndexR

    while i < n1:
        swapIndex = i
        data[k] = L[i]
        i += 1
        k += 1
        swaps += 1
        yield data, left + i, compareIndexL, compareIndexR

    while j < n2:
        swapIndex = j
        data[k] = R[j]
        j += 1
        k += 1
        swaps += 1
        yield data, mid + 1 + j, compareIndexL, compareIndexR

def bogoSort(data, visualize=True):
    global swaps, comparisons
    startSortTime = time.time() if not visualize else None

    def isSorted(data):
        for i in range(len(data) - 1):
            if data[i] > data[i + 1]:
                return False
        return True
    
    sorted = isSorted(data)
    
    while not sorted:
        random.shuffle(data)

        randIndex1 = random.randint(0, len(data) - 1)
        randIndex2 = random.randint(0, len(data) - 1)
        randIndex3 = random.randint(0, len(data) - 1)

        swaps += 1

        if visualize:
            yield data, randIndex1, randIndex2, randIndex3
        sorted = isSorted(data)
    
    if not visualize:
        return time.time() - startSortTime

def partition(data, low, high, visualize=True):
    global swaps, comparisons
    swapIndex = None
    compareIndexL = None
    compareIndexR = None
    pivotNum = data[high]
    pivot = data[pivotNum]
    i = low - 1

    for j in range(low, high):
        comparisons += 1
        if data[j] <= pivot:
            swapIndex = data[j]
            compareIndexL = data[i]
            i += 1
            swap(data, i, j)
            if visualize:
                yield data, swapIndex, compareIndexL, compareIndexR
    
    swap(data, i + 1, high)

    return i + 1

def quickSort(data, low, high, visualize=True):
    startSortTime = time.time() if not visualize else None
    if low < high:
        part = partition(data, low, high, visualize=False)
        yield from quickSort(data, low, part - 1)
        yield from quickSort(data, part + 1, high)
    
    if not visualize:
        return time.time() - startSortTime


def timeSort(sortFunc, data, *args, **kwargs):
    startTime = time.time()
    if kwargs.get("visualize", True):
        return sortFunc(data, *args, **kwargs)
    else:
        result = sortFunc(data, *args, **kwargs)
        return time.time() - startTime
    
def swap(data, i, j):
    global swaps
    data[i], data[j] = data[j], data[i]
    swaps += 1


def main():
    global swaps, comparisons, complexity
    running = True
    sortGenerator = None
    startTime = 0
    visualTime = 0
    sortTime = 0

    data = createData(640, 1000)

    drawData(data, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and sortGenerator is None:
                    swaps = 0
                    comparisons = 0
                    timingData = data.copy()
                    sortMethod = bubbleSort

                    if sortMethod == bubbleSort:
                        sortGenerator = timeSort(bubbleSort, data, visualize=True)
                        sortTime = timeSort(bubbleSort, timingData, visualize=False)
                        complexity = "O(n\u00b2)"
                    elif sortMethod == mergeSort:
                        sortGenerator = timeSort(mergeSort, data, 0, len(data) - 1, visualize=True)
                        sortTime = timeSort(mergeSort, timingData, 0, len(data) - 1, visualize=False)
                        complexity = "O(n log n)"
                    elif sortMethod == bogoSort:
                        sortGenerator = timeSort(bogoSort, data, visualize=True)
                        sortTime = timeSort(bogoSort, data, visualize=False)
                        complexity = "O(n!)"
                    elif sortMethod == quickSort:
                        sortGenerator = timeSort(quickSort, data, 0, len(data) - 1, visualize=True)
                        sortTime = timeSort(quickSort, data, 0, len(data) - 1, visualize=False)
                        complexity = "O(n log n)"
                    startTime = time.time()
    
        if sortGenerator:
            try:
                data, swapIndex, compareIndexL, compareIndexR = next(sortGenerator)
                drawData(data, 50, swapIndex, compareIndexL, compareIndexR)
                visualTime = time.time() - startTime
            except StopIteration:
                sortGenerator = None
        
        displayStats(sortTime, visualTime, swaps, comparisons, complexity)

        pygame.display.flip()
        clock.tick(FPS)
    
if __name__ == "__main__":
    main()