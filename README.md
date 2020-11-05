# TGRA Assignment 5
by Luca Fluri (luca20)



## Running the Animation

to run simply execute the Control3DProgram python script.

`python Control3DProgram.py`



## Submission Description

My Submission is rather straightforward. I went for an Animation since I more or less did User Interaction in the last assignment and I also didn't have that much time to invest in this project sadly.

There are no user inputs and the animation is 35 seconds long. After that the window doesn't close. It seemed rather abrupt so I chose to leave it running.

The Animation consists of 1 Scene several Objects (Stationary and moving), a total of 4 lights (1 positional and 3 directional and again stationary and moving). Objects and the Camera are animated through a simple lerp and Bezier splines. Most longer movements are done with Bezier splines.



I also implemented a lighting model, which is discussed later on. (Assignment 4)



**Implemented**:

- Lighting (color, position and motion)
- Textures (although very rough I have to admit)
- Mesh Objects (Can be loaded in and used but not textured)
- Motion along smooth curves (I used Bezier Splines) (Camera and Objects)
- Camera Cuts (There is only one cut but several animation of the camera)



## Lighting Model Report (Assignment 4)

My Lighting Model includes 4 Lights (can be both directional or positional depending on the 4th vector value). There is global ambience and each light has diffuse, specular and ambience values. For the material I included diffuse, specular and shininess. I first included emission values as well, but discarded them since I never used them. There is also a diffuse and a specular texture available to configure.



### Shader Description

#### Vertex Shader

```glsl
attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;
```

First the position, normal and uv vector per Vertex are initialized then the 3 main matrices.

```glsl
uniform vec4 u_eye_position;

varying vec2 v_uv;
varying vec4 v_normal;
```

**eye_position**: Position of the camera

**v_uv** & **v_normal**: varying uv and normal vectors which is used in the fragment shader

```glsl
uniform vec4 u_light1_position;
uniform vec4 u_light2_position;
uniform vec4 u_light3_position;
uniform vec4 u_light4_position;	
```

All Light positions are initialized, these are used in the vertex shader, mainly to calculate the s vector ( the vector from the surface to the light) depending on whether it's a directional or positional light.

```glsl
	v_uv = a_uv;
```

the uv vector isn't changed and directly set for the fragment shader to use.

```glsl
position = u_model_matrix * position;
v_normal = normalize(u_model_matrix * normal);

vec4 v = normalize(u_eye_position - position);

```

Position and normal vector are set in to global Coordinates
The v vector (surface to eye) is calculated

```glsl
// LIGHT 1
	v_s1 = u_light1_position;
	if(u_light1_position[3] == 1.0){
		v_s1 = normalize(u_light1_position - position);
	}
	v_h1 = normalize(v_s1 + v);
```

All s and h vectors (average vector between the light vector
s and the camera vector v ) are calculated. v_s is set in directional or positional mode.



#### Fragment Shader

All other light model (previously mentioned) are initialized.

```glsl
vec4 mat_diffuse = u_mat_diffuse;
vec4 mat_specular = u_mat_specular;
if(u_using_texture == 1.0){
	mat_diffuse = u_mat_diffuse * texture2D(u_tex01, v_uv);
	mat_specular = u_mat_specular * texture2D(u_tex02, v_uv);
}
```

Diffuse and Specular Textures are applied if needed.

```glsl
// LIGHT 1
float lambert1 = max(dot(v_normal, v_s1) / (n_len*length(v_s1)), 0);
float phong1 = max(dot(v_normal, v_h1) / (n_len*length(v_h1)), 0);

vec4 light1Color =  u_light1_ambient + (u_light1_diffuse * mat_diffuse) * lambert1 + (u_light1_specular * u_mat_specular) * pow(phong1, u_mat_shininess); 

```

individual lambert, phong and then the light colors are calculated per Light

```glsl
gl_FragColor = u_global_ambient * u_mat_diffuse + light1Color + light2Color + light3Color + light4Color;

```

These are then added together with the global ambience to get to complete fragment color.



Most of the work is done in the fragment shader, this way we have a more uniform and even specular effect for instance.