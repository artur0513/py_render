import pygame.image

from renderer import *
import time

FPS = 60
WIDTH = 1280
HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
BACKGROUND = (0, 190, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("render test")

pygame.font.init()
font = pygame.font.Font(None, 30)

nigger = Object("models/african_head.obj.txt", "models/african_head_diffuse.tga", screen)
nigger.add_normal_map("models/african_head_nm.tga")
#nigger.multiply_coords(1)
nigger.rotate([10, 5, 15])
nigger.move([0, 0, 6])

renderer = Renderer(screen)
lamp = Light_source([0, 0, -20], 1, WHITE)
renderer.add(lamp)

renderer.add(nigger)
renderer.render()


#for i in range(60):
#    nigger.rotate([0, 6*i, 0])
#    renderer.render()
#    pygame.image.save(screen, "video/frame" + str(i) + ".png")

full_time = 0
i = 0
clock = pygame.time.Clock()
faces_count = nigger.get_faces_count()
pygame.display.update()
finished = False
while not finished:
    clock.tick(FPS)
    i += 1

    pygame.display.update()
    #nigger.draw_skelet()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            x = 20
            if event.key == pygame.K_w:
                lamp.move([x, 0, 0])
            if event.key == pygame.K_s:
                lamp.move([-x, 0, 0])
            if event.key == pygame.K_a:
                lamp.move([0, x, 0])
            if event.key == pygame.K_d:
                lamp.move([0, -x, 0])
            if event.key == pygame.K_SPACE:
                lamp.move([0, 0, x])
            if event.key == pygame.K_LCTRL:
                lamp.move([0, 0, -x])
            if event.key == pygame.K_ESCAPE:
                finished = True

pygame.quit()
