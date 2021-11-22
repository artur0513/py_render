import math
import pygame
import random
import numpy as np
from pygame import gfxdraw


# draw_line не работает(пока)
def draw_line(surface, pos1, pos2, color):
    x0 = round(pos1[0])
    y0 = round(pos1[1])
    x1 = round(pos2[0])
    y1 = round(pos2[1])
    steep = False

    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    derror2 = abs(dy) * 2
    error2 = 0
    y = y0
    for x in range(x0, x1):
        if steep:
            surface.set_at((y, x), color)
        else:
            surface.set_at((x, y), color)
        error2 += derror2

        if derror2 > dx:
            if y1 > y0:
                y += 1
            else:
                y -= 1
            error2 -= 2 * dx


def draw_triangle(surface, points, colors, texture_points, texture, zbuffer):
    tsizex = texture.get_width() - 1
    tsizey = texture.get_height() - 1

    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    pos1 = points[0]
    pos2 = points[1]
    pos3 = points[2]

    tpos1 = texture_points[0]
    tpos2 = texture_points[1]
    tpos3 = texture_points[2]

    if not (pos1[1] == pos2[1] and pos1[1] == pos3[1]):
        HEIGHT = surface.get_height()
        WIDTH = surface.get_width()

        if pos1[1] > pos2[1]:
            pos1, pos2 = pos2, pos1
            color1, color2 = color2, color1
            tpos1, tpos2 = tpos2, tpos1
        if pos1[1] > pos3[1]:
            pos1, pos3 = pos3, pos1
            color1, color3 = color3, color1
            tpos1, tpos3 = tpos3, tpos1
        if pos2[1] > pos3[1]:
            pos2, pos3 = pos3, pos2
            color2, color3 = color3, color2
            tpos2, tpos3 = tpos3, tpos2

        total_height = pos3[1] - pos1[1]
        for y in range(math.ceil(pos1[1]), math.ceil(pos2[1])):
            segment_height = pos2[1] - pos1[1]
            alpha = (y - pos1[1]) / total_height
            beta = (y - pos1[1]) / segment_height

            Ax = math.ceil(pos1[0] + (pos3[0] - pos1[0]) * alpha)
            Az = math.ceil(pos1[2] + (pos3[2] - pos1[2]) * alpha)
            Bx = math.ceil(pos1[0] + (pos2[0] - pos1[0]) * beta)
            Bz = math.ceil(pos1[2] + (pos2[2] - pos1[2]) * beta)

            colorA = vector_sum(vector_multiply(color1, 1 - alpha), vector_multiply(color3, alpha))
            colorB = vector_sum(vector_multiply(color1, 1 - beta), vector_multiply(color2, beta))

            if Ax > Bx:
                Ax, Bx = Bx, Ax
                colorA, colorB = colorB, colorA
            if Ax < 0:
                Ax = 0
            if Bx > WIDTH:
                Bx = WIDTH
            for i in range(Ax, Bx):
                if Ax == Bx:
                    phi = 1
                else:
                    phi = (i - Ax) / (Bx - Ax)
                Pz = Az + (Bz - Az) * phi

                Pcolor = vector_sum(colorA, vector_multiply(vector_diff(colorB, colorA), phi))

                mass = barcoords((pos1, pos2, pos3), (i, y))
                tpoint = decartcoords((tpos1, tpos2, tpos3), mass)
                Tcolor = texture.get_at((round(tpoint[0] * tsizex), round(tpoint[1] * tsizey)))

                Pcolor = sum_colors(Tcolor, Pcolor)
                if 0 < y < HEIGHT:
                    if (zbuffer[y * WIDTH + i] == -1 or zbuffer[y * WIDTH + i] > Pz) and Pz > 0:
                        zbuffer[y * WIDTH + i] = Pz
                        gfxdraw.pixel(surface, i, y, Pcolor)

        for y in range(math.ceil(pos2[1]), math.ceil(pos3[1])):

            segment_height = pos3[1] - pos2[1]
            alpha = (y - pos1[1]) / total_height
            beta = (y - pos2[1]) / segment_height

            Ax = math.ceil(pos1[0] + (pos3[0] - pos1[0]) * alpha)
            Az = math.ceil(pos1[2] + (pos3[2] - pos1[2]) * alpha)
            Bx = math.ceil(pos2[0] + (pos3[0] - pos2[0]) * beta)
            Bz = math.ceil(pos2[2] + (pos3[2] - pos2[2]) * beta)

            colorA = vector_sum(vector_multiply(color1, 1 - alpha), vector_multiply(color3, alpha))
            colorB = vector_sum(vector_multiply(color3, beta), vector_multiply(color2, 1 - beta))

            if Ax > Bx:
                Ax, Bx = Bx, Ax
                colorA, colorB = colorB, colorA
            if Ax < 0:
                Ax = 0
            if Bx > WIDTH:
                Bx = WIDTH
            for i in range(Ax, Bx):
                if Ax == Bx:
                    phi = 1
                else:
                    phi = (i - Ax) / (Bx - Ax)
                Pz = Az + (Bz - Az) * phi

                Pcolor = vector_sum(colorA, vector_multiply(vector_diff(colorB, colorA), phi))
                mass = barcoords((pos1, pos2, pos3), (i, y))
                tpoint = decartcoords((tpos1, tpos2, tpos3), mass)
                Tcolor = texture.get_at((round(tpoint[0] * tsizex), round(tpoint[1] * tsizey)))
                Pcolor = sum_colors(Tcolor, Pcolor)

                if 0 < y < HEIGHT:
                    if (zbuffer[y * WIDTH + i] == -1 or zbuffer[y * WIDTH + i] > Pz) and Pz > 0:
                        zbuffer[y * WIDTH + i] = Pz
                        gfxdraw.pixel(surface, i, y, Pcolor)

    return zbuffer


def scalar(vector1, vector2):
    scalar = vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]
    return scalar


def cos_between_vectors(vector1, vector2):
    a = scalar(vector1, vector2)
    b = math.sqrt(scalar(vector1, vector1) * scalar(vector2, vector2))
    ans = a / b
    return ans


def normal_vector_v(vector1, vector2):
    # x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
    # y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
    # z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    v1_np = np.array(vector1)
    v2_np = np.array(vector2)
    ans = np.cross(v1_np, v2_np)
    return ans


def normal_vector_p(point1, point2, point3):
    vector1 = vector_diff(point1, point2)
    vector2 = vector_diff(point1, point3)
    ans = normal_vector_v(vector1, vector2)
    return ans


def vector_diff(vector1, vector2):
    ans = [x - y for x, y in zip(vector1, vector2)]
    return ans


def vector_sum(vector1, vector2):
    ans = [x + y for x, y in zip(vector1, vector2)]
    return ans


def vector_multiply(vector, number):
    ans = [x * number for x in vector]
    return ans


def vector_div(vector, number):
    ans = [x / number for x in vector]
    return ans


def triangle_center(point1, point2, point3):
    a = vector_sum(point1, point2)
    b = vector_sum(a, point3)
    ans = vector_div(b, 3)
    return ans


def read_from_file(filename):
    file = open(filename, 'r')
    vertices = []
    faces = []
    texture_links = []
    texture_points = []
    for line in file:
        if len(line) >= 2:
            line = line.replace("\n", "")
            line = line.strip()

            if line[0] == "v" and line[1] == " ":
                newline = line.replace("v ", "")
                vertices.append([- float(x) for x in newline.split(" ")])

            if line[0] == "v" and line[1] == "t" and line[2] == " ":
                newline = line.replace("vt  ", "")
                texture_points.append([float(x) for x in newline.split(" ")])

            if line[0] == "f" and line[1] == " ":
                line_replaced = line.replace("f ", "")

                if len(line_replaced.split(" ")[0].split("/")) > 1:
                    point1 = int(line_replaced.split(" ")[0].split("/")[0])
                    point2 = int(line_replaced.split(" ")[1].split("/")[0])
                    point3 = int(line_replaced.split(" ")[2].split("/")[0])

                    texture_point1 = int(line_replaced.split(" ")[0].split("/")[1])
                    texture_point2 = int(line_replaced.split(" ")[1].split("/")[1])
                    texture_point3 = int(line_replaced.split(" ")[2].split("/")[1])

                    faces.append([point1, point2, point3])
                    texture_links.append([texture_point1, texture_point2, texture_point3])

                else:
                    point1 = int(line_replaced.split(" ")[0])
                    point2 = int(line_replaced.split(" ")[1])
                    point3 = int(line_replaced.split(" ")[2])
                    faces.append([point1, point2, point3])

    file.close()
    return vertices, faces, texture_links, texture_points


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return [r, g, b]


def sum_colors(color1, color2):
    ans_color_r = (color1[0] + color2[0]) / 2
    ans_color_g = (color1[1] + color2[1]) / 2
    ans_color_b = (color1[2] + color2[2]) / 2
    return (ans_color_r, ans_color_g, ans_color_b)


def matrix_multiply(a, b):
    a_np = np.array(a)
    b_np = np.array(b)
    c_np = np.dot(a_np, b_np)
    c = tuple(c_np)
    return c


def color_fix(color):
    for i in range(3):
        color[i] = min(max(color[i], 0), 255)


def barcoords(triangle, point):
    x1 = triangle[0][0]
    y1 = triangle[0][1]
    x2 = triangle[1][0]
    y2 = triangle[1][1]
    x3 = triangle[2][0]
    y3 = triangle[2][1]
    x = point[0]
    y = point[1]

    m1 = ((y - y3) * (x2 - x3) - (x - x3) * (y2 - y3)) / ((y1 - y3) * (x2 - x3) - (x1 - x3) * (y2 - y3))
    m2 = ((y - y1) * (x3 - x1) - (x - x1) * (y3 - y1)) / ((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1))
    m3 = ((y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)) / ((y3 - y1) * (x2 - x1) - (x3 - x1) * (y2 - y1))

    return [m1, m2, m3]


def decartcoords(triangle, mass):
    moment1 = vector_multiply(triangle[0], mass[0])
    moment2 = vector_multiply(triangle[1], mass[1])
    moment3 = vector_multiply(triangle[2], mass[2])
    point = vector_sum(moment1, moment2)
    point = vector_sum(point, moment3)
    return point
