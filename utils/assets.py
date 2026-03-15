from pathlib import Path
import pygame


def load_first_image(paths, size=None, convert_alpha=True):
    """พยายามโหลดรูปจากลิสต์ path แรกที่เจอคืน surface; ถ้ากำหนด size จะสเกลให้พอดี"""
    for p in paths:
        path = Path(p)
        if not path.exists():
            continue
        try:
            img = pygame.image.load(str(path))
            if convert_alpha:
                img = img.convert_alpha()
            else:
                img = img.convert()
            if size:
                img = pygame.transform.smoothscale(img, size)
            return img
        except pygame.error:
            continue
    return None
