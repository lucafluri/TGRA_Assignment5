
varying vec4 v_normal;

varying vec2 v_uv;

uniform float u_using_texture;

uniform vec4 u_global_ambient;


uniform vec4 u_light1_diffuse;
uniform vec4 u_light1_specular;
uniform vec4 u_light1_ambient;
varying vec4 v_s1;
varying vec4 v_h1;

uniform vec4 u_light2_diffuse;
uniform vec4 u_light2_specular;
uniform vec4 u_light2_ambient;
varying vec4 v_s2;
varying vec4 v_h2;

uniform vec4 u_light3_diffuse;
uniform vec4 u_light3_specular;
uniform vec4 u_light3_ambient;
varying vec4 v_s3;
varying vec4 v_h3;

uniform vec4 u_light4_diffuse;
uniform vec4 u_light4_specular;
uniform vec4 u_light4_ambient;
varying vec4 v_s4;
varying vec4 v_h4;


uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform vec4 u_mat_emission;
uniform float u_mat_shininess;

uniform sampler2D u_tex01;
uniform sampler2D u_tex02;

void main(void)
{
	vec4 mat_diffuse = u_mat_diffuse;
	vec4 mat_specular = u_mat_specular;
	if(u_using_texture == 1.0){
		mat_diffuse = u_mat_diffuse * texture2D(u_tex01, v_uv);
		mat_specular = u_mat_specular * texture2D(u_tex02, v_uv);
	}

	float n_len = length(v_normal);

	// LIGHT 1
	float lambert1 = max(dot(v_normal, v_s1) / (n_len*length(v_s1)), 0);
	float phong1 = max(dot(v_normal, v_h1) / (n_len*length(v_h1)), 0);

	vec4 light1Color =  u_light1_ambient + (u_light1_diffuse * mat_diffuse) * lambert1
				+ (u_light1_specular * u_mat_specular) * pow(phong1, u_mat_shininess); 

	// LIGHT 2
	float lambert2 = max(dot(v_normal, v_s2) / (n_len*length(v_s2)), 0);
	float phong2 = max(dot(v_normal, v_h2) / (n_len*length(v_h2)), 0);

	vec4 light2Color =  u_light2_ambient + (u_light2_diffuse * mat_diffuse) * lambert2
				+ (u_light2_specular * u_mat_specular) * pow(phong2, u_mat_shininess); 

	// LIGHT 3
	float lambert3 = max(dot(v_normal, v_s3) / (n_len*length(v_s3)), 0);
	float phong3 = max(dot(v_normal, v_h3) / (n_len*length(v_h3)), 0);

	vec4 light3Color =  u_light3_ambient + (u_light3_diffuse * mat_diffuse) * lambert3
				+ (u_light3_specular * u_mat_specular) * pow(phong3, u_mat_shininess); 

	// LIGHT 4
	float lambert4 = max(dot(v_normal, v_s4) / (n_len*length(v_s4)), 0);
	float phong4 = max(dot(v_normal, v_h4) / (n_len*length(v_h4)), 0);

	vec4 light4Color =  u_light4_ambient + (u_light4_diffuse * mat_diffuse) * lambert4
				+ (u_light4_specular * u_mat_specular) * pow(phong4, u_mat_shininess); 






	gl_FragColor = u_global_ambient * mat_diffuse + light1Color + light2Color + light3Color + light4Color;



    // Tmp
    // gl_FragColor.r = gl_FragColor.r + v_uv.x;
    
}