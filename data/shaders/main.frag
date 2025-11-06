#version 430

uniform sampler2D surface;
uniform sampler2D hud_surf;
uniform sampler2D noise_tex;
uniform sampler2D static_noise_tex;
uniform sampler2D crt_filter_tex;
uniform sampler2D crack_tex;
uniform float time;
uniform vec2 scroll;
uniform ivec2 dimensions;
uniform vec2 border_discard;
uniform float saturation = 1.0;
uniform bool in_void;
uniform float crt_effect = 1.0;
uniform float power_off = 0.0;

out vec4 f_color;
in vec2 uv;

vec4 lookup_texel(sampler2D tex, ivec2 uv_px) {
    ivec2 tex_size = textureSize(tex, 0);
    return texture(tex, (uv_px * 1.0 + vec2(0.5, 0.5)) / tex_size);
}

float random(ivec2 seed) {
  return pow(time, 2.3) * (seed.x + 3) + pow(time, 3.7) * (seed.y + 3);
}

vec2 uv_grow(vec2 uv_in, float factor) {
  vec2 offset = uv_in - vec2(0.5, 0.5);
  return offset * factor + vec2(0.5, 0.5);
}

void main() {
  vec2 uv_range = vec2(1.0 / (1.0 - border_discard.x), 1.0 / (1.0 - border_discard.y));
  vec2 cropped_uv = vec2(uv.x * uv_range.x - (uv_range.x - 1.0) * 0.5, uv.y * uv_range.y - (uv_range.y - 1.0) * 0.5);
  ivec2 tex_size = textureSize(surface, 0).xy;
  ivec2 center_px = tex_size / 2;

  vec2 center_offset = vec2(uv - vec2(0.5, 0.5));
  if (in_void) {
    float dis = distance(vec2(0.5, 0.5), uv);
    cropped_uv = uv_grow(vec2(cropped_uv.x + center_offset.x * dis * 0.2 * crt_effect, cropped_uv.y + center_offset.y * dis * 0.2 * crt_effect), 1.0 - 0.1 * crt_effect);
  }

  ivec2 uv_px_i = ivec2(vec2(tex_size) * cropped_uv);
  vec2 uv_px = vec2(uv_px_i);

  vec4 base_color = texture(surface, cropped_uv);
  vec4 ui_color = texture(hud_surf, cropped_uv);

  if (base_color.a < 1.0) {
    float noise_v1 = texture(noise_tex, (uv_px + scroll) * 0.01 + vec2(time * 0.062, time * 0.047)).r;
    float noise_v2 = texture(noise_tex, (uv_px + scroll) * 0.02 + vec2(time * -0.013, time * -0.0485)).r;
    float noise_v = noise_v1 * 0.5 + noise_v2 * 0.5;
    if (in_void) {
      f_color = vec4(0.094, 0.067, 0.118, 1.0);
      if (noise_v > 0.61) {
        f_color = vec4(0.149, 0.106, 0.18, 1.0);
      }

      vec4 ref_color = texture(surface, cropped_uv * 0.92 + 0.04);
      f_color += vec4(ref_color.rgb * 0.1, 1.0);
    } else {
      float land_strength = 0.0;
      for (int i = 0; i < 6; i++) {
        if (lookup_texel(surface, uv_px_i + ivec2(0, -i)).a > 0.9) {    
          land_strength += 0.3;
        }
      }
      for (int i = -1; i <= 1; i++) {
        if ((lookup_texel(surface, uv_px_i + ivec2(i, -7)).a > 0.9) && (lookup_texel(surface, uv_px_i + ivec2(i, 0)).a > 0.9)) {
          land_strength += 10;
        }
      }
      noise_v += land_strength * 0.16;
      f_color = vec4(0.447, 0.851, 0.937, 1.0);
      if (noise_v > 0.61) {
        f_color = vec4(0.996, 0.988, 0.827, 1.0);
      } else if (noise_v1 * 0.7 + noise_v2 * 0.3 < 0.45) {
        f_color = vec4(0.29, 0.612, 0.875, 1.0);
      }
    }
  } else if ((in_void) && (length(base_color.rgb - vec3(0.11765, 0.11765, 0.19608)) < 0.01)) {
    float static_noise = mod(random(uv_px_i), 0.1) * 10;
    if (static_noise < 0.33) {
      f_color = vec4(0.475, 0.518, 0.616, 1.0);
    } else if (static_noise < 0.67) {
      f_color = vec4(0.392, 0.38, 0.545, 1.0);
    } else {
      f_color = vec4(0.804, 0.82, 0.788, 1.0);
    }
    f_color = vec4(f_color.r * 0.33, f_color.g * 0.27, f_color.b * 0.33, 1.0);
  } else {
    f_color = vec4(base_color.rgb, 1.0);
  }

  f_color = f_color * (1.0 - ui_color.a) + vec4(ui_color.rgb * ui_color.a, 1.0);

  if (in_void) {
    ivec2 filter_uv = ivec2(cropped_uv * dimensions);
    float r = mod(random(ivec2(mod(time, 10) * -1000, mod(time, 10) * 3190)), 47.1);
    float noise_filter = lookup_texel(static_noise_tex, (filter_uv + ivec2(-r * 5000, r * 3000)) / 6).r * 0.2 * crt_effect + (1.0 - 0.5 * crt_effect);
    f_color = vec4(f_color.rgb * lookup_texel(crt_filter_tex, filter_uv).rgb, 1.0) * 0.65 * crt_effect + f_color * noise_filter;
  }

  if ((cropped_uv.x < 0.0) ||(cropped_uv.x > 1.0) || (cropped_uv.y < 0.0) ||(cropped_uv.y > 1.0)) {
    f_color = vec4(0.0, 0.0, 0.0, 1.0);
  }

  float brightness = (f_color.r + f_color.g + f_color.b) / 3;
  vec3 grayscale_color = vec3(brightness);
  if (f_color.rgb != vec3(1.0, 0.0, 1.0)) {
    f_color = vec4(f_color.rgb * saturation + grayscale_color * (1.0 - saturation), f_color.a);
  }

  vec4 cracked_color = texture(crack_tex, cropped_uv);
  float texel_height = 1.0 / tex_size.y;
  float crack_shift = 0.0;
  while (cracked_color.g > 0) {
    crack_shift += texel_height;
    cracked_color = texture(crack_tex, vec2(cropped_uv.x, cropped_uv.y + crack_shift));
  }
  while (cracked_color.b > 0) {
    crack_shift -= texel_height;
    cracked_color = texture(crack_tex, vec2(cropped_uv.x, cropped_uv.y + crack_shift));
  }
  if (crack_shift != 0.0) {
    f_color = vec4(texture(surface, vec2(cropped_uv.x, cropped_uv.y + crack_shift)).rgb * 0.8 + f_color.rgb * 0.2, 1.0);
  }

  cracked_color.r *= 0.5;

  f_color = vec4((f_color.rgb * (1.0 - cracked_color.r)) + (vec3(1.0) * cracked_color.r), 1.0);

  if (((abs(center_offset.x) * 0.05 + abs(center_offset.y) * 0.5) > pow(1.0 - power_off, 5)) && (length(center_offset) > (1.0 - power_off) * 0.15)) {
    f_color = vec4(0.0, 0.0, 0.0, 1.0);
  }
}