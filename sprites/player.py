import pygame
from pathlib import Path
from collections import deque
from config import WIDTH, HEIGHT
from sprites.base import SpaceObject
from sprites.weapon import Weapon


class Player(SpaceObject):
    """Player spaceship using composition (Weapon) and inheritance (SpaceObject)."""

    def __init__(self, bullet_group, all_sprites, sound_manager=None):
        image = self._load_player_image()
        super().__init__(image)

        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20

        self.speed = 6
        self.weapon = Weapon(bullet_group, all_sprites, cooldown_ms=250, sound_manager=sound_manager)

    def _load_player_image(self):
        image_candidates = [
            Path("assets/player.png"),
            Path("assets/player.webp"),
            Path("player.png/Spaceship-2D-Game-Sprites2.webp"),
        ]
        target_size = (60, 60)

        for image_path in image_candidates:
            if image_path.exists():
                try:
                    image = pygame.image.load(str(image_path)).convert_alpha()
                    image = self._remove_background(image)
                    return pygame.transform.smoothscale(image, target_size)
                except pygame.error:
                    pass

        fallback = pygame.Surface((50, 40), pygame.SRCALPHA)
        fallback.fill((0, 255, 0))
        return fallback

    def _remove_background(self, image):
        """Remove flat background, keep only the main sprite, and crop bounds."""
        background = image.get_at((0, 0))
        threshold = 24
        width, height = image.get_size()

        opaque = [[False for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                pixel = image.get_at((x, y))
                if self._is_background(pixel, background, threshold):
                    image.set_at((x, y), (pixel.r, pixel.g, pixel.b, 0))
                else:
                    opaque[y][x] = pixel.a > 0

        component = self._largest_component(opaque, width, height)
        if component:
            min_x = min(x for x, _ in component)
            min_y = min(y for _, y in component)
            max_x = max(x for x, _ in component)
            max_y = max(y for _, y in component)
            result = pygame.Surface((max_x - min_x + 1, max_y - min_y + 1), pygame.SRCALPHA)
            for x, y in component:
                result.set_at((x - min_x, y - min_y), image.get_at((x, y)))
            return result
        return image

    def _is_background(self, pixel, background, threshold):
        return (
            abs(pixel.r - background.r) <= threshold
            and abs(pixel.g - background.g) <= threshold
            and abs(pixel.b - background.b) <= threshold
        )

    def _largest_component(self, opaque, width, height):
        visited = [[False for _ in range(width)] for _ in range(height)]
        best_component = []
        directions = (
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),            (1, 0),
            (-1, 1),  (0, 1),   (1, 1),
        )

        for y in range(height):
            for x in range(width):
                if visited[y][x] or not opaque[y][x]:
                    continue

                queue = deque([(x, y)])
                visited[y][x] = True
                current = []

                while queue:
                    cx, cy = queue.popleft()
                    current.append((cx, cy))
                    for dx, dy in directions:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if not visited[ny][nx] and opaque[ny][nx]:
                                visited[ny][nx] = True
                                queue.append((nx, ny))

                if len(current) > len(best_component):
                    best_component = current

        return best_component

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        self.weapon.fire((self.rect.centerx, self.rect.top))
