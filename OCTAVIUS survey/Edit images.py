#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from matplotlib import use
use("Agg")
import matplotlib.pyplot as plt
from io import open as iopen
import matplotlib.image as mpimage
from matplotlib.lines import Line2D
from PIL import Image
import ast
import time
from astropy.io import fits
from astropy import coordinates,wcs,log
from astropy.nddata import Cutout2D
import astropy
from astropy.table import Table
import sys
import numpy as np
import astropy.units as u
import gc
import traceback
import tqdm
import queue
from astropy.nddata.utils import NoOverlapError
from astropy.io import fits
import urllib
import pyvips
from io import BytesIO
import pickle
import pandas as pd
from astropy.coordinates import SkyCoord
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import json
import matplotlib.patches as mppatches
from scipy.ndimage import label


# In[7]:


data = pd.read_csv("GW_vett_practice.csv")

class ImagePlotCenters:
    @staticmethod
    def parse(target, image_number):
        """Takes image metadata and marks the center and circles bright objects on the preloaded image."""
        # Extract necessary data
        RA = target["RA"]
        DEC = target["DEC"]
        NAME = target["NAME"]  # Get the name from the CSV file
        SIZE = 3  # Fixed size in arcseconds
        
        # Generate the image filename based on a counter (image_number)
        image_name = f"GWpract_{image_number}.jpg"  # Start with the .jpg file for input
        
        out_dir = "GW_practice/"
        in_file_path = os.path.join(out_dir, image_name)  # Use .jpg directly for input
        out_file_path = os.path.join(out_dir, f"GWpract_{image_number}.png")  # Output saved as .png
        
        # Check if the input image exists
        if not os.path.exists(in_file_path):
            raise FileNotFoundError(f"Input image file not found: {in_file_path}")

        # Create Matplotlib figure and display the image
        fig = plt.figure()
        ax = plt.Axes(fig, [0, 0, 1, 1])
        fig.add_axes(ax)
        img = mpimage.imread(in_file_path)
        ax.imshow(img, aspect='equal')
        ax.set_axis_off()

        # Calculate center pixel coordinates and scaling
        xmax, ymax = img.shape[:2]
        xcent, ycent = xmax / 2, ymax / 2
        scale = SIZE / xmax / 60
        marker_size = 10
        error_size = 15 / 3600 / scale

        # Plot the central marker
        p = mppatches.Circle(
            (round(xcent, 0), round(ycent, 0)),
            radius=error_size,
            linestyle=":",
            ec="green",
            linewidth=2,
            fc='none'
        )
        ax.add_patch(p)

        # Add a scale bar
        fontprops = fm.FontProperties(size=18)
        scalebar = AnchoredSizeBar(
            ax.transData,
            151 / 2, "30''", 'lower left',
            pad=0.1,
            color='white',
            frameon=False,
            size_vertical=1,
            fontproperties=fontprops
        )
        ax.add_artist(scalebar)

        # Add the target name (from the CSV) as an annotation at the top of the image
        ax.text(xcent, 15, NAME, ha="center", va="center", size=20, color="white",
                bbox=dict(boxstyle="square", fc="black", ec=None, alpha=0.5))

        # Detect bright objects in the image and circle them
        ImagePlotCenters.detect_and_circle_bright_objects(img, ax)

        # Save the figure as a temporary file
        temp_file_path = os.path.join(out_dir, f"temp_{image_number}.png")
        plt.savefig(temp_file_path, dpi=167)
        plt.close(fig)

        # Crop and resize the image for output
        image_quality = (800, 800)
        with Image.open(temp_file_path) as temp:
            width, height = temp.size
            if width < height:
                ratio = image_quality[0] / width
                temp = temp.resize((image_quality[0], int(round(height * ratio, 0))))
            else:
                ratio = image_quality[1] / height
                temp = temp.resize((int(round(width * ratio, 0)), image_quality[1]))

            width, height = temp.size
            temp = temp.crop((
                int(round(width / 2 - image_quality[0] / 2, 0)),
                int(round(height / 2 - image_quality[1] / 2, 0)),
                int(round(width / 2 + image_quality[0] / 2, 0)),
                int(round(height / 2 + image_quality[1] / 2, 0))
            ))
            temp.save(out_file_path)  # Save directly as .png, replacing original .jpg

        # Cleanup temporary files
        os.remove(temp_file_path)

        # Remove the original .jpg file to replace it with .png
        os.remove(in_file_path)

    @staticmethod
    def detect_and_circle_bright_objects(img, ax):
        """Detect bright objects in the image and circle them."""
        # Convert the image to grayscale for simplicity
        gray_img = np.mean(img, axis=2)

        # Define a threshold to detect brighter objects
        threshold = np.max(gray_img) * 0.45  
        bright_objects = gray_img > threshold

        # Label connected regions (bright objects)
        labeled, num_objects = label(bright_objects)

        # Loop through each detected object and draw a circle around it
        for i in range(1, num_objects + 1):
            # Get the coordinates of the object's center
            coords = np.column_stack(np.where(labeled == i))
            ymean, xmean = np.mean(coords, axis=0)

            # Draw a circle around the object (tab:blue color, thinner line)
            radius = 10  # Circle radius, can be adjusted if necessary
            circle = mppatches.Circle(
                (xmean, ymean),
                radius=radius,
                edgecolor='tab:blue',  # Using the tab:blue color for circles
                facecolor='none',
                lw=0.5  # Lighter circle with thinner line thickness
            )
            ax.add_patch(circle)

# Process each row and generate the images
for idx, row in data.iterrows():
    # Ensure each object has a unique name from the CSV file
    row['NAME'] = row['NAME']  # Keep the name from the CSV file intact
    ImagePlotCenters.parse(row, image_number=idx + 1)  

print("Image processing complete!")

