import pygame
from pathlib import Path
from config import WIDTH, HEIGHT


class StartMenu:
    """หน้าจอเริ่มเกม แสดงภาพเปิดและแถบโหลดก่อนเข้าเกมอัตโนมัติ"""

    def __init__(self):
        self.background = self._load_background()
        self.font = pygame.font.SysFont(None, 48)
        self.title_font = pygame.font.SysFont(None, 96, bold=True)
        self.done = False
        self.progress = 0  # 0-100
        self._build_loading_bar()
        self.ship = self._load_ship_overlay()

    def _load_background(self):
        candidates = [
            Path("assets/start_screen.png"),
            Path("assets/start_screen2.png"),
            Path("assets/start_menu.png"),
            Path("assets/title.png"),
            Path("assets/sceen.png"),   # รองรับชื่อไฟล์ที่ผู้ใช้ใส่
            Path("assets/screen.png"),
            Path("assets/images/start_screen.png"),
            Path("assets/images/start_screen2.png"),
            Path("assets/images/title.png"),
            Path("assets/images/sceen.png"),
            Path("assets/images/screen.png"),
        ]
        folders = [Path("assets/start"), Path("assets/images/start"), Path("assets/images")]
        path = self._pick_first_image(candidates, folders)
        if path:
            try:
                img = pygame.image.load(str(path)).convert()
                return pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            except pygame.error:
                pass
        # fallback: fill gradient-ish rectangle
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill((5, 10, 35))
        return surf

    def _build_loading_bar(self):
        bar_width = int(WIDTH * 0.6)
        bar_height = 24
        self.bar_rect = pygame.Rect(0, 0, bar_width, bar_height)
        self.bar_rect.center = (WIDTH // 2, int(HEIGHT * 0.9))

    def _load_ship_overlay(self):
        candidates = [
            Path("assets/start_ship.png"),
            Path("assets/red_ship.png"),
            Path("assets/ship_title.png"),
            Path("assets/images/red_ship.png"),
        ]
        folders = [Path("assets/start"), Path("assets/images/start")]
        path = self._pick_first_image(candidates, folders)
        if path and path.exists():
            try:
                img = pygame.image.load(str(path)).convert_alpha()
                # สเกลให้พอดีจอครึ่งล่าง
                target_h = int(HEIGHT * 0.45)
                scale = target_h / img.get_height()
                target_w = int(img.get_width() * scale)
                return pygame.transform.smoothscale(img, (target_w, target_h))
            except pygame.error:
                pass
        return None

    def handle_events(self, event):
        # อนุญาตกดข้ามโหลด
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.done = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.done = True

    def update(self):
        if not self.done:
            self.progress = min(100, self.progress + 1.2)  # ~1.5s ที่ 60fps
            if self.progress >= 100:
                self.done = True

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # ชื่อเกม
        title = self.title_font.render("GALAXY SHOOTER", True, (0, 200, 255))
        trect = title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.15)))
        screen.blit(title, trect)

        # รูปยาน overlay
        if self.ship:
            ship_rect = self.ship.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.5)))
            screen.blit(self.ship, ship_rect)
        # แถบโหลดสไตล์ภาพตัวอย่าง
        outline_color = (0, 200, 255)
        fill_color = (0, 255, 200)
        seg_count = 18

        pygame.draw.rect(screen, outline_color, self.bar_rect, 3, border_radius=6)
        seg_width = (self.bar_rect.width - seg_count + 1) // seg_count
        filled_segments = int(seg_count * (self.progress / 100))
        for i in range(filled_segments):
            seg = pygame.Rect(
                self.bar_rect.left + i * (seg_width + 1) + 3,
                self.bar_rect.top + 3,
                seg_width - 4,
                self.bar_rect.height - 6,
            )
            pygame.draw.rect(screen, fill_color, seg, border_radius=3)

        loading_text = self.font.render("LOADING...", True, outline_color)
        lrect = loading_text.get_rect(midbottom=(self.bar_rect.centerx, self.bar_rect.top - 10))
        screen.blit(loading_text, lrect)

    def _pick_first_image(self, candidates, folders):
        for p in candidates:
            if p.exists():
                return p
        exts = (".png", ".jpg", ".jpeg")
        for folder in folders:
            if folder.is_dir():
                for path in sorted(folder.iterdir()):
                    if path.is_file() and path.suffix.lower() in exts:
                        return path
        return None
