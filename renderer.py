import pygame.image

from object import *
import time
import os

import datetime

now = datetime.datetime.now()

class Renderer:
    def __init__(self, screen):

        self.screen = screen
        self.objects = []
        self.lights = []
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.fov = 45

        self.show_statistics = True
        self.total_draw_faces = 0
        self.draw_time_ms = 0
        self.stat_x = 10
        self.stat_y = 10
        self.color = (255, 255, 255)

        pygame.font.init()
        self.font = pygame.font.Font(None, 30)

        self.zbuffer = [-1 for i in range(self.WIDTH * self.HEIGHT)]

        screen_numbers = []
        i = 1
        for dirpath, dirnames, filenames in os.walk('screenshots'):
            filenames = str(filenames)
            filenames = filenames.replace("['", "")
            filenames = filenames.replace("']", "")
            for filename in filenames.split("', '"):

                if filename.find("screenshot") != -1:
                    filename = filename.replace("screenshot", "")
                    filename = filename.replace(".png", "")
                    screen_numbers.append(int(filename))
        while i in screen_numbers:
            i += 1
        self.next_screen_name = "screenshots/screenshot" + str(i) + ".png"

    def add(self, target):
        if type(target) == Object:
            self.objects.append(target)

        if type(target) == Light_source:
            self.lights.append(target)

    def render(self):
        self.total_draw_faces = 0
        self.draw_time_ms = 0

        start_time = time.time()
        self.screen.fill((0, 0, 0))
        for obj in self.objects:
            obj.recalculate_coords(self.fov)
            self.zbuffer = obj.draw(self.zbuffer, self.lights)
            self.total_draw_faces += obj.current_faces_counter
        self.zbuffer = [-1 for i in range(self.WIDTH * self.HEIGHT)]
        self.draw_time_ms = round((time.time() - start_time) * 10000) / 10
        if self.show_statistics:
            self.draw_statistics()
        pygame.image.save(self.screen, self.next_screen_name)

    def draw_statistics(self):
        text1 = self.font.render(str(self.draw_time_ms) + " ms per frame", True, self.color)
        self.screen.blit(text1, (self.stat_x, self.stat_y))

        text2 = self.font.render("Total faces: " + str(self.total_draw_faces), True, self.color)
        self.screen.blit(text2, (self.stat_x, self.stat_y + text1.get_height()))

        text3 = self.font.render(str(self.screen.get_width()) + "x" + str(self.screen.get_height()), True, self.color)
        self.screen.blit(text3, (self.stat_x, self.stat_y + text1.get_height() + text2.get_height()))

        text4 = self.font.render(now.strftime("%d-%m-%Y %H:%M"), True, self.color)
        self.screen.blit(text4, (self.stat_x, self.stat_y + text1.get_height() + text2.get_height() + text3.get_height()))
