import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 255, 0)

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Bird settings
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Pipe settings
PIPE_WIDTH = 60
PIPE_GAP = 150
pipe_velocity = -4
pipes = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def draw_bird():
    pygame.draw.rect(screen, BLACK, (bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT))

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe["top"])
        pygame.draw.rect(screen, GREEN, pipe["bottom"])

def create_pipe():
    height = random.randint(100, SCREEN_HEIGHT - 200)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP)
    return {"top": top_pipe, "bottom": bottom_pipe}

def move_pipes():
    for pipe in pipes:
        pipe["top"].x += pipe_velocity
        pipe["bottom"].x += pipe_velocity
    if pipes and pipes[0]["top"].right < 0:
        pipes.pop(0)

def check_collision():
    bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
    if bird_y < 0 or bird_y > SCREEN_HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            return True
    return False

def display_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Game loop
running = True
spawn_pipe_event = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_event, 1500)

while running:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = JUMP_STRENGTH
        if event.type == spawn_pipe_event:
            pipes.append(create_pipe())

    # Update bird position
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Move pipes
    move_pipes()

    # Check for collisions
    if check_collision():
        running = False

    # Update score
    for pipe in pipes:
        if pipe["top"].x + PIPE_WIDTH < bird_x and not pipe.get("scored", False):
            score += 1
            pipe["scored"] = True

    # Draw everything
    draw_bird()
    draw_pipes()
    display_score()

    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
