
varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

uniform float u_using_texture;


uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;
uniform vec4 u_light_ambient;


uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
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

	float s_len = length(v_s);
	float h_len = length(v_h);
	float n_len = length(v_normal);
	float lambert = max(dot(v_normal, v_s) / (n_len*s_len), 0);
	float phong = max(dot(v_normal, v_h) / (n_len*h_len), 0);

	gl_FragColor =  u_light_ambient + (u_light_diffuse * mat_diffuse) * lambert
				+ (u_light_specular * u_mat_specular) * pow(phong, u_mat_shininess); 


    // Tmp
    // gl_FragColor.r = gl_FragColor.r + v_uv.x;
    
}