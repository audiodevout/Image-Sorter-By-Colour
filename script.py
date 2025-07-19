"""
Image Sorting by Complex Color Analysis (Earthy, Bright, Warm, Cool, Muted)

This script processes all images in a specified folder and sorts them by 
analyzed dominant color characteristics rather than simple average RGB.

Features:
- Extracts dominant color palette from each image using KMeans clustering.
- Converts RGB colors to HSV color space for better perceptual color handling.
- Categorizes images into five color mood categories: earthy, warm, bright, cool, muted.
- Sorts images first by category order, then by hue within categories.
- Renames images sequentially (1.ext, 2.ext, etc.) in the sorted order.

Usage:
- Set the 'folder_path' variable to the folder containing your images.
- Install dependencies with:
    pip install pillow numpy scikit-learn
- Run the script with Python 3.

WARNING:
- The script renames your original image files. Backup your folder before running.
"""

import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# === Configuration ===

# Replace this with your actual folder path.
# Use raw string (r'...') for Windows paths to avoid escape issues.
folder_path = 'path'

# Define the order in which color categories should be sorted
categories_order = ['earthy', 'warm', 'bright', 'cool', 'muted']

# === Functions ===

def extract_palette(image_path, n_colors=5):
    """
    Extract dominant color palette from an image using KMeans clustering.

    Args:
        image_path (str): Path to the image file.
        n_colors (int): Number of dominant colors to extract.

    Returns:
        palette (ndarray): Array of RGB dominant colors.
        weights (ndarray): Relative weights of each color in the palette.
    """
    img = Image.open(image_path).convert('RGB')
    img = img.resize((100, 100))  # Resize for performance
    data = np.array(img).reshape(-1, 3)  # Flatten pixels to list of RGB

    kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(data)
    palette = kmeans.cluster_centers_
    counts = np.bincount(kmeans.labels_)
    weights = counts / counts.sum()

    return palette, weights

def rgb_to_hsv(rgb):
    """
    Convert RGB color (0-255) to HSV (Hue in degrees, Saturation and Value 0-1).

    Args:
        rgb (array-like): RGB color triplet.

    Returns:
        tuple: (hue, saturation, value)
    """
    rgb = np.array(rgb) / 255.0
    r, g, b = rgb
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    # Hue calculation
    if diff == 0:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360

    # Saturation calculation
    s = 0 if mx == 0 else diff / mx

    # Value calculation
    v = mx

    return h, s, v

def analyze_colors(palette, weights):
    """
    Compute weighted average hue, saturation, and value from a palette.

    Args:
        palette (ndarray): RGB colors.
        weights (ndarray): Weights for each color.

    Returns:
        tuple: (average_hue, average_saturation, average_value)
    """
    hues = []
    sats = []
    vals = []

    for color, w in zip(palette, weights):
        h, s, v = rgb_to_hsv(color)
        hues.append(h * w)
        sats.append(s * w)
        vals.append(v * w)

    avg_hue = sum(hues)
    avg_sat = sum(sats)
    avg_val = sum(vals)

    return avg_hue, avg_sat, avg_val

def categorize_color(hue, sat, val):
    """
    Categorize color based on HSV values.

    Categories:
        - Earthy: Warm hues, low saturation, medium brightness.
        - Bright: High saturation and brightness.
        - Muted: Low saturation and low brightness.
        - Warm: Warm hues generally.
        - Cool: Everything else.

    Args:
        hue (float): Hue in degrees (0-360).
        sat (float): Saturation (0-1).
        val (float): Value/Brightness (0-1).

    Returns:
        str: category name.
    """
    # Warm hues: red to yellow range and magenta to red wraparound
    warm = (hue <= 60) or (hue >= 300)

    if warm and sat < 0.5 and 0.3 < val < 0.7:
        return 'earthy'
    elif sat > 0.6 and val > 0.7:
        return 'bright'
    elif sat < 0.3 and val < 0.5:
        return 'muted'
    elif warm:
        return 'warm'
    else:
        return 'cool'

# === Main Script ===

def main():
    supported_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]

    image_categorized = []

    for img_file in images:
        path = os.path.join(folder_path, img_file)
        palette, weights = extract_palette(path)
        avg_hue, avg_sat, avg_val = analyze_colors(palette, weights)
        category = categorize_color(avg_hue, avg_sat, avg_val)
        image_categorized.append((img_file, category, avg_hue, avg_sat, avg_val))
        print(f"{img_file}: category={category}, hue={avg_hue:.1f}, sat={avg_sat:.2f}, val={avg_val:.2f}")

    # Sort images by category (as per categories_order) then by hue within category
    image_categorized.sort(key=lambda x: (categories_order.index(x[1]), x[2]))

    # Rename images sequentially in sorted order
    for i, (filename, category, h, s, v) in enumerate(image_categorized, start=1):
        ext = os.path.splitext(filename)[1]
        new_name = f"{i}{ext}"
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
        print(f"Renamed {filename} -> {new_name}")

if __name__ == "__main__":
    main()
