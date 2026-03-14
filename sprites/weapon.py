import pygame
from sprites.bullet import Bullet


class Weapon:
    """Composable weapon that owns bullet spawning & cooldown logic.

    Encapsulation: firing state lives here, not in Player.
    Dependency Inversion: Game objects depend on this abstraction, not on
    concrete bullet creation scattered around the codebase.
    """

    def __init__(self, bullet_group: pygame.sprite.Group, all_sprites: pygame.sprite.Group, cooldown_ms: int = 250, sound_manager=None):
        self._bullet_group = bullet_group
        self._all_sprites = all_sprites
        self._cooldown_ms = cooldown_ms
        self._last_shot_at = 0
        self._sound_manager = sound_manager

    def fire(self, origin: tuple[int, int]):
        now = pygame.time.get_ticks()
        if now - self._last_shot_at < self._cooldown_ms:
            return None

        self._last_shot_at = now
        bullet = Bullet(*origin)
        self._bullet_group.add(bullet)
        self._all_sprites.add(bullet)
        if self._sound_manager:
            self._sound_manager.play_shoot()
        return bullet

    @property
    def cooldown_ms(self) -> int:
        return self._cooldown_ms

    @cooldown_ms.setter
    def cooldown_ms(self, value: int):
        # Encapsulation with validation example
        self._cooldown_ms = max(0, value)
