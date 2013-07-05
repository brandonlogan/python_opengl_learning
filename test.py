#!/usr/bin/env python
import OpenGL.GL as gl
import OpenGL.GLU as glu
from pygame.locals import *
import pygame
import math
import ode


class Level(object):
    def __init__(self, data, world, space):
        self.data = data
        self.display_list = gl.glGenLists(1)
        self.world = world
        self.space = space
        self.bodies = []
        self.geoms = []
        self.make_objects()

    def make_objects(self):
        for z, row in enumerate(self.data):
            for x, point in enumerate(row):
                geom = ode.GeomBox(space=self.space, lengths=(1,point,1))
                geom.setPosition((x+.5,1,z+.5))
                self.geoms.append(geom)
        print "Made %s objects" % self.space.getNumGeoms()

    def render(self):
        gl.glNewList(self.display_list, gl.GL_COMPILE)
        gl.glPushMatrix()
        gl.glColor3f(.5,.5,.5)
        #gl.glScaled(.3,.3,.3)
        gl.glBegin(gl.GL_QUADS)
        for z, row in enumerate(self.data):
            for x, point in enumerate(row):
                # top
                gl.glNormal3d(0,1,0)
                gl.glVertex3f(x,point,z)
                gl.glVertex3f(x+1,point,z)
                gl.glVertex3f(x+1,point,z+1)
                gl.glVertex3f(x,point,z+1)
            
                # bottom
                gl.glNormal3d(0,-1,0)
                gl.glVertex3f(x,0,z)
                gl.glVertex3f(x+1,0,z)
                gl.glVertex3f(x+1,0,z+1)
                gl.glVertex3f(x,0,z+1)

                # front
                gl.glNormal3d(0,0,1)
                gl.glVertex3f(x,0,z+1)
                gl.glVertex3f(x+1,0,z+1)
                gl.glVertex3f(x+1,point,z+1)
                gl.glVertex3f(x,point,z+1)

                # back
                gl.glNormal3d(0,0,-1)
                gl.glVertex3f(x,0,z)
                gl.glVertex3f(x+1,0,z)
                gl.glVertex3f(x+1,point,z)
                gl.glVertex3f(x,point,z)

                # left
                gl.glNormal3d(-1,0,0)
                gl.glVertex3f(x,0,z)
                gl.glVertex3f(x,point,z)
                gl.glVertex3f(x,point,z+1)
                gl.glVertex3f(x,0,z+1)

                # right
                gl.glNormal3d(1,0,0)
                gl.glVertex3f(x+1,0,z)
                gl.glVertex3f(x+1,point,z)
                gl.glVertex3f(x+1,point,z+1)
                gl.glVertex3f(x+1,0,z+1)
        gl.glEnd()
        gl.glPopMatrix()
        gl.glEndList()

    def call_list(self):
        gl.glCallList(self.display_list)


class Camera(object):
    def __init__(self, eye, target, up, rotation, world, space, perspective):
        self.eye = eye
        self.target = target
        self.up = up
        self.world = world
        self.space = space
        self.body = ode.Body(self.world)
        self.body.setGravityMode(True)
        self.body.setPosition(eye)
        self.mass = ode.Mass()
        self.mass.setSphere(1000, 1)
        self.geom = ode.GeomSphere(self.space, .75)
        self.geom.setBody(self.body)
        self.rotation = rotation
        self.perspective = perspective
        self.__last_position = self.body.getPosition()

    def move(self, m_x, m_y, m_z):
        z = m_z*math.cos(math.radians(self.rotation[0]))
        x = -m_z*math.sin(math.radians(self.rotation[0]))
        z += m_x*math.sin(math.radians(self.rotation[0]))
        x += m_x*math.cos(math.radians(self.rotation[0]))
        y = m_y
        self.body.addForce((x,y,z))

    def rotate(self, x, y):
        self.rotation[0] -= x
        self.rotation[1] -= y

    def collide(self, args, geom1, geom2):
        contacts = ode.collide(geom1, geom2)
        world,contact_group = args
        for c in contacts:
            c.setBounce(0.0)
            c.setMu(5000)
            j = ode.ContactJoint(world, contact_group, c)
            j.attach(geom1.getBody(), geom2.getBody())

    def is_dirty(self):
        return self.body.getPosition() == self.__last_position

    def get_position(self):
        return self.body.getPosition()

    def __camera_info(self):
        position = self.get_position()
        return [position[0],position[1],position[2],position[0],position[1],position[2]-.1]+self.up

    def dampen(self):
        vel = self.body.getAngularVel()
        nvel = [x*.99 for x in vel]
        self.body.setAngularVel(nvel)

    def update(self):
        if self.rotation[0] > 360: self.rotation[0] -= 360
        if self.rotation[0] < 0: self.rotation[0] += 360
        if self.rotation[1] > 90: self.rotation[1] = 90
        if self.rotation[1] < -90: self.rotation[1] = -90
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(*self.perspective)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glRotated(self.rotation[0],0,1,0)
        gl.glRotated(self.rotation[1],math.cos(math.radians(self.rotation[0])),0,
                  math.sin(math.radians(self.rotation[0])))
        glu.gluLookAt(*self.__camera_info())
        self.dampen()
        self.last_position = self.body.getPosition()


class Application(object):
    def __init__(self):
        self.size = (640,480)
        self.flags = OPENGL | DOUBLEBUF | HWSURFACE
        self.clear_color = (0., 0., 0., 1.)
        self.stop = False
        self.dirty_camera = False
        self.light_pos = [0,3,0,1]
        self.light_ambient = [0,0,0,1]
        self.light_diffuse = [.5,.5,.5,1]
        self.light_specular = [.5,.5,.5,1]
        self.last_mouse_pos = None
        self.clock = pygame.time.Clock()
        self.world = ode.World()
        self.world.setGravity((0,-9.81,0))
        self.world.setERP(0.8)
        self.world.setCFM(1E-5)
        self.space = ode.Space()
        self.contact_group = ode.JointGroup()
        self.floor = ode.GeomPlane(self.space, (0,1,0), 0)
        self.camera = None

    def start(self):
        self.init()
        self.load_camera()
        self.load_level()
        self.initGL()
        self.set_light()
        self.render()
        self.run()
        self.finish()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, self.flags)

    def initGL(self):
        gl.glViewport(0,0,640,480)
        self.move_camera()
        gl.glClearColor(*self.clear_color)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glEnable(gl.GL_NORMALIZE)
        gl.glMaterial(gl.GL_FRONT, gl.GL_AMBIENT, (.1,.1,.1,1))
        gl.glMaterial(gl.GL_FRONT, gl.GL_DIFFUSE, (1,1,1,1))
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)

    def set_light(self):
        gl.glEnable(gl.GL_LIGHT0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.camera.get_position())
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, self.light_ambient)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, self.light_diffuse)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, self.light_specular)

    def finish(self):
        print self.clock.get_fps()
        pygame.quit()

    def load_level(self):
        data = open('level.dat').read()
        data = data.split('\n')
        data = [[int(x) for x in line] for line in data if len(line) > 0]
        self.level = Level(data, self.world, self.space)

    def load_camera(self):
        self.camera = Camera([0,4,0],[0,4,-.1],[0,1,0],[0,0],self.world,
                             self.space, (90, float(self.size[0])/self.size[1], .1,100))

    def end(self):
        self.stop = True

    def render(self):
        self.level.render()

    def call_lists(self):
        self.level.call_list()

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                self.end()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.last_mouse_pos = pygame.mouse.get_pos()
                    pygame.mouse.set_visible(False)
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.last_mouse_pos = None
                    pygame.mouse.set_visible(True)
            if event.type == MOUSEMOTION:
                if self.last_mouse_pos is not None: self.handle_mouse()

    def move_camera(self):
        self.dirty_camera = False
        self.camera.update()
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.camera.get_position())

    def move(self, m_x, m_y, m_z):
        self.camera.move(m_x,m_y,m_z)

    def handle_keys(self, keys):
        if keys[K_COMMA] or keys[K_a] or\
                keys[K_o] or keys[K_e] or\
                keys[K_SPACE] or keys[K_LSHIFT]:
            self.dirty_camera = True
        if keys[K_COMMA]:
            self.move(0,0,-10)
        if keys[K_a]:
            self.move(-10,0,0)
        if keys[K_o]:
            self.move(0,0,10)
        if keys[K_e]:
            self.move(10,0,0)
        if keys[K_SPACE]:
            self.move(0,50,0)
        if keys[K_LSHIFT]:
            self.move(0,-10,0)

    def clear_screen(self):
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT | gl.GL_COLOR_BUFFER_BIT)

    def update_screen(self):
        pygame.display.flip()

    def sync(self):
        gl.glFinish()

    def handle_camera(self):
        self.move_camera()

    def handle_world(self):
        self.space.collide((self.world,self.contact_group), self.camera.collide)
        self.world.step(1/60.)
        self.contact_group.empty()

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        diff = [(self.last_mouse_pos[x]-mouse_pos[x])/3. for x in range(2)]
        self.camera.rotate(*diff)
        self.dirty_camera = True
        pygame.mouse.set_pos(self.last_mouse_pos)

    def run(self):
        while not self.stop:
            self.clock.tick()
            self.handle_events(pygame.event.get())
            self.handle_keys(pygame.key.get_pressed())
            self.handle_world()
            self.handle_camera()
            self.clear_screen()
            self.call_lists()
            self.update_screen()
            self.sync()

if __name__ == '__main__':
    app = Application()
    app.start()