import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sailboat Adventure: Escape the Kraken")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
RED = (255, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.Font(None, 36)

# Load images
background_img = pygame.image.load("sea_background.png")  # Light blue sea background
sailboat_img = pygame.image.load("sailboat.png")  # Placeholder sailboat image
kraken_img = pygame.image.load("kraken.png")  # Placeholder kraken image
treasure_img = pygame.image.load("treasure.png")  # Placeholder treasure image
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
sailboat_img = pygame.transform.scale(sailboat_img, (60, 60))
kraken_img = pygame.transform.scale(kraken_img, (100, 100))
treasure_img = pygame.transform.scale(treasure_img, (40, 40))

# Game Variables
sailboat_x, sailboat_y = WIDTH // 2, HEIGHT // 2
sailboat_speed = 8  # Increased speed for the sailboat

kraken_x, kraken_y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
kraken_speed = 1.2  # Reduced speed for the Kraken

# Generate treasures dynamically based on player's movement
treasures = []

score = 0
fuel = 150  # Increased initial fuel

# Functions
def display_text(text, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Function to spawn treasures at random positions
def spawn_treasure():
    return pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 40, 40)

# Main game loop
def main():
    global sailboat_x, sailboat_y, kraken_x, kraken_y, fuel, score, treasures
    running = True

    while running:
        screen.blit(background_img, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and sailboat_x > 0:
            sailboat_x -= sailboat_speed
        if keys[pygame.K_RIGHT] and sailboat_x < WIDTH - 60:
            sailboat_x += sailboat_speed
        if keys[pygame.K_UP] and sailboat_y > 0:
            sailboat_y -= sailboat_speed
        if keys[pygame.K_DOWN] and sailboat_y < HEIGHT - 60:
            sailboat_y += sailboat_speed

        # Decrease fuel
        fuel -= 0.03  # Slower fuel depletion
        if fuel <= 0:
            display_text("Out of fuel! Game Over!", RED, WIDTH // 2 - 100, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        # Kraken follows the sailboat more slowly
        if kraken_x < sailboat_x:
            kraken_x += kraken_speed
        if kraken_x > sailboat_x:
            kraken_x -= kraken_speed
        if kraken_y < sailboat_y:
            kraken_y += kraken_speed
        if kraken_y > sailboat_y:
            kraken_y -= kraken_speed

        # Check for collision with Kraken
        if pygame.Rect(kraken_x, kraken_y, 100, 100).colliderect(pygame.Rect(sailboat_x, sailboat_y, 60, 60)):
            display_text("Caught by the Kraken! Game Over!", RED, WIDTH // 2 - 150, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        # Collect treasures
        for treasure in treasures[:]:
            if pygame.Rect(sailboat_x, sailboat_y, 60, 60).colliderect(treasure):
                treasures.remove(treasure)
                score += 10
                fuel += 25  # Gain more fuel when collecting treasures

        # Spawn new treasures dynamically as the player moves
        if len(treasures) < 10:  # Ensure there's always 10 treasures
            treasures.append(spawn_treasure())

        # Draw treasures
        for treasure in treasures:
            screen.blit(treasure_img, treasure)

        # Draw sailboat
        screen.blit(sailboat_img, (sailboat_x, sailboat_y))

        # Draw Kraken
        screen.blit(kraken_img, (kraken_x, kraken_y))

        # Display stats
        display_text(f"Score: {score}", WHITE, 10, 10)
        display_text(f"Fuel: {int(fuel)}", WHITE, 10, 40)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
