import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Rocket dimensions
ROCKET_WIDTH, ROCKET_HEIGHT = 50, 70

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Rocket Game")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load images
rocket_image = pygame.image.load("rocket.png")  # Placeholder for rocket image
rocket_image = pygame.transform.scale(rocket_image, (ROCKET_WIDTH, ROCKET_HEIGHT))

stone_image = pygame.image.load("stone.png")  # Placeholder for obstacle image
stone_image = pygame.transform.scale(stone_image, (50, 50))

laser_image = pygame.image.load("laser.png")  # Placeholder for laser image
laser_image = pygame.transform.scale(laser_image, (10, 40))

xp_boost_image = pygame.image.load("xp_boost.png")  # Placeholder for XP boost image
xp_boost_image = pygame.transform.scale(xp_boost_image, (30, 30))

background = pygame.image.load("space_background.png")  # Placeholder for background image
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Game variables
rocket_x = WIDTH // 2 - ROCKET_WIDTH // 2
rocket_y = HEIGHT - ROCKET_HEIGHT - 20

obstacles = []
lasers = []
power_ups = []

obstacle_speed = 4
laser_speed = -8

score = 0
high_score = 0
frame_count = 0
running = True
paused = False
power_up_active = False
power_up_duration = 300  # Frames
power_up_timer = 0

# Functions
def create_obstacle():
    x = random.randint(0, WIDTH - 50)
    y = -50
    return pygame.Rect(x, y, 50, 50)

def create_laser():
    x = rocket_x + ROCKET_WIDTH // 2 - 5
    y = rocket_y
    return pygame.Rect(x, y, 10, 40)

def create_power_up():
    x = random.randint(0, WIDTH - 30)
    y = -30
    return pygame.Rect(x, y, 30, 30)

def move_obstacles():
    global score
    for obstacle in obstacles:
        obstacle.y += obstacle_speed
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)
            score += 1

def move_lasers():
    for laser in lasers:
        laser.y += laser_speed
        if laser.y < 0:
            lasers.remove(laser)

def move_power_ups():
    global power_up_active, power_up_timer
    for power_up in power_ups:
        power_up.y += obstacle_speed // 2
        if power_up.y > HEIGHT:
            power_ups.remove(power_up)
        elif pygame.Rect(rocket_x, rocket_y, ROCKET_WIDTH, ROCKET_HEIGHT).colliderect(power_up):
            power_ups.remove(power_up)
            power_up_active = True
            power_up_timer = power_up_duration

def check_collision():
    rocket_rect = pygame.Rect(rocket_x, rocket_y, ROCKET_WIDTH, ROCKET_HEIGHT)
    for obstacle in obstacles:
        if rocket_rect.colliderect(obstacle):
            return True
    return False

def check_laser_hits():
    global score
    for laser in lasers:
        for obstacle in obstacles:
            if laser.colliderect(obstacle):
                lasers.remove(laser)
                obstacles.remove(obstacle)
                score += 5
                return

def display_text(text, x, y, color=WHITE):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def reset_game():
    global rocket_x, rocket_y, obstacles, lasers, power_ups, score, power_up_active
    rocket_x = WIDTH // 2 - ROCKET_WIDTH // 2
    rocket_y = HEIGHT - ROCKET_HEIGHT - 20
    obstacles = []
    lasers = []
    power_ups = []
    score = 0
    power_up_active = False

# Game loop
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_SPACE:
                lasers.append(create_laser())

    if paused:
        display_text("Paused", WIDTH // 2 - 50, HEIGHT // 2, WHITE)
        pygame.display.flip()
        clock.tick(10)
        continue

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rocket_x > 0:
        rocket_x -= 5
    if keys[pygame.K_RIGHT] and rocket_x < WIDTH - ROCKET_WIDTH:
        rocket_x += 5

    # Add obstacles and power-ups periodically
    frame_count += 1
    if frame_count % 50 == 0:
        obstacles.append(create_obstacle())
    if frame_count % 300 == 0:
        power_ups.append(create_power_up())

    # Move entities
    move_obstacles()
    move_lasers()
    move_power_ups()

    # Check collisions
    if check_collision():
        if score > high_score:
            high_score = score
        reset_game()

    check_laser_hits()

    # Power-up management
    if power_up_active:
        obstacle_speed = 2
        power_up_timer -= 1
        if power_up_timer <= 0:
            power_up_active = False
            obstacle_speed = 4

    # Draw rocket
    screen.blit(rocket_image, (rocket_x, rocket_y))

    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(stone_image, (obstacle.x, obstacle.y))

    # Draw lasers
    for laser in lasers:
        screen.blit(laser_image, (laser.x, laser.y))

    # Draw power-ups
    for power_up in power_ups:
        screen.blit(xp_boost_image, (power_up.x, power_up.y))

    # Display score and high score
    display_text(f"Score: {score}", 10, 10)
    display_text(f"High Score: {high_score}", 10, 40)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
