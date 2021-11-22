from renderer import *

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

camera_pos = (0, 0, 5)


nigger = Object("models/african_head.obj.txt", "models/african_head_diffuse.tga", screen)
nigger.multiply_coords(1)
nigger2 = Object("models/african_head.obj.txt", "models/african_head_diffuse.tga", screen)
nigger3 = Object("models/african_head.obj.txt", "models/african_head_diffuse.tga", screen)
nigger.rotate((20, 20, 30))
nigger.move([0, 0, 6])
nigger2.rotate((10, -30, 10))
nigger2.move([1, 2, 9])
nigger3.rotate((30, 35, 40))
nigger3.move([-1, -2, 8])

renderer = Renderer(screen)
#draw_triangle(screen, ((100, 100, 1), (200, 300, 1), (300, 200, 1)), (255, 0, 0), (0, 255, 0), (0, 0, 255), renderer.zbuffer )
lamp = Light_source([-20, -20, -20], 1, WHITE)
lamp2 = Light_source([-30, 0, -20], 4, RED)
lamp3 = Light_source([-20, -20, -10], 1, BACKGROUND)
lamp4 = Light_source([0, 0, -50], 1, WHITE)
renderer.add(lamp)
#renderer.add(lamp2)
#renderer.add(lamp3)
#renderer.add(lamp4)
renderer.add(nigger)
renderer.add(nigger3)
renderer.add(nigger2)
renderer.update()
renderer.render()

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
