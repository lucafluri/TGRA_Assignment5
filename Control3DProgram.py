
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

import obj_3D_loading

class GraphicsProgram3D:

    def __init__(self):

        pygame.init() 
        pygame.display.set_caption('TGRA Assignment 5 -- Luca Fluri')

        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()  
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()

        self.view_matrix.look(Point(1, 0, 4), Point(10, 0, 4), Vector(0, 0, 1))

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.fov = 90
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.projection_matrix.set_perspective(120, 800/600, 0.001, 10 )
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

        self.sphere = OptimizedSphere(24, 48)

        # self.obj_model = obj_3D_loading.load_obj_file(sys.path[0] + "/models", "smooth_sphere.obj")

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.W_key_down = False  
        self.S_key_down = False  
        self.A_key_down = False  
        self.D_key_down = False  
        self.E_key_down = False  
        self.Q_key_down = False  
        self.T_key_down = False  
        self.G_key_down = False
        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.UP_key_down = False
        self.DOWN_key_down = False


        self.white_background = False

        self.texture_id01 = self.load_texture("/textures/tex01.png")
        self.texture_id02 = self.load_texture("/textures/tex02.jpg")

        self.fr_ticker = 0
        self.fr_sum = 0

    def load_texture(self, path_string):
        # Loading and Binding Texture
        surface = pygame.image.load(sys.path[0] + path_string)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0


        self.angle += (pi * delta_time) * 180.0/pi
        # if self.angle > 180:
        #     self.angle -= 180


        if self.W_key_down:
            self.view_matrix.slide(0, 0, -10 * delta_time)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, 10 * delta_time)
        if self.A_key_down:
            self.view_matrix.slide(-10 * delta_time, 0, 0)
            # self.view_matrix.yaw(180 * delta_time)
        if self.D_key_down:
            self.view_matrix.slide(10 * delta_time, 0, 0)
            # self.view_matrix.yaw(-180 * delta_time)
        if self.LEFT_key_down:
            self.view_matrix.yaw(90 * delta_time)
        if self.RIGHT_key_down:
            self.view_matrix.yaw(-90 * delta_time)
        if self.UP_key_down:
            self.view_matrix.pitch(90 * delta_time)
        if self.DOWN_key_down:
            self.view_matrix.pitch(-90 * delta_time)

        if self.T_key_down:
            self.fov -= 1.5 * delta_time
        if self.G_key_down:
            self.fov += 1.5 * delta_time

        
        
    

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800/600, 0.001, 10 )
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)

        self.shader.set_light_position(self.view_matrix.eye)
        # self.shader.set_light_position(Point(0.0, 0.0, 50.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)
        self.shader.set_light_ambient(0.1, 0.1, 0.05)

        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(5.0)


        self.model_matrix.load_identity()

        self.shader.set_material_diffuse(Color(1.0, 1.0, 0.0))

        self.cube.set_vertices(self.shader)
        # self.sphere.set_vertices(self.shader)

        # # Floor
        # self.shader.set_material_diffuse(1.0, 1.0, 1.0)
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.0, 0.0 , 0.0)  
        # self.model_matrix.add_scale(100, 100, 0.1)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # # Walls
        # for wall in self.walls:
        #     x, y, xlength, ylength = wall
        #     if self.checkWallCollision(x, y, xlength, ylength):
        #         self.drawWall(x, y, xlength, ylength, [0.0, 1.0, 0.0])
        #     else:
        #         self.drawWall(x, y, xlength, ylength)

        # Rotating Cube
        # if self.checkWallCollision(8, 0, sqrt(2), sqrt(2)):
        #     self.weirdObjectColor=[random(), random(), random()]
        # self.drawWeirdRotatingObject()

        # glActiveTexture(GL_TEXTURE0)
        # glBindTexture(GL_TEXTURE_2D, self.tex_id)
        # self.shader.set_diffuse_texture(self.tex_id)
        

        #####################################################
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        self.shader.set_diffuse_tex(0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        self.shader.set_specular_tex(1)

        
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(10)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, 0.0 , 3.0)  
        self.model_matrix.add_scale(1, 1, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()


        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        self.shader.set_diffuse_tex(0) 
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(10)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, 0.0 , 5.0)  
        self.model_matrix.add_scale(1, 1, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # glActiveTexture(GL_TEXTURE31)
        # glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        # self.sphere.set_vertices(self.shader)
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(10)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, 0.0 , 0.0)  
        self.model_matrix.add_scale(1, 1, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        pygame.display.flip()

        

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_e:
                        self.E_key_down = True
                    if event.key == K_q:
                        self.Q_key_down = True
                    if event.key == K_t:
                        self.T_key_down = True
                    if event.key == K_g:
                        self.G_key_down = True
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_DOWN:
                        self.DOWN_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_e:
                        self.E_key_down = False
                    if event.key == K_q:
                        self.Q_key_down = False
                    if event.key == K_t:
                        self.T_key_down = False
                    if event.key == K_g:
                        self.G_key_down = False
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_DOWN:
                        self.DOWN_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()