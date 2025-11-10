#version 430

uniform sampler2D surface;
uniform sampler2D hud_surf;
uniform sampler2D crt_filter_tex;
uniform sampler2D background_tex;
uniform sampler2D ui_surf;
uniform float time;
uniform vec2 scroll;
uniform ivec2 dimensions;
uniform vec2 border_discard;
uniform float saturation = 0.65;
uniform float crt_effect = 1.0;

out vec4 f_color;
in vec2 uv;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

float noise(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

vec3 chromaticAberration(sampler2D tex, vec2 uv, float amount) {
    vec2 offset = (uv - 0.5) * amount * 0.001;
    return vec3(
        texture(tex, uv + offset).r,
        texture(tex, uv).g,
        texture(tex, uv - offset).b
    );
}

vec3 processBackground(vec2 uv) {
    vec2 distorted_uv = uv;
    float wave_x = sin(uv.y * 15.0 + time * 1.8) * 0.004;
    float wave_y = cos(uv.x * 18.0 + time * 2.2) * 0.004;
    distorted_uv += vec2(wave_x, wave_y);
    vec2 center = uv - 0.5;
    float breathe = sin(time * 1.5) * 0.008 + 1.0;
    distorted_uv = center * breathe + 0.5;
    vec3 bg_color = texture(background_tex, distorted_uv).rgb;
    vec2 ca_offset = center * 0.003;
    bg_color.r = texture(background_tex, distorted_uv + ca_offset).r;
    bg_color.b = texture(background_tex, distorted_uv - ca_offset).b;
    float fog = sin(uv.x * 8.0 + time * 0.5) * cos(uv.y * 6.0 - time * 0.3) * 0.05 + 0.95;
    bg_color *= fog;
    float vignette_bg = 1.0 - length(center) * 0.4;
    bg_color *= vignette_bg;
    bg_color *= vec3(1.02, 0.88, 0.85);
    bg_color *= 0.7;
    return bg_color;
}

float vignette(vec2 uv) {
    vec2 center = uv - vec2(0.5);
    float noiseVal = noise(uv * 3.0 + time * 0.1) * 0.15;
    float dist = length(center * vec2(1.0 + noiseVal * 0.3, 1.0 - noiseVal * 0.2));
    return 1.0 - smoothstep(0.2, 0.8 + noiseVal * 0.1, dist);
}

void main() {
    vec2 uv_range = vec2(1.0 / (1.0 - border_discard.x), 1.0 / (1.0 - border_discard.y));
    vec2 cropped_uv = vec2(uv.x * uv_range.x - (uv_range.x - 1.0) * 0.5, uv.y * uv_range.y - (uv_range.y - 1.0) * 0.5);
    float breathe = sin(time * 2.0) * 0.001;
    vec2 distorted_uv = cropped_uv;
    distorted_uv -= 0.5;
    distorted_uv *= 1.0 + breathe;
    distorted_uv += 0.5;
    distorted_uv.x += sin(distorted_uv.y * 30.0 + time * 3.0) * 0.00025;
    distorted_uv.y += cos(distorted_uv.x * 25.0 + time * 2.5) * 0.00025;
    vec3 base_color = chromaticAberration(surface, distorted_uv, 0.3);
    vec4 ui_color = texture(hud_surf, cropped_uv);
    vec3 bg_processed = processBackground(distorted_uv);
    base_color = mix(bg_processed, base_color, 0.85);
    f_color = vec4(base_color, 1.0);
    f_color = f_color * (1.0 - ui_color.a) + vec4(ui_color.rgb * ui_color.a, 1.0);
    ivec2 filter_uv = ivec2(cropped_uv * dimensions);
    ivec2 tex_size = textureSize(crt_filter_tex, 0);
    vec2 filter_coord = (vec2(filter_uv) + 0.5) / vec2(tex_size);
    vec3 crt_color = texture(crt_filter_tex, filter_coord).rgb;
    f_color.rgb = f_color.rgb * crt_color * 0.7 * crt_effect * 0.4 + f_color.rgb * (1.0 - 0.5 * (crt_effect * 0.4));
    float grain = (random(cropped_uv + time * 0.01) - 0.5) * 0.1;
    f_color.rgb += grain;
    f_color.rgb = pow(f_color.rgb, vec3(1.15));
    vec3 blood_tint = vec3(1.05, 0.9, 0.85);
    f_color.rgb *= blood_tint;
    float brightness = dot(f_color.rgb, vec3(0.299, 0.587, 0.114));
    vec3 grayscale = vec3(brightness);
    float red_preservation = smoothstep(0.2, 0.6, f_color.r - (f_color.g + f_color.b) * 0.8);
    float dynamic_saturation = saturation + red_preservation * 0.65;
    f_color.rgb = mix(grayscale, f_color.rgb, dynamic_saturation);
    float glitch_line = step(1.5, random(vec2(0.0, floor(cropped_uv.y * 50.0) + time * 2.0)));
    if (glitch_line > 0.0) {
        f_color.r *= 1.2;
        f_color.g *= 0.8;
    }
    float flicker = 1.0 - step(0.997, random(vec2(time * 0.1, 0.0))) * 0.08;
    f_color.rgb *= flicker;
    float vign = vignette(cropped_uv);
    f_color.rgb *= vign * 1.2;
    vec2 corner_dist = abs(cropped_uv - 0.5) * 0.5;
    float corner_dark = 1.0 - smoothstep(0.5, 1.1, max(corner_dist.x, corner_dist.y));
    f_color.rgb *= mix(0.25, 1.0, corner_dark);
    f_color.rgb *= 0.8;
    f_color.rgb = floor(f_color.rgb * 48.0) / 48.0;
    vec4 ui_layer = texture(ui_surf, uv);
    if (ui_layer.a > 0.0) {
        f_color = mix(f_color, ui_layer, ui_layer.a);
    }
    if ((cropped_uv.x < 0.0) || (cropped_uv.x > 1.0) || (cropped_uv.y < 0.0) || (cropped_uv.y > 1.0)) {
        f_color = vec4(0.0, 0.0, 0.0, 1.0);
    }
    f_color.a = 1.0;
}
