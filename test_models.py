from OpenGL import GL
from model import Model


class Cube(Model):

    texture_path = "data/uvtemplate.tga"
    model_path = "data/cube.ply"

    def __init__(self, model_matrix_id, texture_id):
        super(Cube, self).__init__(model_matrix_id, texture_id, self.model_path)
        self.init_buffer_objects()


class Suzanne(Model):

    texture_path = "data/uvtemplate.tga"
    model_path = "data/suzanne.ply"

    def __init__(self, model_matrix_id, texture_id):
        super(Suzanne, self).__init__(model_matrix_id, texture_id, self.model_path)
        self.init_buffer_objects()


class Planet(Model):

    texture_path = "data/uvtemplate.tga"
    model_path = "data/sun.ply"

    def __init__(self, model_matrix_id, texture_id):
        super(Planet, self).__init__(model_matrix_id, texture_id, self.model_path)
        self.init_buffer_objects()


class Sun(Planet):

    SIZE = 20

    def __init__(self, model_matrix_id, texture_id):
        super(Sun, self).__init__(model_matrix_id, texture_id)
        self.init_buffer_objects()
        self.scale(self.SIZE, self.SIZE, self.SIZE)


class Earth(Planet):

    SIZE = 1

    def __init__(self, model_matrix_id, texture_id):
        super(Earth, self).__init__(model_matrix_id, texture_id)
        self.change_colors(0.0, 0.0, 1.0)
        self.init_buffer_objects()
        self.scale(self.SIZE, self.SIZE, self.SIZE)

    def change_colors(self, r=0.0, g=0.0, b=0.0):

        new_colors = []
        for index, color in enumerate(self.colors):
            if index % 3 == 0:
                new_colors.append(r)
            if index % 3 == 1:
                new_colors.append(g)
            if index % 3 == 2:
                new_colors.append(b)
        self.colors = new_colors


class Mars(Planet):

    SIZE = .53

    def __init__(self, model_matrix_id, texture_id):
        super(Mars, self).__init__(model_matrix_id, texture_id)
        self.change_colors(1.0, 0.0, 0.0)
        self.init_buffer_objects()
        self.scale(self.SIZE, self.SIZE, self.SIZE)

    def change_colors(self, r=0.0, g=0.0, b=0.0):

        new_colors = []
        for index, color in enumerate(self.colors):
            if index % 3 == 0:
                new_colors.append(r)
            if index % 3 == 1:
                new_colors.append(g)
            if index % 3 == 2:
                new_colors.append(b)
        self.colors = new_colors
