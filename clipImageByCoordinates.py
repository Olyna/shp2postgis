#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:10:36 2019

UNDER CONSTRUCTION
"""

import rasterio
from rasterio.plot import show
from rasterio.windows import Window
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import os
import numpy as np
import cv2
import logging


logger = logging.getLogger(__name__)
# Override the default severity of logging.
logger.setLevel('INFO')
# Use StreamHandler to log to the console.
stream_handler = logging.StreamHandler()
# Don't forget to add the handler.
logger.addHandler(stream_handler)


def quadrants_coords(raster_file, quadrant):
    """Clip selected quadrant of raster file.

    Args:
    raster_file (string): Raster image file fullpath.
    quadrant (integer): One of the four pieces. Start counting from upper left corner, clockwise.
              Integer in range [1,4].

    Returns:
    Bounding box coordinates of selected quadrant (minx, maxx, miny, maxy).
            minx = left = west
            maxx = right = east
            miny = bottom = south
            maxy = top = north
    """
    with rasterio.open(raster_file) as src:

        if quadrant == 1:
            minx = src.bounds.left
            maxy = src.bounds.top
            maxx = src.bounds.left + (src.bounds.right - src.bounds.left)/2 # middle point
            miny = src.bounds.top - (src.bounds.top - src.bounds.bottom)/2 # middle point

        elif quadrant == 2:
            minx = src.bounds.left + (src.bounds.right - src.bounds.left)/2 # upper middle point
            maxy = src.bounds.top # upper middle point
            maxx = src.bounds.right # right middle point
            miny = src.bounds.bottom + (src.bounds.top - src.bounds.bottom)/2 # right middle point

        elif quadrant == 3:
            minx = src.bounds.left + (src.bounds.right - src.bounds.left)/2 # middle point
            maxy = src.bounds.top - (src.bounds.top - src.bounds.bottom)/2 # middle point
            maxx = src.bounds.right
            miny = src.bounds.bottom

        elif quadrant == 4:
            minx = src.bounds.left # left middle point
            maxy = src.bounds.bottom + (src.bounds.top - src.bounds.bottom)/2 # left middle point
            maxx = src.bounds.left + (src.bounds.right - src.bounds.left)/2 # lower middle point
            miny = src.bounds.bottom # lower middle point

        else:
            logger.error('Quadrant must be integer in range [1,4].')

    return(minx, maxx, miny, maxy)




class GeoImClip:
    def __init__(self, searchPath):
        # Path to where the searching will begin.
        self.searchPath = searchPath
        
        # Change current working directory to given search-path.
        os.chdir(self.searchPath)
        logger.debug('Searching sub-directories in path "{}"\n'.format(self.searchPath))
        
        
    def boundingBox(self, minx, maxx, miny, maxy, srid):
        """Generates polygon geometry, from given coordinates.
        Given coordinates must be in the same CRS, as image's CRS.

        Args:
        minx, maxx, miny, maxy : float number.
        srid (integer): coordinates reference system id.

        Returns:
        geometry: polygon geometry dataframe.
                    minx = left = west
                    maxx = right = east
                    miny = bottom = south
                    maxy = top = north
        """
        # Create bounding box
        bbox = box(minx, miny, maxx, maxy)
        # Create geometry in geoDataFrame forma
        geometry = gpd.GeoDataFrame({'geometry': bbox},
                                    index=[0], crs=from_epsg(srid))
        return geometry


    def clip(self, im, geometry, newname, resize=False, write=True):
        """Clip image & update metadata of output image. Option to write
        output image to disk.

        Args:
        im (string): Path to image.
        geometry (geoDataframe): Geometry dataframe used as bounding box to clip image.
        newname (string): Piece of string added to the end of the new filename.
        write (bool (opt)): Whether to save output raster to disk. Defaults to True. 

        Returns:
        out_img (array): clipped array.
        out_meta (dictionary): updated metadata for clipped raster.
        """
        # New name for output image. Split on second occurence of dot.
        out_tif = im.split('.')[0]+ '.'+ im.split('.')[1] + str(newname) + '.tif'

        if os.path.exists(out_tif) == True and os.stat(out_tif).st_size != 0:
            # Pass if file already exists & it's size is not zero.
            return

        with rasterio.open(im) as src:
            # Image metadata.
            metadata = src.meta

            # # It doesn't work well. It changes orinal minx & maxy.
            # # Convert window's CRS to image's CRS.
            # geom = geometry.to_crs(crs=metadata['crs'])

            # Convert x,y to row, col.
            row_start, col_start = src.index(geometry.bounds['minx'][0], geometry.bounds['maxy'][0])
            row_stop, col_stop = src.index(geometry.bounds['maxx'][0], geometry.bounds['miny'][0])

            # Parse pixel size from metadata.
            pixelSize = list(metadata['transform'])[0]

            # Create the new transformation.
            transf = rasterio.transform.from_origin(
                geometry.bounds['minx'][0], geometry.bounds['maxy'][0], pixelSize, pixelSize)

            # Update metadata.
            metadata.update(
                driver='GTiff', transform=transf,
                height=(row_stop-row_start), width=(col_stop-col_start))

            # Construct a window by image coordinates.
            win = Window.from_slices(slice(row_start, row_stop), slice(col_start, col_stop))

            # Clip image.
            out_img = src.read(1, window=win)

        if resize == True:
            # Create the new transformation.
            transf = rasterio.transform.from_origin(
                geometry.bounds['minx'][0], geometry.bounds['maxy'][0], pixelSize//2, pixelSize//2)

            # Update metadata for output image
            metadata.update({"height": out_img.shape[0]*2,
                        "width": out_img.shape[1]*2,
                        "transform": transf})
            # Upsample.
            out_img = cv2.resize(
                out_img, (2*out_img.shape[0], 2*out_img.shape[1]), interpolation=cv2.INTER_LINEAR)

        if write == True:
            # Reshape as rasterio needs the shape.
            temp = out_img.reshape(1, out_img.shape[0], out_img.shape[1])
            # Write output image to disk
            with rasterio.open(out_tif, "w", **metadata) as dest:
                dest.write(temp)

            """
            # Plot output image
            clipped = rasterio.open(out_tif)
            #show((clipped, 1), cmap='terrain')
            """
        return out_img, metadata