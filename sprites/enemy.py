import pygame
import random
from pathlib import Path
from config import (
    WIDTH,
    HEIGHT,
    ENEMY_SPEED_MIN,
    ENEMY_SPEED_MAX,
    ENEMY_SPAWN_Y_RANGE,
    ENEMY_SIZE,
    ENEMY_FALLBACK_SIZE,
    ENEMY2_SIZE,
    ENEMY1_IMAGES,
    ENEMY2_IMAGES,
)
from utils.assets import load_first_image


class Enemy(pygame.sprite.Sprite):
    _CACHED_IMAGE = None

    def __init__(self, base_speed=0, image_candidates=None, use_alt_size=False):
        super().__init__()

        self.use_alt_size = use_alt_size

        if image_candidates:
            self.image = self._load_enemy_image(image_candidates)
        else:
            if Enemy._CACHED_IMAGE is None:
                Enemy._CACHED_IMAGE = self._load_enemy_image(ENEMY1_IMAGES)
            self.image = Enemy._CACHED_IMAGE

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(ENEMY_SPAWN_Y_RANGE[0], ENEMY_SPAWN_Y_RANGE[1])

        # 🔥 ความเร็ว = สุ่ม + ความยากจากคะแนน
        self.base_speed = base_speed
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX) + self.base_speed

    def _load_enemy_image(self, image_candidates=None):
        paths = image_candidates or ENEMY1_IMAGES
        target_size = ENEMY2_SIZE if self.use_alt_size else ENEMY_SIZE
        image = load_first_image(paths, size=target_size, convert_alpha=True)
        if image:
            image = self._remove_background(image)
            return image.convert_alpha()

        fallback = pygame.Surface(ENEMY_FALLBACK_SIZE, pygame.SRCALPHA)
        fallback.fill((255, 0, 0))
        return fallback

    def _remove_background(self, image, tolerance=80):
        """ลบพื้นหลังและครอบเฉพาะตัวศัตรู เพื่อลดขอบเทา"""
        width, height = image.get_size()
        border_pixels = []
        for x in range(width):
            border_pixels.append(image.get_at((x, 0)))
            border_pixels.append(image.get_at((x, height - 1)))
        for y in range(height):
            border_pixels.append(image.get_at((0, y)))
            border_pixels.append(image.get_at((width - 1, y)))

        if not border_pixels:
            return image

        border_tuples = [ (p.r, p.g, p.b, p.a) for p in border_pixels ]
        bg_tuple = max(set(border_tuples), key=border_tuples.count)
        bg = pygame.Color(*bg_tuple)

        for y in range(height):
            for x in range(width):
                pixel = image.get_at((x, y))
                if (
                    abs(pixel.r - bg.r) <= tolerance
                    and abs(pixel.g - bg.g) <= tolerance
                    and abs(pixel.b - bg.b) <= tolerance
                ):
                    image.set_at((x, y), (pixel.r, pixel.g, pixel.b, 0))

        mask = pygame.mask.from_surface(image)
        rects = mask.get_bounding_rects()
        if rects:
            box = rects[0]
            cropped = image.subsurface(box).copy()
            return cropped
        return image

    def set_image(self, image_surface):
        """อัปเดตรูป enemy ปัจจุบัน"""
        center = self.rect.center
        self.image = image_surface
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(ENEMY_SPAWN_Y_RANGE[0], ENEMY_SPAWN_Y_RANGE[1])
            self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX) + self.base_speed
