from OpenGL import GL
import OpenGL.GL.shaders
import pygame
import sys
import os
import glm
import matrix_helper
from test_models import Cube, Suzanne, Sun, Earth, Mars


SIZE_FLOAT = VERT_COMPONENTS = 4

#Shaders:
with open(os.path.join("shader.vert"), 'r') as myfile:
    VERT = myfile.read()
with open(os.path.join("shader.frag"), 'r') as myfile:
    FRAG = myfile.read()


class Scene:

    MOVE_SPEED = .2
    ROT_X = ROT_Y = ROT_Z = 1

    def __init__(self):
        self.shader = GL.shaders.compileProgram(GL.shaders.compileShader(VERT, GL.GL_VERTEX_SHADER),
                                                GL.shaders.compileShader(FRAG, GL.GL_FRAGMENT_SHADER))

        GL.glClearColor(0, 0, 0, 1)
        self.projection_matrix_id = GL.glGetUniformLocation(self.shader, "projectionMatrix")
        self.view_matrix_id = GL.glGetUniformLocation(self.shader, "viewMatrix")
        self.model_matrix_id = GL.glGetUniformLocation(self.shader, "modelMatrix")
        self.texture_id = GL.glGetUniformLocation(self.shader, "myTextureSampler")

        self.reshape(500, 500)
        self.view_mat = glm.types.mat4x4.identity()
        self.view_mat = matrix_helper.translate(self.view_mat, 0, 0, -80)
        self.sun = Sun(self.model_matrix_id, self.texture_id)
        self.earth = Earth(self.model_matrix_id, self.texture_id)
        self.earth.translate(0, 0, 40)
        self.mars = Mars(self.model_matrix_id, self.texture_id)
        self.mars.translate(0, 0, 60)

    def display(self, left=False, right=False, up=False, down=False, forward=False, backward=False):
        x = y = z = 0
        if left:
            x = self.MOVE_SPEED
        if right:
            x = -self.MOVE_SPEED
        if up:
            y = -self.MOVE_SPEED
        if down:
            y = self.MOVE_SPEED
        if forward:
            z = self.MOVE_SPEED
        if backward:
            z = -self.MOVE_SPEED

        self.sun.rotate(1, about_y=True)
        self.earth.rotate(.3, about_y=True)
        self.mars.rotate(.2, about_y=True)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)
        GL.glEnable(GL.GL_CULL_FACE)

        projection_mat = glm.types.mat4x4.perspective(40.0, 4.0 / 4.0, 0.1, 1000.0)
        # view_mat = glm.types.mat4x4.look_at(self.cam_vec,
        #                                     self.cam_center,
        #                                     self.cam_up)
        self.view_mat = matrix_helper.translate(self.view_mat, x, y, z)

        GL.glUseProgram(self.shader)
        GL.glUniformMatrix4fv(self.projection_matrix_id, 1, False, projection_mat.to_tuple())
        GL.glUniformMatrix4fv(self.view_matrix_id, 1, False, self.view_mat.to_tuple())

        self.sun.display()
        self.earth.display()
        self.mars.display()

        GL.glUseProgram(0)

    def reshape(self, width, height):
        GL.glViewport(0, 0, width, height)


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pygame.display.set_mode((500, 500), pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF)
    MyClock = pygame.time.Clock()
    MyGL = Scene()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        MyGL.display(left=keys[pygame.K_a] or keys[pygame.K_LEFT],
                     right=keys[pygame.K_d] or keys[pygame.K_RIGHT],
                     up=keys[pygame.K_r] or keys[pygame.K_HOME],
                     down=keys[pygame.K_f] or keys[pygame.K_END],
                     forward=keys[pygame.K_w] or keys[pygame.K_UP],
                     backward=keys[pygame.K_s] or keys[pygame.K_DOWN])
        MyGL.display()
        pygame.display.flip()
        MyClock.tick(65)


if __name__ == '__main__':
    main()