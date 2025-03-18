import pygame
import random
import time

# Constants
WIDTH, HEIGHT = 1000, 600
WHITE, RED = (255, 255, 255), (255, 0, 0)
FPS = 900

# Pygame Setup
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualization")
clock = pygame.time.Clock()

# Create Data Function with auto-computed bar width
def createData(amount, maxValue):
    bar_width = WIDTH // amount  # Automatically compute the bar width based on the amount of data
    factor = maxValue / amount
    data = [int(i * factor) for i in range(1, amount + 1)]
    random.shuffle(data)
    return data, bar_width

# Generate Random Data
array, bar_width = createData(1000, HEIGHT - 10)  # Generate 100 elements, max height of bars

sort_generator = None  # Holds the sorting generator

# Draw Function
def draw_array(arr, highlight=[]):
    win.fill((0, 0, 0))  # Clear screen
    for i, val in enumerate(arr):
        color = RED if i in highlight else WHITE
        pygame.draw.rect(win, color, (i * bar_width, HEIGHT - val, bar_width, val))
    pygame.display.flip()

# Non-Blocking Bubble Sort
def bubble_sort(arr, visualize=True, delay=10):
    n = len(arr)
    swaps, comparisons = 0, 0
    for i in range(n):
        for j in range(n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                if visualize:
                    draw_array(arr, [j, j + 1])  # Highlight swapped elements
                    yield  # Yield control to main loop to update visualization
    return swaps, comparisons

# Main Loop
running = True
start_time = None
sort_time = None  # To hold the real sorting time
visual_time = None  # To hold the visual time
sort_generator = None  # The sorting generator

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and sort_generator is None:
                # Start sorting for visualization
                array, bar_width = createData(100, HEIGHT - 10)  # Generate new data and compute bar width
                sort_generator = bubble_sort(array, delay=10)  # Set delay to slow sorting down
                start_time = time.time()  # Start time when the sorting begins

                # Run the sort a second time for accurate time measurement (no visualization)
                array_for_timing = array.copy()  # Copy the array to avoid altering the original
                start_time_real = time.time()
                bubble_sort(array_for_timing, visualize=False)  # Run sorting without visualization
                sort_time = time.time() - start_time_real  # Measure real sorting time

    # Step through sorting algorithm
    if sort_generator:
        try:
            next(sort_generator)  # Step to the next sorting iteration
        except StopIteration:
            visual_time = time.time() - start_time  # Measure visual sorting time
            sort_generator = None  # Stop when sorting is done

    # Draw the array and display times
    draw_array(array)
    if visual_time is not None and sort_time is not None:
        font = pygame.font.SysFont('Arial', 30)
        # Increase precision by formatting to 5 decimal places
        time_text = font.render(f"Visual Time: {visual_time:.5f}s  |  Sort Time: {sort_time:.10f}s", True, (255, 255, 255))
        win.blit(time_text, (10, 10))  # Position text on the screen

    pygame.display.flip()  # Refresh the screen
    clock.tick(FPS)  # Keeps animation smooth

pygame.quit()
