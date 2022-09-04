# pylint: disable=no-member

import sys
import pygame

pygame.init()

width, height = 720, 720
pygame.display.set_caption("Checker AI")
screen = pygame.display.set_mode((width, height))
CELL_SIZE = width // 8

background = pygame.Surface((width, height))

for file in range(8):
    for rank in range(8):
        is_light = (file + rank) % 2 == 0
        color = pygame.Color("#FFFFFF") if is_light else pygame.Color("#183037")
        pygame.draw.rect(
            background,
            color,
            (file * CELL_SIZE, rank * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

clock = pygame.time.Clock()

while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
