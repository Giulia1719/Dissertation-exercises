## SDSS Image Downloading

To create a survey in OCTAVIUS, you will need not only a CSV file with the objects' data but also images of them. 
There are multiple ways to approach it, but the best is starting with downloading pictures from the SDSS catalogue. 

### SDSS Image List tool

If the number of objects is small, you can generate image cutouts of SDSS images based on a defined list of object positions, namely the RA and DEC. 

You need to go to https://skyserver.sdss.org/dr16/en/tools/chart/listinfo.aspx, write the RA and DEC in the table and the site will generate the images for you. 
You can decide on the scale of the pictures, but usually between 0.5 and 1 ''/pix is the best.

### SDSS SQL in Python

If you have a CSV file with multiple entries, a Python code can do it for you. It automatically generates pictures and stores them in a folder. They can then be edited and shown on an OCTAVIUS survey. The Python code is here: 
