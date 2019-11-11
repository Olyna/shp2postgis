#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:10:36 2019

@author: Gounari Olympia
"""

import rasterio
from rasterio.plot import show
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import os
import json
import numpy as np


def quadrants_coords(raster_file, quadrant):
    """Clip selected quadrant of raster file.

    Args:
    raster_file (string): Raster image file fullpath.
    quadrant: One of the four pieces. Start counting from upper left corner, clockwise.
              Integer in range [1,4].

    Returns:
    Bounding box coordinates of selected quadrant.
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
            print('Quadrant must be integer in range [1,4].')

    return(minx, maxx, miny, maxy)



class GeoImClip:
    def __init__(self, searchPath):
        # Path to where the searching will begin.
        self.searchPath = searchPath
        
        # Change current working directory to given search-path.
        os.chdir(self.searchPath)
        print('Searching sub-directories in path "{}"\n'.format(self.searchPath))
        
        
    def boundingBox(self, minx, maxx, miny, maxy, srid):
        """Generates polygon geometry, from given coordinates.

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
        

    def getFeatures(self, gdf):
        """Parse features from GeoDataFrame in such a manner that
        rasterio wants them. Called from function clip().

        Args:
        gdf: geometry dataframe.
        """
        return [json.loads(gdf.to_json())['features'][0]['geometry']]
    
    
    def clip(self, im, geometry, write=False):
        """Clip image & update metadata of output image. Option to write
        output image to disk.

        Args:
        im (string): Path to image.
        geometry: Geometry dataframe used as bounding box to clip image.
        write (bool (opt)): Whether to save output raster to disk. Defaults to False. 

        Returns:
        out_img: clipped array.
        out_meta: updated metadata for clipped raster.
        """
        # Read image without load it on disk (dataset object)
        data = rasterio.open(im, nodata=0)
        # Convert geometry to image's Coord. Ref. Syst.
        geom = geometry.to_crs(crs=data.crs.data)
        # Plot original image
        #show((data, 1), cmap='terrain')
        coords = self.getFeatures(geom)
        # Clip image. Keep output array and transformation to update metadata
        out_img, out_transform = mask(dataset=data, shapes=coords, crop=True)
        # Copy original metadata
        out_meta = data.meta.copy()
        #print(out_meta)
        # Update metadata for output image
        out_meta.update({"driver": "GTiff",
                     "height": out_img.shape[1],
                     "width": out_img.shape[2],
                     "transform": out_transform,
                     "crs": data.crs.data})

        if write == True:
            # New name for output image
            out_tif = im.split('.')[0] + '_clipped.TIF'
            # Write output image to disk
            with rasterio.open(out_tif, "w", **out_meta) as dest:
                dest.write(out_img)

            """
            # Plot output image
            clipped = rasterio.open(out_tif)
            #show((clipped, 1), cmap='terrain')
            """
        else:
            pass

        return out_img, out_meta
