import math
from random import choice, randint

import pygame
from settings import BOARD_SIZE, BOARD_OFFSET


class Sparks:
    """A small spark in the fireworks"""

    COLORS = [
        pygame.Color("#FF0000"),
        pygame.Color("#00FF47"),
        pygame.Color("#1400FF"),
        pygame.Color("#EBFF00"),
        pygame.Color("#00D1FF"),
        pygame.Color("#FA00FF"),
    ]

    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.direction = math.radians(randint(0, 360))
        self.speed = randint(2, 7)
        self.radius = randint(1, 5)

        self.surface = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surface.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surface, choice(self.COLORS), (5, 5), 5)

        self.alpha = 255

    def update(self):
        self.position.x += math.cos(self.direction) * self.speed
        self.position.y += math.sin(self.direction) * self.speed
        self.speed -= 0.02

    def render(self, screen):
        screen.blit(
            self.surface, (self.position.x - self.radius, self.position.y - self.radius)
        )
        self.surface.set_alpha(self.alpha)
        self.alpha -= randint(8, 15)


class SparksContainer:
    """The sparks container"""

    def __init__(self):
        self.sparks = []
        self.to_fire = []

    def create_new_firework(self):
        """Creates a new firework"""
        position = [
            BOARD_OFFSET
            + (BOARD_SIZE / 2)
            + randint(-int(BOARD_SIZE / 2), int(BOARD_SIZE / 2)),
            BOARD_OFFSET
            + (BOARD_SIZE / 2)
            + randint(-int(BOARD_SIZE / 2), int(BOARD_SIZE / 2)),
        ]
        for _ in range(randint(15, 30)):
            self.to_fire.append(
                [Sparks(*position), pygame.time.get_ticks(), randint(100, 300)]
            )

    def update(self, screen):
        """Updates & Renders all the spark

        Args:
            screen: the pygame screen
        """
        to_remove = []

        for i, spark in enumerate(self.sparks):
            spark.render(screen)
            spark.update()

            if spark.alpha <= 0:
                to_remove.append(i)

        for i, index in enumerate(to_remove):
            self.sparks.pop(index - i)

        to_remove.clear()

        for i, (spark, timer, wait_time) in enumerate(self.to_fire):
            if pygame.time.get_ticks() - timer > wait_time:
                self.sparks.append(spark)
                to_remove.append(i)

        for i, index in enumerate(to_remove):
            self.to_fire.pop(index - i)
