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
    def __init__(self, filename, texturename, screen):
        self.vertices, self.faces, self.texture_links, self.texture_points = read_from_file(filename)
        self.world_vertices = copy.deepcopy(self.vertices)
        self.cam_vertices = copy.deepcopy(self.vertices)
        self.screen = screen
        self.texture = pygame.image.load(texturename)
        self.texture = pygame.transform.flip(self.texture, False, True)
        self.calculate_normals()
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.world_pos = [0, 0, 0]
        self.angle = [0, 0, 0]
        self.use_normal_map = False

    def add_normal_map(self, normalname):
        self.use_normal_map = True
        self.normal_map = pygame.image.load(normalname)
        self.normal_map = pygame.transform.flip(self.normal_map, False, True)

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
            points = [point1, point2, point3]

            tpoint1 = self.texture_points[self.texture_links[i][0] - 1]
            tpoint2 = self.texture_points[self.texture_links[i][1] - 1]
            tpoint3 = self.texture_points[self.texture_links[i][2] - 1]
            tpoints = [tpoint1, tpoint2, tpoint3]

            wpoint1 = self.vertices[face[0] - 1]
            wpoint2 = self.vertices[face[1] - 1]
            wpoint3 = self.vertices[face[2] - 1]
            wpoints = [wpoint1, wpoint2, wpoint3]

            if not self.use_normal_map:
                color1 = illumination_color(self.vertices[face[0] - 1], self.normals[face[0] - 1], lights)
                color2 = illumination_color(self.vertices[face[1] - 1], self.normals[face[1] - 1], lights)
                color3 = illumination_color(self.vertices[face[2] - 1], self.normals[face[2] - 1], lights)

                self.current_faces_counter += 1
                colors = [color1, color2, color3]
                zbuffer = draw_triangle2(surface,
                                         points, colors, tpoints, self.texture, zbuffer)


            if self.use_normal_map:
                self.current_faces_counter += 1
                zbuffer = draw_triangle3(surface,
                                         points, wpoints, lights, tpoints, self.texture, self.normal_map, self.angle, zbuffer)
                #zbuffer = draw_triangle4(surface, points, tpoints, self.normal_map, zbuffer)
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
        self.angle = angle
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
        for i in range(1, len(self.vertices) + 1):
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
