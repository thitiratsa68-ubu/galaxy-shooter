import pygame
from pathlib import Path
from config import (
    WIDTH,
    HEIGHT,
    INITIAL_ENEMIES,
    INITIAL_LIVES,
    SCORE_PER_HIT,
    SCORE_POS,
    LIFE_POS,
    LIFE_SIZE,
    LIFE_GAP,
    PLAYER_BOTTOM_OFFSET,
    ENEMY_SIZE,
    ENEMY2_IMAGES,
)
from sprites.enemy import Enemy
from sprites.player import Player


class GameScene:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 72)
        self.btn_font = pygame.font.SysFont(None, 42)
        self.background = self._load_background()
        self.alt_background = self._load_alt_background()
        self.alt_applied = False
        self.alt_enemy_image = None
        self.heart = self._load_heart_icon()
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
                    image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
                    return image.convert()
                except pygame.error:
                    pass
        return None

    def _load_alt_background(self):
        """ฉากหลังสำรองสำหรับด่านถัดไปเมื่อคะแนนถึงเกณฑ์"""
        candidates = [
            Path("assets/background2.png"),
            Path("assets/background2.jpg"),
            Path("assets/background_level2.png"),
            Path("assets/background_level2.jpg"),
            Path("assets/bg2.png"),
            Path("assets/bg2.jpg"),
            Path("assets/start_screen2.png"),  # ใช้ภาพเริ่มเกมเดิมเป็นฉากด่าน 2 ได้
            Path("assets/start_screen.png"),
            Path("assets/images/background2.png"),
            Path("assets/images/background2.jpg"),
            Path("assets/images/background_level2.png"),
            Path("assets/images/background_level2.jpg"),
            Path("assets/images/bg2.png"),
            Path("assets/images/bg2.jpg"),
            Path("assets/images/start_screen2.png"),
            Path("assets/images/start_screen.png"),
        ]
        for image_path in candidates:
            if image_path.exists():
                try:
                    image = pygame.image.load(str(image_path)).convert()
                    image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
                    return image.convert()
                except pygame.error:
                    continue
        return None

    def _load_alt_enemy_image(self):
        alt_size = (60, 60)  # ขยายศัตรูชุดที่ 2 เล็กน้อย
        candidates = [Path(p) for p in ENEMY2_IMAGES]
        folder = Path("enemy2.png")
        if folder.is_dir():
            candidates.extend(sorted(folder.glob("*.png")))
            candidates.extend(sorted(folder.glob("*.jpg")))

        for path in candidates:
            if path.exists():
                try:
                    img = pygame.image.load(str(path)).convert_alpha()
                    img = pygame.transform.smoothscale(img, alt_size)
                    return img
                except pygame.error:
                    continue
        return None

    def reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # รีเซ็ตกลับสถานะด่านแรก
        self.background = self._load_background()
        self.alt_applied = False

        self.player = Player(self.bullets, self.all_sprites)
        self.all_sprites.add(self.player)

        for _ in range(INITIAL_ENEMIES):
            enemy = self._create_enemy()
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        self.score = 0
        self.lives = INITIAL_LIVES
        self.game_over = False
        self.started = False
        self._build_start_button()
        self._build_restart_button()

    def _create_enemy(self, base_speed=0):
        enemy = Enemy(base_speed=base_speed)
        if self.alt_applied and self.alt_enemy_image:
            enemy.set_image(self.alt_enemy_image.copy())
        return enemy

    def _build_start_button(self):
        self.start_label = self.btn_font.render("Start", True, (0, 0, 0))
        padding = 20
        w = self.start_label.get_width() + padding
        h = self.start_label.get_height() + padding
        self.start_rect = pygame.Rect(0, 0, w, h)
        self.start_rect.center = (WIDTH // 2, HEIGHT // 2)

    def _build_restart_button(self):
        self.restart_label = self.btn_font.render("Restart", True, (0, 0, 0))
        padding = 20
        w = self.restart_label.get_width() + padding
        h = self.restart_label.get_height() + padding
        self.restart_rect = pygame.Rect(0, 0, w, h)
        self.restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 60)

    def _load_heart_icon(self):
        candidates = [
            Path("assets/heart.png"),
            Path("assets/life.png"),
        ]
        for path in candidates:
            if path.exists():
                try:
                    img = pygame.image.load(str(path)).convert_alpha()
                    return pygame.transform.smoothscale(img, LIFE_SIZE)
                except pygame.error:
                    pass
        # fallback: draw heart shape manually
        surf = pygame.Surface(LIFE_SIZE, pygame.SRCALPHA)
        w, h = LIFE_SIZE
        red = (255, 0, 0)
        pygame.draw.circle(surf, red, (w // 3, h // 3), w // 3)
        pygame.draw.circle(surf, red, (2 * w // 3, h // 3), w // 3)
        points = [(0, h // 3), (w, h // 3), (w // 2, h)]
        pygame.draw.polygon(surf, red, points)
        return surf

    # 🔥 ใช้จัดการปุ่ม
    def handle_events(self, event):
        if not self.started:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_rect.collidepoint(event.pos):
                    self.started = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.started = True
            return

        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_rect.collidepoint(event.pos):
                    self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

    def _apply_alt_theme(self):
        if self.alt_background:
            self.background = self.alt_background
        if self.alt_enemy_image is None:
            self.alt_enemy_image = self._load_alt_enemy_image()
        if self.alt_enemy_image:
            for enemy in self.enemies:
                enemy.set_image(self.alt_enemy_image.copy())
        self.alt_applied = True
    def update(self):
        if self.game_over or not self.started:
            return

        if self.alt_background and not self.alt_applied and self.score >= 100:
            self._apply_alt_theme()

        self.all_sprites.update()

        # กระสุนชนศัตรู
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for _ in hits:
            self.score += SCORE_PER_HIT
            difficulty = self.score // 50
            new_enemy = self._create_enemy(base_speed=difficulty)
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)
            if self.alt_background and not self.alt_applied and self.score >= 100:
                self._apply_alt_theme()

        # ผู้เล่นชนศัตรู
        player_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if player_hits:
            self.lives -= 1

            if self.lives <= 0:
                self.game_over = True
            else:
                self.player.rect.centerx = WIDTH // 2
                self.player.rect.bottom = HEIGHT - PLAYER_BOTTOM_OFFSET

                difficulty = self.score // 50
                new_enemy = self._create_enemy(base_speed=difficulty)
                self.enemies.add(new_enemy)
                self.all_sprites.add(new_enemy)

    
      

        
    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)

        score = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score, SCORE_POS)

        for i in range(self.lives):
            screen.blit(self.heart, (LIFE_POS[0] + i * LIFE_GAP, LIFE_POS[1]))

        if not self.started:
            # ปุ่ม Start
            pygame.draw.rect(screen, (255, 255, 255), self.start_rect)
            pygame.draw.rect(screen, (0, 0, 0), self.start_rect, 3)
            label_rect = self.start_label.get_rect(center=self.start_rect.center)
            screen.blit(self.start_label, label_rect)
            return

        if self.game_over:
            text = self.big_font.render("Game Over", True, (255, 255, 255))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)

            # ปุ่ม Restart
            pygame.draw.rect(screen, (255, 255, 255), self.restart_rect)
            pygame.draw.rect(screen, (0, 0, 0), self.restart_rect, 3)
            label_rect = self.restart_label.get_rect(center=self.restart_rect.center)
            screen.blit(self.restart_label, label_rect)
