#version 330

uniform sampler2D surface;

out vec4 f_color;
in vec2 uv;

const ivec2 dimensions = ivec2(140, 100);

vec4 lookup_texel(sampler2D tex, ivec2 uv_px) {
    ivec2 tex_size = dimensions;

    // force black for out-of-bounds pixels
    if ((uv_px.x < 0) || (uv_px.y < 0) || (uv_px.x >= tex_size.x) || (uv_px.y >= tex_size.y)) {
        return vec4(0.0, 0.0, 0.0, 0.0);   
    }

    return texture(tex, (uv_px * 1.0 + vec2(0.5, 0.5)) / tex_size);
}

void main() {
    /*ivec2 uv_px = ivec2(uv.x * dimensions.x, uv.y * dimensions.y);
    vec4 color = lookup_texel(surface, uv_px);
    if (color.r > 0.5) {
        f_color = vec4(1.0, 0.0, 0.0, 1.0);
    } else {
        f_color = vec4(0.0, 0.0, 0.0, 1.0);
    }*/
    vec4 color = texture(surface, uv);
    f_color = vec4(38.0 / 255.0, 27.0 / 255.0, 46.0 / 255.0, 1.0);
    if (color.r > 0.5) {
        f_color = vec4(48.0 / 255.0, 49.0 / 255.0, 84.0 / 255.0, 1.0);
    }
    if (color.g > 0.5) {
        f_color = vec4(37.0 / 255.0, 91.0 / 255.0, 107.0 / 255.0, 1.0);
    }
}