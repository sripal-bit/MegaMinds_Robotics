
import pygame
import heapq
import math
import time

pygame.init()

# ---------------- SETTINGS ----------------
CELL = 30
COLS, ROWS = 28, 17
LEFT, TOP = 30, 90

WIDTH = LEFT * 2 + COLS * CELL
HEIGHT = TOP + ROWS * CELL + 45

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MegaMinds - Autonomous A* Robot")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 17)

WHITE = (245, 245, 245)
BLACK = (25, 30, 40)
BLUE = (40, 120, 255)
GREEN = (0, 190, 100)
RED = (225, 60, 60)
GRAY = (120, 125, 135)
GRID = (215, 220, 230)
CYAN = (35, 150, 190)

START = (1, 1)
GOAL = (26, 15)
SPEED = 150

# Each tuple describes a rectangular group of blocked grid cells.
obstacles = set()

def add_wall(x1, y1, x2, y2):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            obstacles.add((x, y))

add_wall(5, 0, 5, 10)
add_wall(5, 12, 5, 16)
add_wall(9, 3, 15, 3)
add_wall(9, 4, 9, 10)
add_wall(12, 6, 19, 6)
add_wall(15, 7, 15, 13)
add_wall(20, 2, 20, 10)
add_wall(22, 11, 26, 11)
add_wall(2, 13, 10, 13)

# Open passages through selected walls.
for gap in [(5, 11), (9, 2), (16, 6),
            (20, 11), (15, 14), (7, 13)]:
    obstacles.discard(gap)


def center(cell):
    x, y = cell
    return (LEFT + x * CELL + CELL / 2,
            TOP + y * CELL + CELL / 2)


def free(cell):
    x, y = cell
    return (0 <= x < COLS and 0 <= y < ROWS
            and cell not in obstacles)


def heuristic(a, b):
    # Manhattan distance: only horizontal/vertical moves are allowed.
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal):
    """Return a shortest path as a list of grid cells."""
    if not free(start) or not free(goal):
        return []

    # Priority queue items: (estimated total cost, cost so far, cell)
    queue = [(heuristic(start, goal), 0, start)]
    parent = {}
    cost = {start: 0}
    visited = set()

    while queue:
        _, current_cost, current = heapq.heappop(queue)

        if current in visited:
            continue

        if current == goal:
            path = [current]
            while current in parent:
                current = parent[current]
                path.append(current)
            return path[::-1]

        visited.add(current)
        x, y = current

        for nxt in [(x + 1, y), (x - 1, y),
                    (x, y + 1), (x, y - 1)]:
            if not free(nxt):
                continue

            new_cost = current_cost + 1
            if new_cost < cost.get(nxt, float("inf")):
                cost[nxt] = new_cost
                parent[nxt] = current
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(
                    queue, (priority, new_cost, nxt)
                )

    return []


def reset():
    global cell, rx, ry, path, path_index
    global distance, collisions, started, finished

    cell = START
    rx, ry = center(START)
    path = astar(START, GOAL)
    path_index = 1
    distance = 0.0
    collisions = 0
    started = time.perf_counter()
    finished = False


reset()
autonomous = True
message = "A* route planned"

running = True
while running:
    dt = min(clock.tick(60) / 1000, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                reset()
                message = "Simulation restarted"

            elif event.key == pygame.K_SPACE:
                autonomous = not autonomous
                if autonomous:
                    path = astar(cell, GOAL)
                    path_index = 1
                    message = "Autonomous mode"
                else:
                    message = "Manual mode: arrow keys"

            elif not autonomous and not finished:
                directions = {
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0, 1)
                }

                if event.key in directions:
                    dx, dy = directions[event.key]
                    nxt = (cell[0] + dx, cell[1] + dy)

                    if free(nxt):
                        cell = nxt
                        rx, ry = center(cell)
                        distance += CELL
                    else:
                        collisions += 1
                        message = "Blocked move"

                    if cell == GOAL:
                        finished = True

    # ---------------- AUTONOMOUS MOVEMENT ----------------
    if autonomous and not finished and path:
        if path_index < len(path):
            next_cell = path[path_index]
            tx, ty = center(next_cell)

            dx = tx - rx
            dy = ty - ry
            remaining = math.hypot(dx, dy)
            step = SPEED * dt

            if remaining <= step:
                distance += remaining
                rx, ry = tx, ty
                cell = next_cell
                path_index += 1
            elif remaining > 0:
                mx = dx / remaining * step
                my = dy / remaining * step
                rx += mx
                ry += my
                distance += math.hypot(mx, my)

        if cell == GOAL:
            finished = True
            message = "GOAL REACHED!"

    # ---------------- DRAW ARENA ----------------
    screen.fill(WHITE)
    pygame.draw.rect(
        screen, BLACK,
        (0, 0, WIDTH, 70)
    )

    title = font.render(
        "MEGAMINDS ROBOT | A* PATHFINDING", True, WHITE
    )
    screen.blit(title, (20, 15))

    mode = "AUTONOMOUS" if autonomous else "MANUAL"
    info = font.render(
        f"{mode} | SPACE: mode | R: restart | ESC: quit",
        True, WHITE
    )
    screen.blit(info, (20, 42))

    arena = pygame.Rect(
        LEFT, TOP, COLS * CELL, ROWS * CELL
    )
    pygame.draw.rect(screen, (250, 251, 253), arena)

    # Grid lines
    for x in range(COLS + 1):
        px = LEFT + x * CELL
        pygame.draw.line(
            screen, GRID, (px, TOP), (px, TOP + ROWS * CELL)
        )

    for y in range(ROWS + 1):
        py = TOP + y * CELL
        pygame.draw.line(
            screen, GRID, (LEFT, py), (LEFT + COLS * CELL, py)
        )

    # Draw the planned route.
    if path and autonomous:
        points = [center(p) for p in path[path_index - 1:]]
        if len(points) > 1:
            pygame.draw.lines(screen, CYAN, False, points, 4)

    # Draw obstacles.
    for x, y in obstacles:
        rect = pygame.Rect(
            LEFT + x * CELL + 2,
            TOP + y * CELL + 2,
            CELL - 4, CELL - 4
        )
        pygame.draw.rect(screen, GRAY, rect, border_radius=3)

    # Start and goal
    sx, sy = center(START)
    gx, gy = center(GOAL)

    pygame.draw.circle(screen, GREEN, (int(sx), int(sy)), 10)
    pygame.draw.circle(screen, RED, (int(gx), int(gy)), 11)

    # Robot and a visual range indicator
    pygame.draw.circle(screen, (190, 225, 245),
                       (int(rx), int(ry)), 40, 1)
    pygame.draw.circle(screen, BLUE, (int(rx), int(ry)), 11)
    pygame.draw.circle(screen, WHITE, (int(rx), int(ry)), 11, 2)

    elapsed = time.perf_counter() - started
    if finished:
        message = "GOAL REACHED!"

    stats = (
        f"Time: {elapsed:.1f}s   "
        f"Distance: {distance / CELL:.1f} cells   "
        f"Blocked moves: {collisions}"
    )
    screen.blit(font.render(stats, True, BLACK),
                (LEFT, TOP + ROWS * CELL + 8))

    if finished:
        banner = font.render("GOAL REACHED! Press R to restart",
                             True, GREEN)
        screen.blit(banner, (WIDTH // 2 - 155, 73))

    pygame.display.flip()

pygame.quit()
