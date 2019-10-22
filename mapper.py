from gmplot import gmplot
from GPSPhoto import gpsphoto
from resizeimage import resizeimage
from PIL import Image

import os
from os.path import join
import pathlib
from sys import argv
import shutil


# get source directory from command line, or use default
pics_loc = "testpics/"
if len(argv) > 1:
    pics_loc = argv[1]

# the working site will go here
outdir = "site/"

# resource directories within the outdir
thumbdir = "thumbs"
fullpicdir = "bigpics"

if os.path.exists(outdir):
    inp = input("'{}' output directory already exists. Overwrite? (y/n)".format(outdir))
    if inp.lower() != "y": exit()
    shutil.rmtree(outdir)

pathlib.Path(join(outdir, thumbdir)).mkdir(parents=True, exist_ok=True)
pathlib.Path(join(outdir, fullpicdir)).mkdir(parents=True, exist_ok=True)

# where and how big the map starts
centerx = 53.989375
centery = -2.519943
zoomlevel = 6
gmapapikey = ""

gmap = gmplot.GoogleMapPlotter(centerx, centery, zoomlevel,
        apikey=gmapapikey)

def create_thumb(dirpath, imgname):
    """write a thumbnail of the image to the output dir"""
    with open(join(dirpath, imgname), 'r+b') as f:
        with Image.open(f) as image:
            thumb = resizeimage.resize_width(image, 50)
            thumbpath = join(outdir, thumbdir, imgname)
            print("saving thumbnail to", thumbpath)
            thumb.save(thumbpath, image.format)

def create_full(dirpath, imgname):
    """compress the image and write to the output dir"""
    with open(join(dirpath, imgname), 'r+b') as f:
        with Image.open(f) as image:
            fullpicpath = join(outdir, fullpicdir, imgname)
            print("saving full pic to", fullpicpath)
            image.save(fullpicpath, quality=75, optimize=True)

for dirpath, subdirpath, files in os.walk(pics_loc):
    for f in files:
        filepath = join(dirpath, f)
        if not filepath.lower().endswith(".jpg"):
            continue
        try:
            data = gpsphoto.getGPSData(filepath)
            print(f, data['Latitude'], data['Longitude'])

            create_thumb(dirpath, f)
            create_full(dirpath, f)

            # this will display a larger image as popup when the thumbnail is clicked
            onclickjs = 'let e = document.createElement("img"); \n\
                        document.body.appendChild(e); \n\
                        e.setAttribute("active", false) \n\
                        e.setAttribute("class", "big-image"); \n\
                        e.setAttribute("src", "{}");'.format(join(fullpicdir, f))

            gmap.marker(data['Latitude'], 
                    data['Longitude'], 
                    'cornflowerblue',
                    imgpath=join(thumbdir, f),
                    onclick=onclickjs)
        except KeyError:
            print("could not get GPS data for", f)

gmap.add_header('<link rel="stylesheet" href="style.css" />')
gmap.add_header('<script src="script.js"></script>')

gmap.draw(join(outdir, "index.html"))

shutil.copy2("style.css", outdir)
shutil.copy2("script.js", outdir)
