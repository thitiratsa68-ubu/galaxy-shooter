import pygame


class SpaceObject(pygame.sprite.Sprite):
    """Abstract base for every in-game sprite.

    Encapsulates the shared surface/rect setup so children only care about
    their specific movement/behavior. Supports SOLID: SRP (one responsibility)
    and LSP (subclasses can replace this base anywhere a SpaceObject is used).
    """

    def __init__(self, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        raise NotImplementedError
