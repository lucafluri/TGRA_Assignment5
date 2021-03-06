
from OpenGL.GL import *
from OpenGL.GLU import*

from math import * # trigonometry

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc			= glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)


        self.uvLoc			= glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        # self.colorLoc			= glGetUniformLocation(self.renderingProgramID, "u_color")
        self.eyePosLoc			= glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        


        self.globalAmbientLoc			= glGetUniformLocation(self.renderingProgramID, "u_global_ambient")
        
        self.materialDiffuseLoc			= glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc			= glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialShininessLoc			= glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")
        
        self.diffuseTextureLoc			= glGetUniformLocation(self.renderingProgramID, "u_tex01")
        self.specularTextureLoc			= glGetUniformLocation(self.renderingProgramID, "u_tex02")
        
        self.usingTextureLoc			= glGetUniformLocation(self.renderingProgramID, "u_using_texture")

        # LIGHT 1
        self.light1PosLoc			    = glGetUniformLocation(self.renderingProgramID, "u_light1_position")
        self.light1DiffuseLoc			= glGetUniformLocation(self.renderingProgramID, "u_light1_diffuse")
        self.light1SpecularLoc			= glGetUniformLocation(self.renderingProgramID, "u_light1_specular")
        self.light1AmbientLoc			= glGetUniformLocation(self.renderingProgramID, "u_light1_ambient")

        # LIGHT 2
        self.light2PosLoc			    = glGetUniformLocation(self.renderingProgramID, "u_light2_position")
        self.light2DiffuseLoc			= glGetUniformLocation(self.renderingProgramID, "u_light2_diffuse")
        self.light2SpecularLoc			= glGetUniformLocation(self.renderingProgramID, "u_light2_specular")
        self.light2AmbientLoc			= glGetUniformLocation(self.renderingProgramID, "u_light2_ambient")

        # LIGHT 3
        self.light3PosLoc			    = glGetUniformLocation(self.renderingProgramID, "u_light3_position")
        self.light3DiffuseLoc			= glGetUniformLocation(self.renderingProgramID, "u_light3_diffuse")
        self.light3SpecularLoc			= glGetUniformLocation(self.renderingProgramID, "u_light3_specular")
        self.light3AmbientLoc			= glGetUniformLocation(self.renderingProgramID, "u_light3_ambient")

        # LIGHT 4
        self.light4PosLoc			    = glGetUniformLocation(self.renderingProgramID, "u_light4_position")
        self.light4DiffuseLoc			= glGetUniformLocation(self.renderingProgramID, "u_light4_diffuse")
        self.light4SpecularLoc			= glGetUniformLocation(self.renderingProgramID, "u_light4_specular")
        self.light4AmbientLoc			= glGetUniformLocation(self.renderingProgramID, "u_light4_ambient")




    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    # def set_solid_color(self, red, green, blue):
    #     glUniform4f(self.colorLoc, red, green, blue, 1.0)

    def set_global_ambient(self, color):
        glUniform4f(self.globalAmbientLoc, color.r, color.g, color.b, 1.0)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    # def set_material_diffuse(self, red, green, blue):
    #     glUniform4f(self.materialDiffuseLoc, red, green, blue, 1.0)

    def set_material_diffuse(self, color):
        glUniform4f(self.materialDiffuseLoc, color.r, color.g, color.b, 1.0)

    # def set_material_specular(self, red, green, blue):
    #     glUniform4f(self.materialSpecularLoc, red, green, blue, 1.0)

    def set_material_specular(self, color):
        glUniform4f(self.materialSpecularLoc, color.r, color.g, color.b, 1.0)

    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)

    def set_position_attribute(self, vertex_array):
        glUniform1f(self.usingTextureLoc, 1.0)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_diffuse_tex(self, number):
        glUniform1i(self.diffuseTextureLoc, number)

    def set_specular_tex(self, number):
        glUniform1i(self.specularTextureLoc, number)

    def set_attribute_buffers(self, vertex_buffer_id):
        glUniform1f(self.usingTextureLoc, 0.0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        glUniform1f(self.usingTextureLoc, 1.0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))

    # LIGHT 1
    def set_light1_position(self, pos, positional=1.0):
        glUniform4f(self.light1PosLoc, pos.x, pos.y, pos.z, positional)

    def set_light1_diffuse(self, color):
        glUniform4f(self.light1DiffuseLoc, color.r, color.g, color.b, 1.0)

    def set_light1_specular(self, color):
        glUniform4f(self.light1SpecularLoc, color.r, color.g, color.b, 1.0)

    def set_light1_ambient(self, color):
        glUniform4f(self.light1AmbientLoc, color.r, color.g, color.b, 1.0)

    # LIGHT 2
    def set_light2_position(self, pos, positional=1.0):
        glUniform4f(self.light2PosLoc, pos.x, pos.y, pos.z, positional)

    def set_light2_diffuse(self, color):
        glUniform4f(self.light2DiffuseLoc, color.r, color.g, color.b, 1.0)

    def set_light2_specular(self, color):
        glUniform4f(self.light2SpecularLoc, color.r, color.g, color.b, 1.0)

    def set_light2_ambient(self, color):
        glUniform4f(self.light2AmbientLoc, color.r, color.g, color.b, 1.0)

    # LIGHT 3
    def set_light3_position(self, pos, positional=1.0):
        glUniform4f(self.light3PosLoc, pos.x, pos.y, pos.z, positional)

    def set_light3_diffuse(self, color):
        glUniform4f(self.light3DiffuseLoc, color.r, color.g, color.b, 1.0)

    def set_light3_specular(self, color):
        glUniform4f(self.light3SpecularLoc, color.r, color.g, color.b, 1.0)

    def set_light3_ambient(self, color):
        glUniform4f(self.light3AmbientLoc, color.r, color.g, color.b, 1.0)

    # LIGHT 4
    def set_light4_position(self, pos, positional=1.0):
        glUniform4f(self.light4PosLoc, pos.x, pos.y, pos.z, positional)

    def set_light4_diffuse(self, color):
        glUniform4f(self.light4DiffuseLoc, color.r, color.g, color.b, 1.0)

    def set_light4_specular(self, color):
        glUniform4f(self.light4SpecularLoc, color.r, color.g, color.b, 1.0)

    def set_light4_ambient(self, color):
        glUniform4f(self.light4AmbientLoc, color.r, color.g, color.b, 1.0)