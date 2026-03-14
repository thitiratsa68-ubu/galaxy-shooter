import pygame
from pathlib import Path
from config import WIDTH, HEIGHT
from sprites.enemy import EnemyFactory
from sprites.player import Player
from audio.sound_manager import SoundManager


class ScoreBoard:
    """Encapsulates score/life state and rendering (SRP, Encapsulation)."""

    def __init__(self, font: pygame.font.Font, big_font: pygame.font.Font, lives: int = 3):
        self._font = font
        self._big_font = big_font
        self._score = 0
        self._lives = lives

    @property
    def score(self) -> int:
        return self._score

    @property
    def lives(self) -> int:
        return self._lives

    @property
    def game_over(self) -> bool:
        return self._lives <= 0

    def add_score(self, amount: int):
        self._score += amount

    def lose_life(self):
        self._lives -= 1

    def draw(self, screen: pygame.Surface):
        score_surf = self._font.render(f"Score: {self._score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        for i in range(self._lives):
            pygame.draw.rect(screen, (255, 0, 0), (10 + i * 30, 40, 20, 20))

        if self.game_over:
            text = self._big_font.render("Game Over", True, (255, 0, 0))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)

            restart = self._font.render("Press R to Restart", True, (255, 255, 255))
            rect2 = restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            screen.blit(restart, rect2)


class GameScene:
    """Main game orchestrator.

    - Composition: holds Player, EnemyFactory, ScoreBoard, sprite groups.
    - Dependency Inversion: depends on EnemyFactory abstraction instead of concrete enemy classes.
    - Open/Closed: add new enemy behaviors in EnemyFactory without touching GameScene.
    """

    def __init__(self, enemies_per_wave: int = 5):
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 72)
        self.background = self._load_background()
        self.enemies_per_wave = enemies_per_wave
        self.factory = EnemyFactory()
        self.sounds = SoundManager()
        self.reset()

    def _load_background(self):
        image_candidates = [
            Path("assets/background.png"),
            Path("assets/background.jpg"),
            Path("background.png/ChatGPT Image 7 มี.ค. 2569 20_19_17.png"),
        ]
        for image_path in image_candidates:
            if image_path.exists():
                try:
                    image = pygame.image.load(str(image_path)).convert()
                    return pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
                except pygame.error:
                    pass
        return None

    def reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.player = Player(self.bullets, self.all_sprites, sound_manager=self.sounds)
        self.all_sprites.add(self.player)

        self.scoreboard = ScoreBoard(self.font, self.big_font, lives=3)

        for _ in range(self.enemies_per_wave):
            self._spawn_enemy()

    def _spawn_enemy(self):
        difficulty = self.scoreboard.score // 50
        enemy = self.factory.create_enemy(difficulty)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def handle_events(self, event):
        if self.scoreboard.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset()

    def update(self):
        if self.scoreboard.game_over:
            return

        self.all_sprites.update()

        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for _ in hits:
            self.scoreboard.add_score(10)
            self.sounds.play_explosion()
            self._spawn_enemy()

        player_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if player_hits:
            self.scoreboard.lose_life()
            self.sounds.play_hit()
            if not self.scoreboard.game_over:
                self.player.rect.centerx = WIDTH // 2
                self.player.rect.bottom = HEIGHT - 10
                self._spawn_enemy()

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        self.all_sprites.draw(screen)
        self.scoreboard.draw(screen)
