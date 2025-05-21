import pygame
import random
import sys

# Inicializácia pygame
pygame.init()

# Nastavenia okna
SIZE = 20  # veľkosť štvorčeka
GRID_WIDTH = 25
GRID_HEIGHT = 25
WIDTH = GRID_WIDTH * SIZE
HEIGHT = GRID_HEIGHT * SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hadík')

clock = pygame.time.Clock()

# Farby
GREEN = (0, 200, 0)
DARKGREEN = (0, 100, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Funkcia na vykreslenie hada a potravy
def draw_rect(color, pos):
    pygame.draw.rect(screen, color, (pos[0]*SIZE, pos[1]*SIZE, SIZE, SIZE))

# Hlavná funkcia hry
def game():
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (1, 0)  # začína vpravo
    food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    score = 0

    running = True
    while running:
        screen.fill((150, 255, 150))  # pozadie

        # Ovládanie
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_r:
                    game()  # reštart hry

        # Posun hada
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        # Kontrola kolízie s jedlom
        if head == food:
            score += 1
            while True:
                food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                if food not in snake:
                    break
        else:
            snake.pop()  # ak neje potravu, skráti sa

        # Kontrola kolízie s okrajom alebo so sebou
        if (
            head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT or
            head in snake[1:]
        ):
            font = pygame.font.SysFont(None, 50)
            text = font.render("Koniec! Skóre: {} | Stlač R pre reštart".format(score), True, BLACK)
            screen.blit(text, (20, HEIGHT//2 - 30))
            pygame.display.flip()
            # Čakaj na R alebo zavretie okna
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return game()  # reštart

        # Vykreslenie potravy
        draw_rect(RED, food)
        # Vykreslenie hada
        for i, pos in enumerate(snake):
            draw_rect(DARKGREEN if i == 0 else GREEN, pos)

        # Skóre
        font = pygame.font.SysFont(None, 30)
        score_text = font.render("Skóre: {}".format(score), True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)  # rýchlosť hada

# Spustenie hry
game()
