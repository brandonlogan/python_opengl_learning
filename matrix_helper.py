import glm
import math
import numpy


def translate(matrix, x, y, z):
    translation = glm.types.mat4x4.identity()
    translation.col3_vec4(glm.vec4(x, y, z, 1))
    return translation.mul_mat(matrix)


def scale(matrix, x, y, z):
    scaling = glm.mat4x4.identity()
    scaling.i00 = x
    scaling.i11 = y
    scaling.i22 = z
    scaling.i33 = 1
    return scaling.mul_mat(matrix)


def rotate_about_x(matrix, angle):
    angle = math.radians(angle)
    rotation = glm.types.mat4x4.identity()
    rotation.i11 = math.cos(angle)
    rotation.i12 = -math.sin(angle)
    rotation.i21 = math.sin(angle)
    rotation.i22 = math.cos(angle)
    return rotation.mul_mat(matrix)


def rotate_about_y(matrix, angle):
    angle = math.radians(angle)
    rotation = glm.types.mat4x4.identity()
    rotation.i00 = math.cos(angle)
    rotation.i02 = math.sin(angle)
    rotation.i20 = -math.sin(angle)
    rotation.i22 = math.cos(angle)
    return rotation.mul_mat(matrix)


def rotate_about_z(matrix, angle):
    angle = math.radians(angle)
    rotation = glm.types.mat4x4.identity()
    rotation.i00 = math.cos(angle)
    rotation.i01 = -math.sin(angle)
    rotation.i10 = math.sin(angle)
    rotation.i11 = math.cos(angle)
    return rotation.mul_mat(matrix)


def projection(fov, aspect_ratio, z_near, z_far):
    fov = math.radians(fov)
    f = 1.0 / math.tan(fov / 2.0)
    p_matrix = numpy.array([f / aspect_ratio, 0.0, 0.0, 0.0,
                            0.0, f, 0.0, 0.0,
                            0.0, 0.0, (z_far + z_near) / (z_near - z_far), -1.0,
                            0.0, 0.0, 2.0 * z_far * z_near / (z_near - z_far), 0.0], numpy.float32)
    return p_matrix


def identity():
    return [1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0]
