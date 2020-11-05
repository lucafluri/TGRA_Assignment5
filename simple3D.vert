attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

// uniform vec4 u_color;

uniform vec4 u_eye_position;

varying vec2 v_uv;
varying vec4 v_normal;


uniform vec4 u_light1_position;
uniform vec4 u_light2_position;
uniform vec4 u_light3_position;
uniform vec4 u_light4_position;

// varying vec4 v_color;  //Leave the varying variables alone to begin with
varying vec4 v_s1;
varying vec4 v_h1;
varying vec4 v_s2;
varying vec4 v_h2;
varying vec4 v_s3;
varying vec4 v_h3;
varying vec4 v_s4;
varying vec4 v_h4;


void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// UB coords sent into per-pixel use
	v_uv = a_uv;

		
	// Local Coordinates

	position = u_model_matrix * position;
	v_normal = normalize(u_model_matrix * normal);

	vec4 v = normalize(u_eye_position - position);

	// Global Coordinates
	// Check for positional Light: 0:directional, 1:positional

	// LIGHT 1
	v_s1 = u_light1_position;
	if(u_light1_position[3] == 1.0){
		v_s1 = normalize(u_light1_position - position);
	}
	v_h1 = normalize(v_s1 + v);

	// LIGHT 2
	v_s2 = u_light2_position;
	if(u_light2_position[3] == 1.0){
		v_s2 = normalize(u_light2_position - position);
	}
	v_h2 = normalize(v_s2 + v);

	// LIGHT 3
	v_s3 = u_light3_position;
	if(u_light3_position[3] == 1.0){
		v_s3 = normalize(u_light3_position - position);
	}
	v_h3 = normalize(v_s3 + v);

	// LIGHT 4
	v_s4 = u_light4_position;
	if(u_light4_position[3] == 1.0){
		v_s4 = normalize(u_light4_position - position);
	}
	v_h4 = normalize(v_s4 + v);

	

	// float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
	// float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	// v_color = (light_factor_1 + light_factor_2) * u_color; // ### --- Change this vector (pure white) to color variable --- #####

	position = u_view_matrix * position;
	// Eye Coordinates
	position = u_projection_matrix * position;
	// Clip Coordinates

	gl_Position = position;
}