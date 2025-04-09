import pygame
pygame.init()
import time

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Тестовый проект")

image = pygame.image.load("pog.png")
image_rect  = image.get_rect()

image2 = pygame.image.load("pythons .png")
image_rect2 = image2.get_rect()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if event.type == pygame.MOUSEMOTION:
        mouseX, mouseY = pygame.mouse.get_pos()
        image_rect.x = mouseX -150
        image_rect.y = mouseY -150

    if image_rect.colliderect(image_rect2):
        print("Произошло столкновение")
        time.sleep(1)

    screen.fill((25, 34, 250))
    screen.blit(image, image_rect)
    screen.blit(image2, image_rect2)
    pygame.display.flip()


pygame.quit()