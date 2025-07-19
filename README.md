Image Color Sorter

This script sorts images in a folder by their dominant colors. It groups images into categories like earthy, warm, bright, cool, and muted, then renames them in order based on these colors.

Features:

Extracts main colors from each image using clustering.

Uses color theory (hue, saturation, brightness) for better sorting.

Works on common image types like JPG, PNG, GIF, BMP.

Renames images as 1.jpg, 2.png, and so on.

Requirements:

Python 3 installed

Packages: pillow, numpy, scikit-learn (install with pip)

How to use:

Set your image folder path in the script (replace the folder_path variable).

Install required packages by running:
pip install pillow numpy scikit-learn

Run the script with Python.

Your images will be sorted and renamed in the folder.

Important:

Make a backup of your images before running because files get renamed.

Works best with images that have clear color themes.

You can change the color categories or number of dominant colors by editing the script.

Created by Atharva Gupta. 
