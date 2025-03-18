Best Approach: Using Generators + Event Loop

Instead of time.sleep(), let Pygame handle the sorting visualization frame by frame using a generator. Here’s how:
1. Modify Sorting Functions to Use yield

    Instead of blocking with time.sleep(), yield control back to the main loop.
    This lets Pygame keep updating the screen while sorting.

2. Use a Generator for Sorting

    Call next(sort_generator) every frame to progress the sorting.

3. Track Real Sorting Time Separately

    Use time.time() for actual sorting time.
    Use Pygame’s clock for visual time.