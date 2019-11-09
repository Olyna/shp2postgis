"""
!/usr/bin/env python3
 -*- coding: utf-8 -*-
Created on Mon Oct  7 18:16:12 2019

@author: olyna
"""
import fiona
import rasterio
from rasterio.features import shapes

def vectorize(raster_file, metadata, vector_file, driver, mask_value):
    """Extract vector from raster. Vector propably will include polygons with holes.
    
    Args:
    raster_file: raster image as ndarray.
    src: DatasetReader type. Keeps path to filesystem.
    vector_file: Pathname of output vector file, as string.
    driver: Kind of vector file format, as string.
    mask_value: No data value, as float or integer.
    
    Returns:
    Returns 0 & saves folder containing vector shapefile to cwd or to given path.
    """
    if mask_value is not None:
        mask = raster_file == mask_value
    else:
        mask = None
    
    results = (
        {'properties': {'raster_val': v}, 'geometry': s}
        for i, (s, v) 
        in enumerate(
            # The shapes iterator yields geometry, value pairs
            shapes(raster_file, mask=mask, transform=metadata['transform'])))

    with fiona.open(
            vector_file, 'w', 
            driver = driver,
            crs = metadata['crs'],
            schema = {'properties': [('raster_val', 'int')],
                    'geometry': 'Polygon'}) as dst:
        dst.writerecords(results)
    return 0