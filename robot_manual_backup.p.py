
import pygame
import sys

pygame.init()

# Window settings
WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MegaMinds - Robot Obstacle Avoidance")

clock = pygame.time.Clock()

# Colors
WHITE = (245, 245, 245)
BLUE = (40, 120, 255)
GREEN = (0, 200, 100)
RED = (230, 60, 60)
BLACK = (30, 30, 30)
GRAY = (120, 120, 120)

# Robot
robot_x = 60
robot_y = 60
robot_radius = 12
speed = 4

# Goal
goal_x = 830
goal_y = 530
goal_radius = 16

# Obstacles: x, y, width, height
obstacles = [
    pygame.Rect(180, 80, 40, 250),
    pygame.Rect(320, 200, 250, 40),
    pygame.Rect(450, 320, 40, 180),
    pygame.Rect(650, 100, 40, 250),
    pygame.Rect(200, 430, 180, 40),
]

font = pygame.font.SysFont(None, 32)
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Calculate proposed movement
    dx = 0
    dy = 0

    if keys[pygame.K_LEFT]:
        dx = -speed
    if keys[pygame.K_RIGHT]:
        dx = speed
    if keys[pygame.K_UP]:
        dy = -speed
    if keys[pygame.K_DOWN]:
        dy = speed

    # Move horizontally, then check collisions
    new_x = robot_x + dx
    robot_rect = pygame.Rect(
        new_x - robot_radius,
        robot_y - robot_radius,
        robot_radius * 2,
        robot_radius * 2
    )

    if (
        robot_rect.left >= 0
        and robot_rect.right <= WIDTH
        and not any(robot_rect.colliderect(o) for o in obstacles)
    ):
        robot_x = new_x

    # Move vertically, then check collisions
    new_y = robot_y + dy
    robot_rect = pygame.Rect(
        robot_x - robot_radius,
        new_y - robot_radius,
        robot_radius * 2,
        robot_radius * 2
    )

    if (
        robot_rect.top >= 0
        and robot_rect.bottom <= HEIGHT
        and not any(robot_rect.colliderect(o) for o in obstacles)
    ):
        robot_y = new_y

    # Draw arena
    screen.fill(WHITE)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, GRAY, obstacle)

    # Draw goal
    pygame.draw.circle(
        screen, GREEN, (goal_x, goal_y), goal_radius
    )

    # Draw robot
    pygame.draw.circle(
        screen, BLUE, (robot_x, robot_y), robot_radius
    )

    # Check whether robot reaches goal
    distance = (
        (robot_x - goal_x) ** 2
        + (robot_y - goal_y) ** 2
    ) ** 0.5

    if distance < robot_radius + goal_radius:
        message = font.render(
            "GOAL REACHED!", True, GREEN
        )
        screen.blit(message, (350, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
