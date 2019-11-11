"""
TEST FOR

functions:
vectorizer

classes:
clipImageByCoordinates


@author: olyna
"""

import os
import rasterio
from osgeo import ogr
import time

import sys
sys.path.insert(1, '/home/olyna/Documents/SCRIPTS/Python/Github/')
from clipImageByCoordinates import GeoImClip
from clipImageByCoordinates import quadrants_coords
from vectorizer import vectorize
from searchInFilesystem import treeSearch


if __name__ == '__main__':


    # BIG IMAGE TEST
    start = time.time()

    searchPath = '/home/olyna/Documents/msc_thesis/rast2vect/'
    raster_file = 'model_5_image_rf_sfj.tif'

    # Quadrant_3 TEST
    # Aquire bounding box coordinates for selected quadrant.
    minx, maxx, miny, maxy = quadrants_coords(searchPath + raster_file, 3)

    # Create object for the whole image & set image_path as cwd, to save shapefiles.
    wholeImageObject = GeoImClip(searchPath)

    # Create bounding box from given coordinates.
    bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 32634)

    # Clip & save image, with georeference.
    image, metadata = wholeImageObject.clip(raster_file, bbox)


    # with rasterio.open(raster_file) as src:
    #     image = src.read(1)
    #     metadata = src.meta

    # Convert selected quadrant to shapefile, and save to disk.
    vectorize(image, metadata, 'quant_3_sentinel', 'ESRI Shapefile', None)


    end = time.time()
    print(end-start)

#####################################################################################################
    # Credentials
    host = 'localhost'
    dbname = 'predicted'
    user = 'postgres'
    password = '1234'
    
    ############################################## SMALL test #############

    # Create new database
    createsdb('localhost', 'predicted', 'postgres', '1234')

    # Connect to new database
    con = ps.connect(host=host, dbname=dbname, user=user, password=password)
    con.autocommit = True
    # Open a cursor to perform new-database operations
    cur = con.cursor()
    
    # Create our table, with geometry
    creategeotable(cur, 'creta')
    
    # Insert data from shp to database
    shp2table(cur, 'creta_pred', 'creta')
    
    # Close connection with database
    cur.close()
    con.close()
#######################################################################################################
    
"""
    ################################################# THESSALIA  ############
    # Convert raster to vector, and save to disk
    vectorize('model_5_image_rf_sfj.tif', 'thessalia_pred', 'ESRI Shapefile', None)

    # Create our new database
    createsdb('localhost', 'predicted', 'postgres', '1234')
    
    # Create table, with geometry
    creategeotable('thessalia', 'localhost', 'predicted', 'postgres', '1234')

    # Insert data from shp to database
    shp2table(cur, cwd, 'thessalia_pred', 'thessalia')
    
    # Close connection with database
    con.close()
"""



    """
    # SMALL IMAGE TEST
    start = time.time()

    searchPath = '/home/olyna/Documents/msc_thesis/rast2vect/'
    raster_file = '2005_predicted.TIF'


    # Whole Image TEST
    # Set image_path as cwd, to save shapefiles.
    os.chdir(searchPath)

    with rasterio.open(raster_file) as src:
        image = src.read(1)
        metadata = src.meta
    # Convert raster to shapefile and save to disk.
    vectorize(image, metadata, 'whole', 'ESRI Shapefile', None)

    end = time.time()
    print(end-start)
    print(getrusage(RUSAGE_SELF))
    """

    """
    # Quadrant_1 TEST
    # Aquire bounding box coordinates for selected quadrant.
    minx, maxx, miny, maxy = quadrants_coords(searchPath + raster_file, 1)

    # Create object for the whole image & set image_path as cwd, to save shapefiles.
    wholeImageObject = GeoImClip(searchPath)

    # Create bounding box from given coordinates.
    bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 4326)

    # Clip & save image, with georeference.
    image, metadata = wholeImageObject.clip(raster_file, bbox)

    # Convert selected quadrant to shapefile, and save to disk.
    vectorize(image, metadata, 'quadrant_1', 'ESRI Shapefile', None)


    # Quadrant_2 TEST
    # Aquire bounding box coordinates for selected quadrant.
    minx, maxx, miny, maxy = quadrants_coords(searchPath + raster_file, 2)

    # Create object for the whole image & set image_path as cwd, to save shapefiles.
    wholeImageObject = GeoImClip(searchPath)

    # Create bounding box from given coordinates.
    bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 4326)

    # Clip & save image, with georeference.
    image, metadata = wholeImageObject.clip(raster_file, bbox)

    # Convert selected quadrant to shapefile, and save to disk.
    vectorize(image, metadata, 'quadrant_2', 'ESRI Shapefile', None)


    # Quadrant_3 TEST
    # Aquire bounding box coordinates for selected quadrant.
    minx, maxx, miny, maxy = quadrants_coords(searchPath + raster_file, 3)

    # Create object for the whole image & set image_path as cwd, to save shapefiles.
    wholeImageObject = GeoImClip(searchPath)

    # Create bounding box from given coordinates.
    bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 4326)

    # Clip & save image, with georeference.
    image, metadata = wholeImageObject.clip(raster_file, bbox)

    # Convert selected quadrant to shapefile, and save to disk.
    vectorize(image, metadata, 'quadrant_3', 'ESRI Shapefile', None)
    

    # Quadrant_4 TEST
    # Aquire bounding box coordinates for selected quadrant.
    minx, maxx, miny, maxy = quadrants_coords(searchPath + raster_file, 4)

    # Create object for the whole image & set image_path as cwd, to save shapefiles.
    wholeImageObject = GeoImClip(searchPath)

    # Create bounding box from given coordinates.
    bbox = wholeImageObject.boundingBox(minx, maxx, miny, maxy, 4326)

    # Clip & save image, with georeference.
    image, metadata = wholeImageObject.clip(raster_file, bbox)

    # Convert selected quadrant to shapefile, and save to disk.
    vectorize(image, metadata, 'quadrant_4', 'ESRI Shapefile', None)
    """


"""
#### SPATIALLY JOIN SHAPEFILES BY ATTRIBUTES ####################################

# Filename of new merged shp.
out_filename = 'merged.shp'
# Geometry of new merged shp.
out_geom_type = ogr.wkbPolygon

# Create the output Driver.
out_driver = ogr.GetDriverByName('ESRI Shapefile')
# Delete files with the same name, if exist.
if os.path.exists(out_filename):
    out_driver.DeleteDataSource(out_filename)
# Create destination DataSource.
out_dst = out_driver.CreateDataSource(out_filename)
# Create the output Layer.
out_layer = out_dst.CreateLayer(out_filename, geom_type = out_geom_type)
# Get output Layer definition.
out_lay_defn = out_layer.GetLayerDefn()

# Gather fullpaths of shapefiles to spatially join (by attribute) & return as list of strings.
files2merge = []
for i in ['1.shp', '2.shp', '3.shp', '4.shp']:
    fileList1 = treeSearch(searchPath, 'quad', '_', i)
    files2merge.append(fileList1)
print(files2merge)

# Open one randmly selected layer, to copy fields' names
src = ogr.Open(files2merge[0][0])
lay = src.GetLayer()
lay_defn = lay.GetLayerDefn()
# Create field definition.
field_defn = lay_defn.GetFieldDefn(0)
# Field name, as string.
field_name = field_defn.GetName()
# Create new field definition.
rast_val_field = ogr.FieldDefn(field_name, ogr.OFTInteger)
# Add new field to created output Layer.
out_layer.CreateField(rast_val_field)

# Merge.
# For all fullpaths in list of shps
for file in files2merge:
    # Open file.
    src = ogr.Open(file[0])
    lay = src.GetLayer()
    for feat in lay:
        # Create feature for output layer definition.
        out_feat = ogr.Feature(out_lay_defn)
        # Get & set geometry of feature.
        out_feat.SetGeometry(feat.GetGeometryRef().Clone())
        # Set value of field (created before).
        out_feat.SetField(field_name, feat.GetField(field_name))
        # Add the current feature to output layer.
        out_layer.CreateFeature(out_feat)
        # Dereference the feature
        out_feat = None
        # force the layer to flush any pending writes to disk, and leave
        # the disk file in a consistent state.
        out_layer.SyncToDisk()


### Dissolve with geopandas lib
import geopandas as gpd

merged = gpd.read_file("/home/olyna/Documents/msc_thesis/rast2vect/merged.shp")
# query the first few records of the geom_type column
merged.head()

# dissolve the state boundary by region 
res = merged.dissolve(by='raster_val')    # Gives every class as one geometry !!!

# view the resulting geodataframe
res.to_file("dissolved.shp")


############################# TRY with geopandas - FAILED ########################

shp1_path = files2merge[1][0]
shp2_path = files2merge[2][0]

shp1 = gpd.read_file(shp1_path)
shp2 = gpd.read_file(shp2_path)

res = gpd.sjoin(shp2, shp1, how='left', op='touch')
res.to_file("joined.shp")
"""