import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Balloon Rise Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Game Variables
balloon_radius = 30
balloon_x = screen_width // 2
balloon_y = screen_height - balloon_radius
balloon_speed = 5
balloon_velocity_y = -2

# Hurdle Variables
hurdle_width = 60
hurdle_height = 20
hurdles = []

# Game Font
font = pygame.font.SysFont("Arial", 30)

# Score
score = 0

# Game Loop
running = True
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get player input
    keys = pygame.key.get_pressed()

    # Move the balloon
    if keys[pygame.K_LEFT]:
        balloon_x -= 5
    if keys[pygame.K_RIGHT]:
        balloon_x += 5

    # Make sure the balloon stays within the screen boundaries
    if balloon_x - balloon_radius < 0:
        balloon_x = balloon_radius
    if balloon_x + balloon_radius > screen_width:
        balloon_x = screen_width - balloon_radius

    # Balloon rises continuously
    balloon_y += balloon_velocity_y
    if balloon_y - balloon_radius < 0:
        balloon_y = screen_height - balloon_radius
        score += 1  # Increase score when the balloon goes up

    # Generate hurdles
    if random.randint(1, 100) == 1:
        hurdle_x = random.randint(0, screen_width - hurdle_width)
        hurdle_y = random.randint(-500, -50)
        hurdles.append(pygame.Rect(hurdle_x, hurdle_y, hurdle_width, hurdle_height))

    # Move and draw hurdles
    for hurdle in hurdles:
        hurdle.y += 3  # Hurdle speed
        pygame.draw.rect(screen, RED, hurdle)
        if hurdle.y > screen_height:  # Remove hurdle when it goes off screen
            hurdles.remove(hurdle)
        # Check for collisions
        if hurdle.colliderect(pygame.Rect(balloon_x - balloon_radius, balloon_y - balloon_radius, balloon_radius * 2, balloon_radius * 2)):
            running = False  # End the game if balloon collides with a hurdle

    # Draw the balloon
    pygame.draw.circle(screen, BLUE, (balloon_x, balloon_y), balloon_radius)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
