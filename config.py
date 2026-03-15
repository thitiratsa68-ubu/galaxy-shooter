import pygame

# ขนาดหน้าจอและเฟรมเรต
WIDTH = 800
HEIGHT = 600
FPS = 60

# ผู้เล่น
PLAYER_SPEED = 6
PLAYER_BOTTOM_OFFSET = 20
PLAYER_SHOOT_DELAY_MS = 250
PLAYER_SIZE = (80, 80)
PLAYER_FALLBACK_SIZE = (64, 64)

# กระสุน
BULLET_SIZE = (5, 15)
BULLET_COLOR = (255, 255, 0)
BULLET_SPEED = -10

# ศัตรู
ENEMY_SIZE = (50, 50)
ENEMY_FALLBACK_SIZE = (40, 40)
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 5
ENEMY_SPAWN_Y_RANGE = (-150, -40)
INITIAL_ENEMIES = 5

# ศัตรูชุดที่ 2
ENEMY2_SIZE = (60, 60)

# สถานะเกม
INITIAL_LIVES = 3
SCORE_PER_HIT = 10

# HUD
SCORE_POS = (10, 10)
LIFE_POS = (10, 40)
LIFE_SIZE = (20, 20)
LIFE_GAP = 30

# ไฟล์ทรัพยากร (ปรับได้ที่นี่ ไม่ต้องแก้โค้ดหลัก)
LEVEL1_BACKGROUNDS = [
    "assets/background.png",
    "assets/background.jpg",
    "background.png/ChatGPT Image 7 มี.ค. 2569 20_19_17.png",
]
LEVEL2_BACKGROUNDS = [
    "assets/background2.png",
    "assets/background2.jpg",
    "assets/background_level2.png",
    "assets/background_level2.jpg",
    "assets/bg2.png",
    "assets/bg2.jpg",
    "assets/start_screen2.png",
    "assets/start_screen.png",
    "assets/images/background2.png",
    "assets/images/background2.jpg",
    "assets/images/background_level2.png",
    "assets/images/background_level2.jpg",
    "assets/images/bg2.png",
    "assets/images/bg2.jpg",
    "assets/images/start_screen2.png",
    "assets/images/start_screen.png",
]
ENEMY1_IMAGES = [
    "assets/enemy.png",
    "assets/enemy.jpg",
    "enemy.png/e10138041e8a5d17269b8d2fbbfe9736.jpg",
]
ENEMY2_IMAGES = [
    "assets/enemy2.png",
    "assets/enemy2.jpg",
    "enemy2.png/ChatGPT Image 14 มี.ค. 2569 18_17_44.png",
    "assets/images/enemy2.png",
    "assets/images/enemy2.jpg",
]
START_BACKGROUNDS = [
    "assets/start_screen.png",
    "assets/start_screen2.png",
    "assets/start_menu.png",
    "assets/title.png",
    "assets/sceen.png",
    "assets/screen.png",
    "assets/images/start_screen.png",
    "assets/images/start_screen2.png",
    "assets/images/title.png",
    "assets/images/sceen.png",
    "assets/images/screen.png",
]
START_SHIP_IMAGES = [
    "assets/start_ship.png",
    "assets/red_ship.png",
    "assets/ship_title.png",
    "assets/images/red_ship.png",
]
