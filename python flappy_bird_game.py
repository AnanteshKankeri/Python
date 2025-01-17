import pygame
from PIL import Image, ImageOps
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)  # Black background for contrast
FPS = 60
BIRD_SIZE = (50, 50)  # Updated bird size (larger for better visibility)
BIRD_POS = [WIDTH // 4, HEIGHT // 2]  # Initial position of the bird
PIPE_WIDTH = 70  # Standard pipe width
PIPE_GAP = 200  # Increased gap between the top and bottom pipes
PIPE_COLOR = (255, 0, 0)  # Red pipes
PIPE_VELOCITY = 5  # Speed of pipe movement

# Create a Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Negative Flappy Bird")

# Load the realistic bird image
bird_image = Image.open("A_realistic_image_of_a_bird_in_flight,_with_vivid_.png")
negative_bird = ImageOps.invert(bird_image.convert("RGB"))
negative_bird.save("negative_realistic_bird.png")

# Resize the bird to the new size (50x50)
negative_bird_resized = negative_bird.resize(BIRD_SIZE)
negative_bird_resized.save("negative_resized_realistic_bird.png")

# Load the resized negative bird image into Pygame
bird_surface = pygame.image.load("negative_resized_realistic_bird.png")
bird_rect = bird_surface.get_rect(center=(BIRD_POS[0], BIRD_POS[1]))

# Pipe class to manage obstacles
class Pipe:
    def __init__(self):
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.top_rect = pygame.Rect(WIDTH, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(WIDTH, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - (self.height + PIPE_GAP))

    def move(self):
        self.top_rect.x -= PIPE_VELOCITY
        self.bottom_rect.x -= PIPE_VELOCITY

    def draw(self, surface):
        pygame.draw.rect(surface, PIPE_COLOR, self.top_rect)
        pygame.draw.rect(surface, PIPE_COLOR, self.bottom_rect)

    def off_screen(self):
        return self.top_rect.x < -PIPE_WIDTH

    def collide(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)

# Bird movement
bird_velocity_y = 0
gravity = 0.5
flap_strength = -10

clock = pygame.time.Clock()
pipes = [Pipe()]  # List to hold pipes
score = 0

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity_y = flap_strength

    # Apply gravity to the bird
    bird_velocity_y += gravity
    BIRD_POS[1] += bird_velocity_y
    bird_rect.y = BIRD_POS[1]

    # Check for boundary collision (top and bottom)
    if BIRD_POS[1] > HEIGHT - BIRD_SIZE[1]:
        BIRD_POS[1] = HEIGHT - BIRD_SIZE[1]
        bird_velocity_y = 0
    elif BIRD_POS[1] < 0:
        BIRD_POS[1] = 0
        bird_velocity_y = 0

    # Draw the bird
    screen.blit(bird_surface, bird_rect)

    # Manage pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw(screen)

        # Check if pipe is off the screen, remove it
        if pipe.off_screen():
            pipes.remove(pipe)
            pipes.append(Pipe())  # Add new pipe
            score += 1  # Increment score

        # Check for collision with the bird
        if pipe.collide(bird_rect):
            running = False  # End game on collision

    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
