# renderer.py
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import config

class Renderer:
    def __init__(self):
        self.init_gl()

    def init_gl(self):
        """Initialize OpenGL settings"""
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))
        
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        self.set_perspective()

    def set_perspective(self):
        """Set up the perspective projection"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (config.DISPLAY_WIDTH/config.DISPLAY_HEIGHT), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_textured_cube(self, x, y, z, color, is_floor=False, scale=1.0):
        vertices = [
            [x-0.5*scale, y-0.5*scale, z-0.5*scale], [x+0.5*scale, y-0.5*scale, z-0.5*scale],
            [x+0.5*scale, y+0.5*scale, z-0.5*scale], [x-0.5*scale, y+0.5*scale, z-0.5*scale],
            [x-0.5*scale, y-0.5*scale, z+0.5*scale], [x+0.5*scale, y-0.5*scale, z+0.5*scale],
            [x+0.5*scale, y+0.5*scale, z+0.5*scale], [x-0.5*scale, y+0.5*scale, z+0.5*scale]
        ]

        if is_floor:
            glBegin(GL_QUADS)
            glColor3f(*color)
            glNormal3f(0, 1, 0)
            glVertex3f(x-0.5*scale, y-0.5*scale, z-0.5*scale)
            glVertex3f(x+0.5*scale, y-0.5*scale, z-0.5*scale)
            glVertex3f(x+0.5*scale, y-0.5*scale, z+0.5*scale)
            glVertex3f(x-0.5*scale, y-0.5*scale, z+0.5*scale)
            glEnd()
        else:
            surfaces = (
                (0,1,2,3), (3,2,6,7), (7,6,5,4),
                (4,5,1,0), (1,5,6,2), (4,0,3,7)
            )
            
            normals = [
                (0,0,-1), (0,1,0), (0,0,1),
                (0,-1,0), (1,0,0), (-1,0,0)
            ]

            glBegin(GL_QUADS)
            glColor3f(*color)
            for i, surface in enumerate(surfaces):
                glNormal3f(*normals[i])
                for vertex in surface:
                    glVertex3fv(vertices[vertex])
            glEnd()

    def setup_camera(self, player_pos, player_angle, camera_mode):
        """Set up the camera position based on mode"""
        glLoadIdentity()
        
        if camera_mode == "far":
            gluLookAt(
                player_pos[0] + config.CAMERA_DISTANCE * math.sin(player_angle),
                config.CAMERA_DISTANCE,
                player_pos[2] + config.CAMERA_DISTANCE * math.cos(player_angle),
                player_pos[0], 0, player_pos[2],
                0, 1, 0
            )
        else:
            look_x = player_pos[0] + math.sin(player_angle)
            look_z = player_pos[2] + math.cos(player_angle)
            gluLookAt(
                player_pos[0], player_pos[1], player_pos[2],
                look_x, player_pos[1], look_z,
                0, 1, 0
            )