import pygame
import math
from pathlib import Path
from config import (
    WIDTH,
    HEIGHT,
    PLAYER_SPEED,
    PLAYER_BOTTOM_OFFSET,
    PLAYER_SHOOT_DELAY_MS,
    PLAYER_SIZE,
    PLAYER_FALLBACK_SIZE,
)
from sprites.bullet import Bullet

class Player(pygame.sprite.Sprite):
    _CACHED_IMAGE = None
    _SHOOT_SOUND = None

    def __init__(self, bullet_group, all_sprites):
        super().__init__()

        if Player._CACHED_IMAGE is None:
            Player._CACHED_IMAGE = self._load_player_image()
        self.image = Player._CACHED_IMAGE

        if Player._SHOOT_SOUND is None:
            Player._SHOOT_SOUND = self._load_shoot_sound()

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - PLAYER_BOTTOM_OFFSET

        self.speed = PLAYER_SPEED
        self.shoot_delay = PLAYER_SHOOT_DELAY_MS  # มิลลิวินาที
        self.last_shot = 0

        self.bullet_group = bullet_group# จะถูกตั้งค่าใน GameScene
        self.all_sprites = all_sprites# จะถูกตั้งค่าใน GameScene

    def _load_player_image(self):
        image_candidates = [
            Path("assets/player.png"),
            Path("assets/player.webp"),
            Path("player.png/ChatGPT Image 14 มี.ค. 2569 15_36_37.png"),
            Path("player.png/Spaceship-2D-Game-Sprites2.webp"),
        ]
        target_size = PLAYER_SIZE

        for image_path in image_candidates:
            if image_path.exists():
                try:
                    raw = pygame.image.load(str(image_path)).convert_alpha()
                    image = pygame.transform.smoothscale(raw, target_size)
                    return image
                except pygame.error:
                    pass

        fallback = pygame.Surface(PLAYER_FALLBACK_SIZE, pygame.SRCALPHA)
        fallback.fill((0, 255, 0))
        return fallback

    def _load_shoot_sound(self):
        candidates = [
            Path("laser.wav"),
            Path("assets/laser.wav"),
            Path("assets/sounds/laser.wav"),
            Path("assets/sounds/shoot.wav"),
            Path("assets/sounds/shoot.ogg"),
            Path("assets/shoot.wav"),
            Path("assets/shoot.ogg"),
        ]
        for path in candidates:
            if path.exists():
                try:
                    return pygame.mixer.Sound(str(path))
                except pygame.error:
                    continue
        return self._generate_beep()

    def _generate_beep(self, freq=660, duration=0.12, volume=0.28):
        """โทนยิงใหม่ นุ่มกว่า: sine หลัก + overtone เบา ๆ"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            base = math.sin(2 * math.pi * freq * t)
            overtone = 0.4 * math.sin(2 * math.pi * freq * 1.5 * t)
            env = 1.0 - (t / duration)  # fade out
            sample = int(volume * env * 30000 * (base + overtone))
            buf += sample.to_bytes(2, byteorder="little", signed=True)
        return pygame.mixer.Sound(buffer=bytes(buf))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

        # กันออกนอกจอ
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullet_group.add(bullet)  # เพิ่มกระสุนเข้าไปในกลุ่ม bullets ของ Player
            self.all_sprites.add(bullet)  # เพิ่มกระสุนเข้าไปในกลุ่ม all_sprites ของ GameScene
            if Player._SHOOT_SOUND:
                Player._SHOOT_SOUND.play()
