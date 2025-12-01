import pygame
import asyncio # Required for the web version

# Initialize Pygame
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_W, PADDLE_H = 15, 100
BALL_SIZE = 15

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Pong")
clock = pygame.time.Clock()

# --- Game Actors (Dictionaries are easier for students than Classes initially) ---
player = pygame.Rect(10, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
opponent = pygame.Rect(WIDTH - 25, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball Speed variables
ball_speed_x = 5
ball_speed_y = 5
player_speed = 0
opponent_speed = 5

score_player = 0
score_opponent = 0
font = pygame.font.Font(None, 74)

async def main():
    # We must declare these as global to modify them inside the function
    global ball_speed_x, ball_speed_y, player_speed, score_player, score_opponent

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Keyboard Input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed = -6
                if event.key == pygame.K_DOWN:
                    player_speed = 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_speed = 0

        # 2. Game Logic
        # Move Player
        player.y += player_speed
        
        # Keep player on screen
        if player.top < 0: player.top = 0
        if player.bottom > HEIGHT: player.bottom = HEIGHT

        # Move Opponent (Simple AI)
        if opponent.centery < ball.y:
            opponent.y += opponent_speed
        if opponent.centery > ball.y:
            opponent.y -= opponent_speed
        
        # Move Ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball Wall Collision (Top/Bottom)
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Ball Paddle Collision
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1

        # Scoring
        if ball.left <= 0:
            score_opponent += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= -1
        
        if ball.right >= WIDTH:
            score_player += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x *= -1

        # 3. Drawing
        screen.fill(BLACK)
        
        # Draw Net
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        
        # Draw Actors
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, WHITE, opponent)
        pygame.draw.ellipse(screen, WHITE, ball)
        
        # Draw Score
        player_text = font.render(str(score_player), True, WHITE)
        screen.blit(player_text, (WIDTH//2 - 50, 10))
        opponent_text = font.render(str(score_opponent), True, WHITE)
        screen.blit(opponent_text, (WIDTH//2 + 20, 10))

        # Update Display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
        
        # IMPORTANT: This line allows the browser to breathe!
        await asyncio.sleep(0)

# Run the game
asyncio.run(main())
