import pygame


def load_texture(image_path):
    texture = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture, "RGBA", 1)
    return texture, texture_data
