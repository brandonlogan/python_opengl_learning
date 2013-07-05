from OpenGL import GL
import glm
import numpy
import matrix_helper
import texture_helper
import ply_loader


class Model(object):

    SIZE_FLOAT = 4

    model_matrix = None
    vertex_buff = None
    color_buff = None
    vertices = None
    colors = None
    uv_data = None
    texture_path = None
    uv_buffer = None
    faces = None
    vertex_normals = None

    def __init__(self, model_matrix_id, texture_id, ply_path=None):
        self.model_matrix_id = model_matrix_id
        self.model_matrix = glm.mat4x4.identity()
        if ply_path is not None:
            ply_data = ply_loader.load_ply(ply_path)
            self.vertices = ply_data['vertices']
            self.vertex_normals = ply_data['normals']
            self.colors = []
            for color in ply_data['colors']:
                if color == 0:
                    self.colors.append(color)
                else:
                    self.colors.append(float(color)/float(255))

        # self.texture, self.texture_data = texture_helper.load_texture(self.texture_path)
        # self.texture_id = texture_id

    def init_buffer_objects(self):
        self.vertex_buff = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_buff)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(self.vertices) * Model.SIZE_FLOAT,
                        numpy.array(self.vertices, dtype=numpy.float32), GL.GL_STATIC_DRAW)

        self.init_color()

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def init_color(self):
        self.color_buff = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.color_buff)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(self.colors) * Model.SIZE_FLOAT,
                        numpy.array(self.colors, dtype=numpy.float32), GL.GL_STATIC_DRAW)

    def init_texture(self):
        self.texture_buff = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_buff)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, self.texture.get_width(), self.texture.get_height(), 0,
                        GL.GL_BGR, GL.GL_UNSIGNED_BYTE, self.texture_data)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)

        self.uv_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.uv_buffer)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(self.uv_data), numpy.array(self.uv_data, dtype=numpy.float32),
                        GL.GL_STATIC_DRAW)

    def translate(self, x, y, z):
        self.model_matrix = matrix_helper.translate(self.model_matrix, x, y, z)

    def rotate(self, angle, about_x=False, about_y=False, about_z=False):
        if about_x:
            self.model_matrix = matrix_helper.rotate_about_x(self.model_matrix, angle)
        if about_y:
            self.model_matrix = matrix_helper.rotate_about_y(self.model_matrix, angle)
        if about_z:
            self.model_matrix = matrix_helper.rotate_about_z(self.model_matrix, angle)

    def scale(self, x, y, z):
        self.model_matrix = matrix_helper.scale(self.model_matrix, x, y, z)

    def display(self):
        GL.glUniformMatrix4fv(self.model_matrix_id, 1, False, self.model_matrix.to_tuple())

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_buff)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 4, GL.GL_FLOAT, False, 0, None)

        self.display_color()

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices) / 4)
        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)

    def display_color(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.color_buff)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)

    def display_texture(self):
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_buff)
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, False, 0, None)
        GL.glUniform1i(self.texture_id, 0)
