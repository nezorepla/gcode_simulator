import re
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

def process_gcode(gcode_lines):
    # G-code'u işleyerek bir Matplotlib yolu oluştur
    path_data = []
    current_position = None

    for line in gcode_lines:
        match = re.match(r'G[01]\s*X(-?\d+(\.\d+)?)\s*Y(-?\d+(\.\d+)?)', line)
        if match:
            x = float(match.group(1))
            y = float(match.group(3))
            if current_position is None:
                current_position = (x, y)
                path_data.append((Path.MOVETO, current_position))
            else:
                current_position = (x, y)
                path_data.append((Path.LINETO, current_position))

    if path_data:
        codes, verts = zip(*path_data)
        path = Path(verts, codes)
        return path
    else:
        return None

def simulate_gcode(gcode_path, width, height, output_path):
    with open(gcode_path, 'r') as file:
        gcode_lines = file.readlines()

    path = process_gcode(gcode_lines)

    if path:
        fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
        patch = PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)

        plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
        plt.show()
    else:
        print("G-code'da işlenecek komut bulunamadı.")

# Örnek kullanım
gcode_path = "C:\\Users\\alper\\Documents\\G-CODE\\input.gcode"
output_path = "C:\\Users\\alper\\Documents\\G-CODE\\output_image.png"
simulate_gcode(gcode_path, 3000, 1800, output_path)
