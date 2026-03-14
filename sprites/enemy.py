import random
from collections import deque
from pathlib import Path
import pygame
from config import WIDTH, HEIGHT
from sprites.base import SpaceObject


class BaseEnemy(SpaceObject):
    """Shared enemy behavior (inheritance) with overridable movement (polymorphism)."""

    def __init__(self, base_speed: int = 0):
        self.base_speed = base_speed
        image = self._load_enemy_image()
        super().__init__(image)
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)

    def _load_enemy_image(self):
        image_candidates = [
            Path("assets/enemy.png"),
            Path("assets/enemy.jpg"),
            Path("enemy.png/e10138041e8a5d17269b8d2fbbfe9736.jpg"),
        ]
        target_size = (50, 50)

        for image_path in image_candidates:
            if image_path.exists():
                try:
                    image = pygame.image.load(str(image_path)).convert_alpha()
                    image = self._remove_background(image)
                    return pygame.transform.smoothscale(image, target_size)
                except pygame.error:
                    pass

        fallback = pygame.Surface((40, 40), pygame.SRCALPHA)
        fallback.fill((255, 0, 0))
        return fallback

    def _remove_background(self, image):
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


class StraightEnemy(BaseEnemy):
    def __init__(self, base_speed: int = 0):
        super().__init__(base_speed)
        self._speed_y = random.randint(3, 7) + self.base_speed

    def update(self):
        self.rect.y += self._speed_y
        if self.rect.top > HEIGHT:
            self.reset_position()
            self._speed_y = random.randint(3, 7) + self.base_speed


class ZigZagEnemy(BaseEnemy):
    def __init__(self, base_speed: int = 0):
        super().__init__(base_speed)
        self._speed_y = random.randint(2, 5) + self.base_speed
        self._speed_x = random.choice([-2, 2])
        self._tick = 0

    def update(self):
        self._tick += 1
        self.rect.y += self._speed_y
        self.rect.x += self._speed_x

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self._speed_x *= -1

        if self._tick % 40 == 0:
            self._speed_x *= -1

        if self.rect.top > HEIGHT:
            self.reset_position()
            self._tick = 0


class EnemyFactory:
    """Open/Closed: add new enemy classes without changing consumers."""

    def __init__(self, enemy_types=None):
        self.enemy_types = enemy_types or (StraightEnemy, ZigZagEnemy)

    def create_enemy(self, difficulty: int = 0):
        enemy_cls = random.choice(self.enemy_types)
        return enemy_cls(base_speed=difficulty)
