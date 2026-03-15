import pygame
from config import WIDTH, HEIGHT, FPS
from scenes.game_scene import GameScene
from scenes.start_menu import StartMenu


def main():
    # เตรียมมิกเซอร์ให้รองรับเสียงสังเคราะห์และไฟล์เสียง
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
    pygame.init()
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("Galaxy Shooter")

    clock = pygame.time.Clock()
    scene = StartMenu()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene.handle_events(event)

        # เปลี่ยนจากเมนูไปเกมเมื่อกด start
        if isinstance(scene, StartMenu) and scene.done:
            scene = GameScene()

        scene.update()
        scene.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
