import pygame
from config import HEIGHT
from sprites.base import SpaceObject


class Bullet(SpaceObject):
    """Simple upward bullet. Inherits SpaceObject to demonstrate inheritance."""

    def __init__(self, x: int, y: int):
        image = pygame.Surface((5, 15))
        image.fill((255, 255, 0))
        super().__init__(image)
        self.rect.centerx = x
        self.rect.bottom = y
        self._speed_y = -10  # Encapsulated speed for clarity

    def update(self):
        self.rect.y += self._speed_y

        # ถ้าหลุดจอบน ให้ลบตัวเอง
        if self.rect.bottom < 0:
            self.kill()
