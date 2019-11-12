# shp2postgis

This library serves to import a geo-referenced vector file (ESRI Shapefile), or part of it, into a spatial database (PostGIS).

In case of vector files, vectorizer module enables the conversion of a raster file into a vector shapefile, when the first consists of one band. For multiband images, each band must be selected separately. Output shapefile is saved in corresponding folder with all its accompanying files, in the same folder with the original image. Name of the new folder can be given by the user, and is the same name that the generated shapefile will receive.

Module clipImageByCoordinates creates an object, which consists only of the full-path in which one or more raster files are located. Allows the user to clip area of ​​interest from a selected raster image, by entering the corresponding geographical coordinates. The coordinates could be user-selected and represent any area of ​​the image, or they can be derived from the function quadrants_coords(), which returns the geographical coordinates of an image's quadrants. Clipped images are not saved by default, however, clipped image can be saved (optionally). Output image is saved with .tif format, in the same folder with the original image, preserving the original filename, with the suffix 'clipped'. Also, retains metadata and has suitable geo-reference.

The functions pred2db allow you to create a new database, or connect to an existing database in order to create a new table and import data, or import data into an existing table.

## Workflow
### Case 1:  Clip raster file by user-defined coordinates, vectorize and create new Postgis database to save final shapefile.
```
import os
import rasterio
from osgeo import ogr
import time
from joblib import Parallel, delayed

import sys
sys.path.insert(1, '/fullpath_to_repository_directory/shp2postgis')
from clipImageByCoordinates import GeoImClip
from clipImageByCoordinates import quadrants_coords
sys.path.insert(1, '/fullpath_to_repository_directory/SearchFileSystem')
from vectorizer import vectorize
from searchInFilesystem import treeSearch
from pred2db import *


searchPath = '/fullpath_to_image_directory'
raster_file = 'image_filename.tif'

# Create object for the whole image & set image_path as cwd.
wholeImageObject = GeoImClip(searchPath)
```
### Case 2: Clip big raster file in quadrants, parallelize vectorization and save final shapefiles to existing Postgis database.


## Usage
