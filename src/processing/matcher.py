# matcher.py

def match_colors(reference_colors, target_color, threshold=5):
    matches = []
    for ref_color in reference_colors:
        distance = calculate_color_distance(ref_color['rgb'], target_color)
        if distance <= threshold:
            matches.append({
                'name': ref_color['name'],
                'rgb': ref_color['rgb'],
                'distance': distance
            })
    matches.sort(key=lambda x: x['distance'])
    return matches

def calculate_color_distance(color1, color2):
    return ((color1[0] - color2[0]) ** 2 + 
            (color1[1] - color2[1]) ** 2 + 
            (color1[2] - color2[2]) ** 2) ** 0.5

def get_top_n_matches(reference_colors, target_color, n=5):
    matches = match_colors(reference_colors, target_color)
    return matches[:n]