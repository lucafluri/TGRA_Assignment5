
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

        # Turn left
        self.view_matrix.yaw(90)


        self.cube = Cube()

        self.sphere = OptimizedSphere(24, 48)

        self.obj_model = obj_3D_loading.load_obj_file(sys.path[0] + "/models", "smooth_sphere.obj")

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

        self.startTime = time.time()

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

    def lerp(self, a, b, t):
        return a.__mul__(1-t) + b.__mul__(t)

    def getCurrentTime(self):
        # Calc current Program time
        return time.time() - self.startTime
    
    def getT(self, startT, endT):
        # Calc current Program time
        current = self.getCurrentTime()
        if current < startT:
            return 0
        elif current > endT:
            return 1
        else:
            return (current - startT) / (endT - startT)

    # Takes 4 Vectors
    def bezier4(self, p1, p2, p3, p4, t):
        # return  p1.__mul__((1-t)**3) + p2.__mul__(3*(1-t)**2 * t) + p3.__mul__(3*(1-t)*t**2) + p4.__mul__(t**3)
        return self.lerp(self.lerp(self.lerp(p1, p2, t), self.lerp(p2, p3, t), t), self.lerp(self.lerp(p2, p3, t), self.lerp(p3, p4, t), t), t)

    # Recursive Bezier Function
    def bezier(self, vectors, t):
        vectors_new = []
        if(len(vectors) > 2):
            for i in range(len(vectors) - 1):
                vectors_new.append(self.lerp(vectors[i], vectors[i + 1], t))
            return self.bezier(vectors_new, t)
        else:
            return self.lerp(vectors[0], vectors[1], t)
        
    def bezierSpline(self, vectors, t):
        # Build Segments
        # Add first 4 points
        arrays = [vectors[:4]]
        vectors = vectors[4:]

        # Add subsequent 2 points
        for _ in range((int) (len(vectors) / 2)):
            arrays.append(vectors[:2])
            vectors = vectors[2:]
        arrays.append(vectors)


        for i in range(len(arrays)):
            if i == 0:
                continue
            if(len(arrays[i]) == 0):
                continue
            arrays[i].insert(0, arrays[i-1][3])
            arrays[i].insert(1, arrays[i][0] + (arrays[i-1][3] - arrays[i-1][2]))

        # Flatten List
        flat = []
        for arr in arrays:
            flat += arr

        return self.bezier(flat, t)


    





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

        self.projection_matrix.set_perspective(self.fov, 800/600, 0.001, 50 )

        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_light_position(self.view_matrix.eye)
        # self.shader.set_light_position(Point(0.0, 0.0, 50.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)
        self.shader.set_light_ambient(0.15, 0.15, 0.15)



        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(5.0)


        self.model_matrix.load_identity()

        self.shader.set_material_diffuse(Color(1.0, 1.0, 0.0))

        self.cube.set_vertices(self.shader)
        # self.sphere.set_vertices(self.shader)


        
        # Mid Wall
        # glActiveTexture(GL_TEXTURE31)
        # glBindTexture(GL_TEXTURE_2D, 0)
        self.shader.set_specular_tex(31)
        self.shader.set_diffuse_tex(31)
        self.shader.set_material_diffuse(Color(0.25, 0.25, 0.25))
        self.shader.set_material_specular(Color(0.5, 0.5, 0.5))
        self.shader.set_material_shininess(0.25)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(10.0, 8.0 , 4.0)  
        self.model_matrix.add_scale(20, 1, 8)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()


        # Move Camera to end of wall
        bezCamera1 = self.bezierSpline([Vector(0, 0, 0), Vector(5,-2, 0), Vector(10, -5, 2), Vector(15, -3, 0), Vector(17, -1, 0), Vector(20, 8, 5)], self.getT(0, 15))
        self.view_matrix.eye = Point(bezCamera1.x, bezCamera1.y, bezCamera1.z)


        
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

        # BEZIER TESTS
        bez = self.bezierSpline([Vector(1, 0, 0), Vector(3,0, 0), Vector(3, 0, 5), Vector(4, 3, 5), Vector(0, 0, 0), Vector(8, 0, 0), Vector(8, 0, 10), Vector(5, 0, 5)], self.getT(4, 10))
        # print(bez.x, bez.y, bez.z)
        glActiveTexture(GL_TEXTURE31)
        # glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        # self.sphere.set_vertices(self.shader)
        self.shader.set_material_diffuse(Color(1.0, 1.0, 0.0))
        self.shader.set_material_shininess(10)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(bez.x, bez.y, bez.z)  
        self.model_matrix.add_scale(1, 1, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        for i in range(8):
            self.model_matrix.push_matrix()
            self.model_matrix.add_rotation_x(self.angle * 0.74324 + i * 45)
            self.model_matrix.add_translation(8, 2, 0)
            self.model_matrix.add_rotation_x(-self.angle * 0.74324 + i * 45)
            self.model_matrix.add_scale(1.0, 1.0, 1.0)
            self.shader.set_model_matrix(self.model_matrix.matrix)

            self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
            self.obj_model.draw(self.shader)
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