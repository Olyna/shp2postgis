#!/usr/bin/env python3
# -*- coding: utf-8 -*-




def vectorize(raster_file, metadata, vector_file, driver, mask_value=None):
    """Extract vector from raster. Vector propably will include polygons with holes.
    
    Args:
    raster_file (ndarray): raster image.
    src (DatasetReader type): Keeps path to filesystem.
    vector_file (string): Pathname of output vector file.
    driver (string): Kind of vector file format.
    mask_value (float or integer): No data value.
    
    Returns:
    Returns None & saves folder containing vector shapefile to cwd or to given path.
    """
    import fiona
    from rasterio.features import shapes
    import datetime as dt

    start = dt.datetime.now()

    if mask_value is not None:
        mask = raster_file == mask_value
    else:
        mask = None
    
    print("Extract id, shapes & values...")
    features = ({'properties': {'raster_val': v}, 'geometry': s} for i, (s, v) in enumerate(
            # The shapes iterator yields geometry, value pairs.
            shapes(raster_file, mask=mask, connectivity=4, transform=metadata['transform'])))

    print("Save to disk...")
    with fiona.Env():
        with fiona.open(
                vector_file, 'w', 
                driver = driver,
                crs = metadata['crs'],
                schema = {'properties': [('raster_val', 'int')], 'geometry': 'Polygon'}) as dst:
            dst.writerecords(features)

    end = dt.datetime.now()
    print("Elapsed time to vectorize raster to shp {}:\n{} mins".format(
        vector_file, (int((end-start).seconds/60)))
    return None