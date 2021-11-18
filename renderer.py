import pygame.image

from object import *
import time


class Renderer:
    def __init__(self, screen):

        self.screen = screen
        self.objects = []
        self.lights = []
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.fov = 70

        self.show_statistics = True
        self.total_draw_faces = 0
        self.draw_time_ms = 0
        self.stat_x = 10
        self.stat_y = 10
        self.color = (255, 255, 255)

        pygame.font.init()
        self.font = pygame.font.Font(None, 30)

        self.zbuffer = [-1 for i in range(self.WIDTH * self.HEIGHT)]

    def add(self, target):
        if type(target) == Object:
            self.objects.append(target)

        if type(target) == Light_source:
            self.lights.append(target)

    def render(self):
        self.total_draw_faces = 0
        self.draw_time_ms = 0

        start_time = time.time()
        for obj in self.objects:
            self.zbuffer = obj.draw(self.zbuffer, self.lights)
            self.total_draw_faces += obj.current_faces_counter
        self.zbuffer = [-1 for i in range(self.WIDTH * self.HEIGHT)]
        self.draw_time_ms = round((time.time() - start_time) * 10000) / 10
        if self.show_statistics:
            self.draw_statistics()
        pygame.image.save(self.screen, "screenshot.jpg")

    def update(self):
        for obj in self.objects:
            obj.recalculate_coords(self.fov)

    def draw_statistics(self):
        text1 = self.font.render(str(self.draw_time_ms) + " ms per frame", True, self.color)
        self.screen.blit(text1, (self.stat_x, self.stat_y))

        text2 = self.font.render("Total faces: " + str(self.total_draw_faces), True, self.color)
        self.screen.blit(text2, (self.stat_x, self.stat_y + text1.get_height()))
