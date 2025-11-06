#version 430
uniform sampler2D surface;
uniform sampler2D hud_surf;
uniform sampler2D crt_filter_tex;
uniform float time;
uniform vec2 scroll;
uniform ivec2 dimensions;
uniform vec2 border_discard;
uniform float saturation = 1.0;
uniform float crt_effect = 1.0;
uniform float power_off = 0.0;
out vec4 f_color;
in vec2 uv;

vec4 lookup_texel(sampler2D tex, ivec2 uv_px) {
    ivec2 tex_size = textureSize(tex, 0);
    return texture(tex, (uv_px * 1.0 + vec2(0.5, 0.5)) / tex_size);
}

vec2 uv_grow(vec2 uv_in, float factor) {
    vec2 offset = uv_in - vec2(0.5, 0.5);
    return offset * factor + vec2(0.5, 0.5);
}

void main() {
    vec2 uv_range = vec2(1.0 / (1.0 - border_discard.x), 1.0 / (1.0 - border_discard.y));
    vec2 cropped_uv = vec2(uv.x * uv_range.x - (uv_range.x - 1.0) * 0.5, uv.y * uv_range.y - (uv_range.y - 1.0) * 0.5);
    ivec2 tex_size = textureSize(surface, 0).xy;
    vec2 center_offset = vec2(uv - vec2(0.5, 0.5));

    vec4 base_color = texture(surface, cropped_uv);
    vec4 ui_color = texture(hud_surf, cropped_uv);

    f_color = vec4(base_color.rgb, 1.0);

    f_color = f_color * (1.0 - ui_color.a) + vec4(ui_color.rgb * ui_color.a, 1.0);

    ivec2 filter_uv = ivec2(cropped_uv * dimensions);
    f_color = vec4(f_color.rgb * lookup_texel(crt_filter_tex, filter_uv).rgb, 1.0) * 0.65 * crt_effect + f_color * (1.0 - 0.5 * crt_effect);

    if ((cropped_uv.x < 0.0) || (cropped_uv.x > 1.0) || (cropped_uv.y < 0.0) || (cropped_uv.y > 1.0)) {
        f_color = vec4(0.0, 0.0, 0.0, 1.0);
    }

    float brightness = (f_color.r + f_color.g + f_color.b) / 3.0;
    vec3 grayscale_color = vec3(brightness);
    if (f_color.rgb != vec3(1.0, 0.0, 1.0)) {
        f_color = vec4(f_color.rgb * saturation + grayscale_color * (1.0 - saturation), f_color.a);
    }

    if (((abs(center_offset.x) * 0.05 + abs(center_offset.y) * 0.5) > pow(1.0 - power_off, 5)) && 
        (length(center_offset) > (1.0 - power_off) * 0.15)) {
        f_color = vec4(0.0, 0.0, 0.0, 1.0);
    }
}