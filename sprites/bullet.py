import pygame
from config import HEIGHT, BULLET_SIZE, BULLET_COLOR, BULLET_SPEED


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface(BULLET_SIZE)
        self.image.fill(BULLET_COLOR)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y += self.speed

        # ถ้าหลุดจอบน ให้ลบตัวเอง
        if self.rect.bottom < 0:
            self.kill()
