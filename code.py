import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Initialize the matrix
matrix = np.full((5, 5), "0", dtype=object)

# Set starting and ending points
matrix[0, 0] = "A1"
matrix[1, 4] = "A2"
matrix[2, 0] = "B1"
matrix[2, 4] = "B2"
matrix[3, 0] = "C1"
matrix[4, 4] = "C2"

# Locate points in the matrix
def locate_points(matrix):
    points = {}
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            if matrix[i, j] != "0":
                points[matrix[i, j]] = (i, j)
    return points

point_positions = locate_points(matrix)
A1, A2 = point_positions["A1"], point_positions["A2"]
B1, B2 = point_positions["B1"], point_positions["B2"]
C1, C2 = point_positions["C1"], point_positions["C2"]

# Function to fill paths simultaneously with maximum coverage
def fill_paths_max_coverage(matrix, starts_ends, labels):
    queue = deque()
    directions = {}
    arrow_map = {(0, 1): "→", (1, 0): "↓", (0, -1): "←", (-1, 0): "↑"}
    visited = set()

    # Initialize the queue with all start points
    for (start, end), label in zip(starts_ends, labels):
        queue.append((start, end, label, None))  # (current position, destination, label, prev direction)
        visited.add(start)

    while queue:
        next_queue = deque()
        while queue:
            current, end, label, prev_direction = queue.popleft()
            row, col = current

            # If we reached the end, mark it
            if current == end:
                matrix[end[0], end[1]] = f"{label}2"
                continue

            # Mark the current cell if it's empty
            if matrix[row, col] == "0":
                matrix[row, col] = label

            # Explore neighbors in all directions, prioritize empty cells
            neighbors = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
                new_row, new_col = row + dr, col + dc
                new_cell = (new_row, new_col)

                if (
                    0 <= new_row < matrix.shape[0]
                    and 0 <= new_col < matrix.shape[1]
                    and (matrix[new_row, new_col] == "0" or new_cell == end)
                    and new_cell not in visited
                ):
                    neighbors.append((new_cell, (dr, dc)))

            # Sort neighbors to prioritize empty cells over already visited cells
            neighbors.sort(key=lambda x: matrix[x[0][0], x[0][1]] != "0")

            for new_cell, (dr, dc) in neighbors:
                # Mark the direction for this movement
                directions[new_cell] = arrow_map[(dr, dc)]
                visited.add(new_cell)
                next_queue.append((new_cell, end, label, (dr, dc)))

        queue = next_queue

    return directions

# Fill paths
starts_ends = [(A1, A2), (B1, B2), (C1, C2)]
labels = ["A", "B", "C"]
directions = fill_paths_max_coverage(matrix, starts_ends, labels)

# Plot the matrix
def plot_matrix(ax, matrix, title):
    ax.axis("off")
    table = ax.table(cellText=matrix, loc="center", cellLoc="center")
    color_map = {
        "A1": 'red', "A2": 'red', "A": 'pink',
        "B1": 'green', "B2": 'green', "B": 'lightgreen',
        "C1": 'blue', "C2": 'blue', "C": 'lightblue'
    }
    for cell in table._cells:
        text = table._cells[cell].get_text().get_text()
        if text in color_map:
            table._cells[cell].set_facecolor(color_map[text])
    ax.set_title(title)

# Visualize
fig, ax = plt.subplots(figsize=(6, 6))
plot_matrix(ax, matrix, "Max Coverage Paths")
plt.show()

# Print the final matrix with arrows
for i, row in enumerate(matrix):
    row_output = []
    for j, cell in enumerate(row):
        if (i, j) in directions:
            arrow = directions[(i, j)]
            row_output.append(arrow)
        else:
            row_output.append(cell)
    print(" ".join(row_output))
