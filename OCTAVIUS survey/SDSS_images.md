## SDSS Image Downloading

To create a survey in OCTAVIUS, you will need not only a CSV file with the objects' data but also images of them. 
There are multiple ways to approach it, but the best is starting with downloading pictures from the SDSS catalogue. 

### SDSS Image List tool

If the number of objects is small, you can generate image cutouts of SDSS images based on a defined list of object positions, namely the RA and DEC. 
You need to go to https://skyserver.sdss.org/dr16/en/tools/chart/listinfo.aspx, write the RA and DEC in the table and the site will generate the images for you. 
You can decide on the scale of the pictures, but usually between 0.5 and 1 ''/pix is the best.

### SDSS SQL in Python

If you have a CSV file with multiple entries, a Python code can do it for you. It automatically generates pictures and stores them in a folder. They can then be edited and shown on an OCTAVIUS survey. An example of the code is here: 
```
import pandas as pd
import requests
import os

csv_file= 'GW_vett_practice.csv'  
data = pd.read_csv(csv_file)
output_dir = "GW_practice"
os.makedirs(output_dir, exist_ok=True)

def sdss_image(ra, dec, scale=3, width=512, height=512):
    image_url = (f"https://skyserver.sdss.org/dr12/SkyserverWS/ImgCutout/getjpeg?ra={ra}&dec={dec}&scale={scale}&width={width}&height={height}")
    return image_url

counter=1
for index, row in data.iterrows():     #iteration over the CSV rows
    name= row['NAME']
    ra= row['RA'] 
    dec= row['DEC']
    image_url= sdss_image(ra, dec)
    response= requests.get(image_url)
    
    if response.status_code == 200:
        image_path = os.path.join(output_dir, f"GWpract_{counter}.jpg")
        counter +=1
        with open(image_path, "wb") as f:
            f.write(response.content)
        print(f"Saved image for {name} at {image_path}")
    else:
        print(f"Failed to retrieve image for {name} (RA: {ra}, DEC: {dec})")
            
print("Image retrieval complete!")
```


## SDSS Image Edit

After generating the images, they can be edited by identifying the object of interest and any possible light sources, such as stars or galaxies, for whose minimum brightness can be modified in the this file: 
