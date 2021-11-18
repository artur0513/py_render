import copy

from functions import *


class Light_source:
    def __init__(self, pos, strength, color):
        self.strength = strength
        self.pos = pos
        self.color = color

    def move(self, vector):
        self.pos = vector_sum(self.pos, vector)


class Object:
    def __init__(self, filename, screen):
        self.vertices, self.faces, self.normals, self.links_to_normals = read_from_file(filename)
        self.world_vertices = copy.deepcopy(self.vertices)
        self.cam_vertices = copy.deepcopy(self.vertices)
        self.screen = screen
        self.calculate_normals()
        #for face in self.faces:
            #point1 = self.vertices[face[0] - 1]
            #point2 = self.vertices[face[1] - 1]
            #point3 = self.vertices[face[2] - 1]
            # self.normals.append(normal_vector_p(point1, point2, point3))
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.world_pos = [0, 0, 0]

    def get_faces_count(self):
        return len(self.faces)

    def draw_skelet(self):
        surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        for face in self.faces:
            point1 = self.cam_vertices[face[0] - 1]
            point2 = self.cam_vertices[face[1] - 1]
            point3 = self.cam_vertices[face[2] - 1]
            line_color = (200, 50, 50)
            pygame.draw.line(surface, line_color, point1[:-1], point2[:-1])
            pygame.draw.line(surface, line_color, point2[:-1], point3[:-1])
            pygame.draw.line(surface, line_color, point1[:-1], point3[:-1])
        # surface = pygame.transform.flip(surface, False, True)
        self.screen.blit(surface, (0, 0))

    def draw(self, zbuffer, lights):
        self.current_faces_counter = 0
        surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        i = 0
        light_const = 1000

        for face in self.faces:
            point1 = self.cam_vertices[face[0] - 1]  # Точки для отрисовки берем в экранных координатах
            point2 = self.cam_vertices[face[1] - 1]
            point3 = self.cam_vertices[face[2] - 1]
            need_to_draw = False

            color1 = (0, 0, 0)
            color2 = (0, 0, 0)
            color3 = (0, 0, 0)

            for light in lights:
                """
                v = self.vertices[face[0] - 1]  # А вот тени считаем в исходных, мировых
                v = vector_div(v, math.sqrt(scalar(v, v)))
                n1 = self.normals[self.links_to_normals[i][0] - 1]
                n = vector_div(n1, math.sqrt(scalar(n1, n1)))
                l = vector_diff(self.vertices[face[0] - 1], light.pos)
                l = vector_div(l, math.sqrt(scalar(l, l)))
                h = vector_sum(l, v)
                h = vector_div(h, math.sqrt(scalar(h, h)))
                illumination1 = 1 - scalar(l, h) ** 1.5
                l = vector_diff(self.vertices[face[0] - 1], light.pos)
                illumination1 *= scalar(l, l)/light_const

                v = self.vertices[face[1] - 1]  # А вот тени считаем в исходных, мировых
                v = vector_div(v, math.sqrt(scalar(v, v)))
                n1 = self.normals[self.links_to_normals[i][1] - 1]
                n = vector_div(n1, math.sqrt(scalar(n1, n1)))
                l = vector_diff(self.vertices[face[1] - 1], light.pos)
                l = vector_div(l, math.sqrt(scalar(l, l)))
                h = vector_sum(l, v)
                h = vector_div(h, math.sqrt(scalar(h, h)))
                illumination2 = 1 - scalar(l, h) ** 1.5
                l = vector_diff(self.vertices[face[1] - 1], light.pos)
                illumination2 *= scalar(l, l)/light_const

                v = self.vertices[face[2] - 1]  # А вот тени считаем в исходных, мировых
                v = vector_div(v, math.sqrt(scalar(v, v)))
                n1 = self.normals[self.links_to_normals[i][2] - 1]
                n = vector_div(n1, math.sqrt(scalar(n1, n1)))
                l = vector_diff(self.vertices[face[2] - 1], light.pos)
                l = vector_div(l, math.sqrt(scalar(l, l)))
                h = vector_sum(l, v)
                h = vector_div(h, math.sqrt(scalar(h, h)))
                illumination3 = 1 - scalar(l, h) ** 1.5
                l = vector_diff(self.vertices[face[2] - 1], light.pos)
                illumination3 *= scalar(l, l)/light_const
                """
                r = vector_diff(self.vertices[face[0] - 1], light.pos)
                illumination1 = cos_between_vectors(self.normals[face[0] - 1], r) * light.strength \
                                / scalar(r, r) * light_const

                r = vector_diff(self.vertices[face[1] - 1], light.pos)
                illumination2 = cos_between_vectors(self.normals[face[1] - 1], r) * light.strength \
                                / scalar(r, r) * light_const

                r = vector_diff(self.vertices[face[2] - 1], light.pos)
                illumination3 = cos_between_vectors(self.normals[face[2] - 1], r) * light.strength \
                                / scalar(r, r) * light_const

                illumination1 = min(1, illumination1)
                illumination2 = min(1, illumination2)
                illumination3 = min(1, illumination3)

                illumination1 = max(0, illumination1)
                illumination2 = max(0, illumination2)
                illumination3 = max(0, illumination3)

                if illumination1 > 0:
                    color1 = sum_colors(vector_multiply(light.color, illumination1), color1)
                    need_to_draw = True

                if illumination2 > 0:
                    color2 = sum_colors(vector_multiply(light.color, illumination2), color2)
                    need_to_draw = True

                if illumination3 > 0:
                    color3 = sum_colors(vector_multiply(light.color, illumination3), color3)
                    need_to_draw = True

                # if illumination < 0:
                #    illumination = 0.05
                #    color = sum_colors(vector_multiply(light.color, illumination), color)
                #    need_to_draw = True
            #print("Цвета верщин - ", color1, color2, color3)
            if need_to_draw or True:
                self.current_faces_counter += 1
                zbuffer = draw_triangle(surface,
                                        point1, point2, point3, color1, color2, color3, zbuffer)
            i += 1

        self.screen.blit(surface, (0, 0))
        return zbuffer

    def recalculate_coords(self, fov):
        perspective_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        fovY = fov
        aspect_ratio = self.WIDTH / self.HEIGHT
        Yscale = 1 / math.tan(fovY * math.pi / 360)
        Xscale = Yscale / aspect_ratio

        perspective_matrix[0][0] = Xscale
        perspective_matrix[1][1] = Yscale
        perspective_matrix[2][2] = 1
        perspective_matrix[3][2] = 0.5
        perspective_matrix[3][3] = 1

        i = 0
        for point in self.world_vertices:
            coord_matrix = [point[0], point[1], point[2], 1]
            new_coords = matrix_multiply(perspective_matrix, coord_matrix)
            self.cam_vertices[i][0] = self.WIDTH * (1 + new_coords[0] / new_coords[3]) / 2
            self.cam_vertices[i][1] = self.HEIGHT * (1 + new_coords[1] / new_coords[3]) / 2
            self.cam_vertices[i][2] = new_coords[2] / new_coords[3] * 10000
            i += 1

    def rotate(self, angle):  # Угол в градусах, функция сама переводит в радианы
        angle_x = angle[0] * math.pi / 180
        angle_y = angle[1] * math.pi / 180
        angle_z = angle[2] * math.pi / 180
        rotate_matrix_x = [[1, 0, 0], [0, math.cos(angle_x), -math.sin(angle_x)],
                           [0, math.sin(angle_x), math.cos(angle_x)]]
        rotate_matrix_y = [[math.cos(angle_y), 0, math.sin(angle_y)], [0, 1, 0],
                           [-math.sin(angle_y), 0, math.cos(angle_y)]]
        rotate_matrix_z = [[math.cos(angle_z), -math.sin(angle_z), 0], [math.sin(angle_z), math.cos(angle_z), 0],
                           [0, 0, 1]]
        i = 0
        for point in self.vertices:
            coords = [point[0], point[1], point[2]]
            new_coords1 = matrix_multiply(rotate_matrix_x, coords)
            new_coords2 = matrix_multiply(rotate_matrix_y, new_coords1)
            new_coords = matrix_multiply(rotate_matrix_z, new_coords2)
            self.vertices[i] = list(new_coords)
            self.world_vertices[i] = vector_sum(self.vertices[i], self.world_pos)
            i += 1

        i = 0
        for point in self.normals:
            coords = [point[0], point[1], point[2]]
            new_coords1 = matrix_multiply(rotate_matrix_x, coords)
            new_coords2 = matrix_multiply(rotate_matrix_y, new_coords1)
            new_coords = matrix_multiply(rotate_matrix_z, new_coords2)
            self.normals[i] = list(new_coords)
            i += 1

    def move(self, vector):
        self.world_pos = vector_sum(self.world_pos, vector)
        i = 0
        for point in self.world_vertices:
            self.world_vertices[i] = vector_sum(self.world_pos, point)
            i += 1

    def calculate_normals(self):
        self.normals = []
        self.links_to_normals = [[0, 0, 0] for i in range(len(self.faces))]
        for i in range(1, len(self.vertices)+1):
            normals_sum = (0, 0, 0)
            j = 0
            for face in self.faces:
                if face[0] == i or face[1] == i or face[2] == i:
                    point1 = self.vertices[face[0] - 1]
                    point2 = self.vertices[face[1] - 1]
                    point3 = self.vertices[face[2] - 1]
                    if face[0] == i:
                        self.links_to_normals[j][0] = i
                        normals_sum = vector_sum(normals_sum, normal_vector_p(point1, point2, point3))
                    if face[1] == i:
                        self.links_to_normals[j][1] = i
                        normals_sum = vector_sum(normals_sum, normal_vector_p(point1, point2, point3))
                    if face[2] == i:
                        self.links_to_normals[j][2] = i
                        normals_sum = vector_sum(normals_sum, normal_vector_p(point1, point2, point3))
                    j += 1
            normals_sum = vector_div(normals_sum, math.sqrt(scalar(normals_sum, normals_sum)))
            self.normals.append(normals_sum)


    def multiply_coords(self, koef):
        for i in range(len(self.vertices)):
            self.vertices[i] = vector_multiply(self.vertices[i], koef)

