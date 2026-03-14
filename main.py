import pygame

# ลดปัญหาเสียงแครกโดยใช้บัฟเฟอร์ใหญ่ขึ้นและสเตอริโอ
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)

from config import WIDTH, HEIGHT, FPS
from scenes.game_scene import GameScene


def main():
    pygame.init()
    # ลดภาระเรนเดอร์เพื่อไม่ให้เสียงขาด: โหมดมาตรฐาน ไม่ใช้ scaling
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galaxy Shooter")

    clock = pygame.time.Clock()
    game = GameScene()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_events(event)

        game.update()
        game.draw(screen)

        pygame.display.flip()

    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
