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
import sep


# In[7]:


data = pd.read_csv("name_of_file.csv")

class ImagePlotCenters:
    @staticmethod
    def parse(target, image_number):
        """Takes image metadata and marks the center and circles bright objects on the preloaded image."""
        #Extract necessary data
        RA= target["RA"]
        DEC= target["DEC"]
        NAME= target["NAME"]  #Get the name from the CSV file
        SIZE= 3  #Fixed size in arcseconds
        
        #Generate the image filename based on a counter (image_number)
        image_name = f"nameofimage_{image_number}.jpg"  #Start with the .jpg file for input
        
        out_dir= "name_of_directory/"
        in_file_path= os.path.join(out_dir, image_name)  #Use .jpg directly for input
        out_file_path= os.path.join(out_dir, f"nameofimage_{image_number}.png")  #Output saved as .png
        
        #Check if the input image exists
        if not os.path.exists(in_file_path):
            raise FileNotFoundError(f"Input image file not found: {in_file_path}")

        #Create Matplotlib figure and display the image
        fig= plt.figure()
        ax= plt.Axes(fig, [0, 0, 1, 1])
        fig.add_axes(ax)
        img= mpimage.imread(in_file_path)
        ax.imshow(img, aspect= 'equal')
        ax.set_axis_off()

        # Calculate center pixel coordinates and scaling
        xmax, ymax= img.shape[:2]
        xcent, ycent= xmax/2, ymax/2
        radius_arcsec= 4.5
        radius_pixels= radius_arcsec*xmax/(SIZE*60)

        # Plot the central marker
        p = mppatches.Circle(
            (round(xcent, 0), round(ycent, 0)),
            radius= radius_pixels,
            linestyle= ":",
            ec= "green",
            linewidth= 2,
            fc= 'none'
        )
        ax.add_patch(p)        
        
        # Add a scale bar
        fontprops = fm.FontProperties(size=18)
        scalebar = AnchoredSizeBar(
            ax.transData,
            151 / 2, "10''", 'lower left',
            pad=0.1,
            color='white',
            frameon=False,
            size_vertical=1,
            fontproperties=fontprops
        )
        ax.add_artist(scalebar)

        #Add the target name (from the CSV) as an annotation at the top of the image
        ax.text(xcent, 15, NAME, ha= "center", va= "center", size= 20, color= "white",
                bbox= dict(boxstyle= "square", fc= "black", ec= None, alpha= 0.5))

        #Detect bright objects in the image and circle them
        ImagePlotCenters.detect_and_circle_bright_objects(img, ax)

        #Save the figure as a temporary file
        temp_file_path= os.path.join(out_dir, f"temp_{image_number}.png")
        plt.savefig(temp_file_path, dpi= 167)
        plt.close(fig)

        #Crop and resize the image for output
        image_quality= (800, 800)
        with Image.open(temp_file_path) as temp:
            width, height= temp.size
            if width<height:
                ratio= image_quality[0] / width
                temp= temp.resize((image_quality[0], int(round(height * ratio, 0))))
            else:
                ratio= image_quality[1]/height
                temp= temp.resize((int(round(width*ratio, 0)), image_quality[1]))

            width, height= temp.size
            temp= temp.crop((
                int(round(width/2 - image_quality[0]/2, 0)),
                int(round(height/2 - image_quality[1]/2, 0)),
                int(round(width/2 + image_quality[0]/2, 0)),
                int(round(height/2 + image_quality[1]/2, 0))
            ))
            temp.save(out_file_path)  #Save directly as .png, replacing original .jpg

        #Cleanup temporary files
        os.remove(temp_file_path)

        #Remove the original .jpg file to replace it with .png
        os.remove(in_file_path)

    #Detection of secondary objects in the image
    @staticmethod
    def detect_and_circle_bright_objects(img, ax):
        #Change the image to grayscale to make detection easier
        if img.ndim==3:
            gray_img= img.mean(axis=2)
        else:
            gray_img= img.copy()
        data= gray_img.astype('float32')

        #Background identification and subtraction from objects data using sep
        bkg= sep.Background(data)
        bkg_subtracted= data-bkg.back()
        thresh= 3.0*np.median(bkg.rms())
    
        #Minimum area of detected objects required to avoid false detections
        objects = sep.extract(bkg_subtracted, thresh, minarea=5)
    
        #Filter by flux to keep only relevant objects
        flux_min= 1000 
        filtered_objects= [obj for obj in objects if obj['flux']>flux_min]
        
        #Circle the objects
        for obj in filtered_objects:
            x, y= obj['x'], obj['y']
            radius= obj['a']
            circle= mppatches.Circle(
                (x, y),
                radius= radius,
                edgecolor= 'tab:blue',
                facecolor= 'none',
                lw= 0.5)
            ax.add_patch(circle)

#Process each row and generate the images
for idx, row in data.iterrows():
    #Ensure each object has a unique name from the CSV file
    row['NAME']= row['NAME']  #Keep the name from the CSV file intact
    ImagePlotCenters.parse(row, image_number= idx + 1)  

print("Image processing complete!")

