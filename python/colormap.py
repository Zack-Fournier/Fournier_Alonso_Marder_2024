import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


def customcmap():

    # choose colormap
    tab10 = 'tab10'

    # colormap object
    tab10cmap = plt.get_cmap(tab10)

    # last rgb triplet
    last_color_rgb_triplet = tab10cmap(10)[:3]

    # choose Set1 colormap
    colormap_name = 'Set1'

    # create a colormap object
    cmap = plt.get_cmap(colormap_name)

    # Get the RGB triplets for all colors in the colormap
    rgb_triplets = [cmap(i)[:3] for i in range(cmap.N)]

    # new color
    new_color = last_color_rgb_triplet

    # Add the new color as the 9th color
    modified_rgb_triplets = rgb_triplets[:8] + [new_color] + rgb_triplets[8:]

    # Create a custom colormap with the modified RGB triplets
    custom_cmap = ListedColormap(modified_rgb_triplets, name=colormap_name)

    print(modified_rgb_triplets)

    print(last_color_rgb_triplet)

    return custom_cmap
