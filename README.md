# shp2postgis

This library serves to import a geo-referenced vector file (ESRI Shapefile), or part of it, into a spatial database (PostGIS).

In case of vector files, vectorizer module enables the conversion of a raster file into a vector shapefile, when the first consists of one band. For multiband images, each band must be selected separately. Output shapefile is saved in corresponding folder with all its accompanying files, in the same folder with the original image. Name of the new folder can be given by the user, and is the same name that the generated shapefile will receive.

Module clipImageByCoordinates creates an object, which consists only of the full-path in which one or more raster files are located. Allows the user to clip area of ​​interest from a selected raster image, by entering the corresponding geographical coordinates. The coordinates could be user-selected and represent any area of ​​the image, or they can be derived from the function quadrants_coords(), which returns the geographical coordinates of an image's quadrants. Clipped images are not saved by default, however, clipped image can be saved (optionally). Output image is saved with .tif format, in the same folder with the original image, preserving the original filename, with the suffix 'clipped'. Also, retains metadata and has suitable geo-reference.

The functions pred2db allow you to create a new database, or connect to an existing database in order to create a new table and import data, or import data into an existing table.


## Usage
### clipImageByCoordinates
```
minx, maxx, miny, maxy = quadrants_coords(raster_file, quadrant)
```

Clip selected quadrant of raster file. \
Args: \
raster_file (string): Raster image file fullpath. \
quadrant: One of the four pieces. Start counting from upper left corner, clockwise. Integer in range [1,4]. \
Returns: \
Bounding box coordinates of selected quadrant.


```
wholeImageObject = GeoImClip(searchPath)
```

Returns class object.

```
geometry = wholeImageObject.boundingBox(minx, maxx, miny, maxy, srid)
```

Generates polygon geometry, from given coordinates. \
Args: \
minx, maxx, miny, maxy : float number. \
srid (integer): coordinates reference system id. \
Returns: \
geometry: polygon geometry dataframe.

```
out_img, out_meta = wholeImageObject.clip(im, geometry, write=False)
```

Clip image & update metadata of output image. Option to write output image to disk. \
Args: \
im (string): Path to image. \
geometry: Geometry dataframe used as bounding box to clip image. \
write (bool (opt)): Whether to save output raster to disk. Defaults to False. \
Returns: \
out_img: clipped array. \
out_meta: updated metadata for clipped raster.

### vectorizer
```
vectorize(raster_file=out_img, metadata=out_meta, vector_file, driver, mask_value)
```

Extract vector from raster. Vector propably will include polygons with holes. \
Args: \
raster_file (ndarray): raster image. \
src (DatasetReader type): Keeps path to filesystem. \
vector_file (string): Pathname of output vector file. \
driver (string): Kind of vector file format. \
mask_value (float or integer): No data value. \
Returns: \
Returns 0 & saves folder containing vector shapefile to cwd or to given path.

### pred2db
```
createsdb(host, dbname, user, password)
```

Create new postgres database. \
Args: \
host: IP or Localhost, as string. \
dbname: New database name, as string. \
user: Name of existin user, as string. \
password: User password, as string. \
Returns: \
Returns 0.

```
creategeotable(cursor, tablename)
```

Create new table & postgis extension. \
Args: \
cursor: existing psycopg2 cursor. \
tablename: Name of the new table, as string. \
Returns: \
Returns 0.

```
shp2table(cursor, shpname, tablename)
```

Shapefile to database table. \
Args: \
cursor: existing psycopg2 cursor. \
shpname: Path to input shapefile's folder, as string. \
tablename: Name of target table, as string. \
Returns: \
Returns 0.


## Workflow
Required libraries:
```
import os
import rasterio
from osgeo import ogr
import time
from joblib import Parallel, delayed

import sys
sys.path.insert(1, '/fullpath_to_repo_dir/shp2postgis')
from clipImageByCoordinates import GeoImClip
from clipImageByCoordinates import quadrants_coords
sys.path.insert(1, '/fullpath_to_repo_dir/SearchFileSystem')
from vectorizer import vectorize
from searchInFilesystem import treeSearch
from pred2db import *
```
### Case 1:  Clip raster file by user-defined coordinates, vectorize and create new Postgis database to save final shapefile.
![creta_fin](https://user-images.githubusercontent.com/37594015/68877689-21ba9000-070f-11ea-9b46-ba19cc5b0d35.jpg)
```
searchPath = '/fullpath_to_image_directory'
raster_file = 'image_filename.tif'

# Create object for the whole image & set image_path as cwd.
wholeImageObject = GeoImClip(searchPath)

# User defined coordinates of upper left & lower right corner.
minx = 25.66
maxx = 25.80
miny = 35.12
maxy = 35.32

# Create bounding box from given coordinates. Image's srid is required as input parameter.
bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 4326)

# Clip raster, with georeference.
image, metadata = wholeImageObject.clip(raster_file, bbox)

# Vectorize clipped rasterand save shp to disk.
vectorize(image, metadata, 'shp_name', driver='ESRI Shapefile', mask_value=None)


# Database credentials.
host = 'host'
dbname = 'new_database_name'
user = 'username'
password = 'password'

# Create new database.
createsdb(host, dbname, user, password)

# Connect to new database.
con = ps.connect(host=host, dbname=dbname, user=user, password=password)
con.autocommit = True
# Open a cursor to perform new-database operations.
cur = con.cursor()

# Create new table, with geometry column.
creategeotable(cur, 'new_table_name')

# Insert data from shp to database.
shp2table(cur, 'shp_name', 'new_table_name')

# Close connection with database.
cur.close()
con.close()
```

### Case 2: Clip raster file in quadrants, parallelize vectorization and save final shapefiles to existing Postgis database.
```

# Quadrant_1
# Create object for the whole image & set image_path as cwd.
wholeImageObject = GeoImClip(searchPath)

# Aquire bounding box coordinates for selected quadrant.
minx, maxx, miny, maxy = quadrants_coords(os.path.join(searchPath, raster_file), 1)

# Create bounding box from given coordinates. Image's srid is required as input parameter.
bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 32634)

# Clip raster, with georeference.
image1, metadata1 = wholeImageObject.clip(raster_file, bbox)


# Quadrant_2
wholeImageObject = GeoImClip(searchPath)
minx, maxx, miny, maxy = quadrants_coords(os.path.join(searchPath, raster_file), 2)
bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 32634)
image2, metadata2 = wholeImageObject.clip(raster_file, bbox)

# Quadrant_3
wholeImageObject = GeoImClip(searchPath)
minx, maxx, miny, maxy = quadrants_coords(os.path.join(searchPath, raster_file), 3)
bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 32634)
image3, metadata3 = wholeImageObject.clip(raster_file, bbox)

# Quadrant_4
wholeImageObject = GeoImClip(searchPath)
minx, maxx, miny, maxy = quadrants_coords(os.path.join(searchPath, raster_file), 4)
bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 32634)
image4, metadata4 = wholeImageObject.clip(raster_file, bbox)

# Parallelize vectorization of quadrants.
# List of arrays to vectorize.
arrays = [image1, image2, image3, image4]
# List of individual metadata for each raster array.
metadata = [metadata1, metadata2, metadata3, metadata4]
# List of strings filenames to save created shapefiles.
shpfilenames = ['quad_some_location_1', 'quad_some_location_2',
                'quad_some_location_3', 'quad_some_location_4']

# Convert selected quadrant to shapefile, and save to disk.
start = time.time()
Parallel(n_jobs=2, verbose=51)(delayed(vectorize)(
        raster_file = arrays[i],
        metadata = metadata[i],
        vector_file = shpfilenames[i],
        driver = 'ESRI Shapefile',
        mask_value = None
        ) for i in range(0, len(arrays)))

end = time.time()
print("TOTAL elapsed time:. . . {} mins".format((end-start)//60))
```
![sterea_fin](https://user-images.githubusercontent.com/37594015/68877619-08194880-070f-11ea-8476-a4aab3075c3b.jpg)

```
# Database credentials.
host = 'host'
dbname = 'new_database_name'
user = 'username'
password = 'password'

# Connect to existing database.
con = ps.connect(host=host, dbname=dbname, user=user, password=password)
con.autocommit = True
# Open a cursor to perform new-database operations.
cur = con.cursor()

# Create our table (in existing database), with geometry.
creategeotable(cur, 'location')

# Gather shapefiles for a certain table.
shps2db = [treeSearch(searchPath, 'quad', 'some_location', i) for i in ['1.shp', '2.shp', '3.shp', '4.shp']]

# Insert data from shp to database.
for file in shps2db:
    shp2table(cur, file[0], 'location')

# Close connection with database.
cur.close()
con.close()
```
