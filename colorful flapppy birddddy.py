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
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game settings
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 250  # Start with a wider gap
PIPE_WIDTH = 70
PIPE_SPEED = 3

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Draw background with hills and terrains
def draw_background():
    screen.fill(BLUE)
    pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))  # Ground
    for i in range(0, SCREEN_WIDTH, 100):
        pygame.draw.polygon(screen, GREEN, [(i, SCREEN_HEIGHT - 100), (i + 50, SCREEN_HEIGHT - 150), (i + 100, SCREEN_HEIGHT - 100)])  # Hills

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.width = 30
        self.height = 30
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        # Draw bird body
        pygame.draw.circle(screen, YELLOW, (self.x + self.width // 2, self.y + self.height // 2), 15)
        # Draw bird beak
        pygame.draw.polygon(screen, ORANGE, [(self.x + 20, self.y + 15), (self.x + 30, self.y + 10), (self.x + 30, self.y + 20)])
        # Draw bird eye
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 10), 3)
        # Draw bird wings
        pygame.draw.polygon(screen, YELLOW, [(self.x + 5, self.y + 15), (self.x, self.y + 25), (self.x + 10, self.y + 25)])

# Pipe class
class Pipe:
    def __init__(self, x, gap):
        self.x = x
        self.top_height = random.randint(50, SCREEN_HEIGHT - gap - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - gap
        self.gap = gap

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, GREEN, (self.x, SCREEN_HEIGHT - self.bottom_height, PIPE_WIDTH, self.bottom_height))

    def collide(self, bird):
        if bird.x + bird.width > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.top_height or bird.y + bird.height > SCREEN_HEIGHT - self.bottom_height:
                return True
        return False

# Main game function
def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 200, PIPE_GAP) for i in range(3)]
    score = 0
    running = True
    difficulty_increment = 0.002  # Slower difficulty increase

    while running:
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        # Update bird
        bird.update()
        if bird.y < 0 or bird.y + bird.height > SCREEN_HEIGHT:
            running = False

        # Update pipes
        for pipe in pipes:
            pipe.update()
            if pipe.collide(bird):
                running = False

        # Recycle pipes and update score
        if pipes[0].x + PIPE_WIDTH < 0:
            pipes.pop(0)
            new_gap = max(200, PIPE_GAP - int(score * difficulty_increment * 10))  # Ensure a minimum gap
            pipes.append(Pipe(SCREEN_WIDTH, new_gap))
            score += 1

        # Gradually increase pipe speed and gravity
        global PIPE_SPEED, GRAVITY
        PIPE_SPEED = 3 + (score * difficulty_increment * 0.3)
        GRAVITY = 0.5 + (score * difficulty_increment * 0.01)

        # Draw everything
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Display score
        font = pygame.font.SysFont(None, 48)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()
    pygame.time.wait(3000)

# Run the game
if __name__ == "__main__":
    main()
