Tools for Quality Checking your data!

Edit the images.json file to match your data. In the current images.json example, we load subject's T2w images as an overlay on top of their T1w images (data from the CMI HBN dataset) in order to check the co-registration and quality of the data. You could also use this script to load a native or template structural image with a mean functional image as an overlay.
Launch the index.html file in a web browser (We have tested on Firefox & Chrome) to bring up the image viewer. Press 's' key to start rating images. Foward arrow means the image is good, back arrow = bad image. To go back one image, use the space bar. Click "Save CSV" in the top left corner to save the QC rating session in a csv file.

CMI_T2_T1_checkalignment.ipynb is a Jupyter notebook to load images, overlay them and save as a .jpg image then concatenate all .jpg images into a single PDF (fastest rating method, but must manually keep track of bad images) 
