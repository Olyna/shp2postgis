# shp2postgis

This library serves to import a geo-referenced vector file (ESRI Shapefile), or part of it, into a spatial database.

In case of vector files, vectorizer module enables the conversion of a raster file into a vector shapefile, when the first consists of one band. For multiband images, each band must be selected separately. Output shapefile is saved in corresponding folder with all its accompanying files, in the same folder with the original image. Name of the new folder can be given by the user, and is the same name that the generated shapefile will receive.

Module clipImageByCoordinates creates an object, which consists only of the full-path in which one or more raster files are located. Allows the user to clip area of ​​interest from a selected raster image, by entering the corresponding geographical coordinates. The coordinates could be user-selected and represent any area of ​​the image, or they can be derived from the function quadrants_coords(), which returns the geographical coordinates of an image's quadrants. Clipped images are not saved by default, however, clipped image can be saved (optionally)). Output image is saved with .tif format, in the same folder with the original image, preserving the original filename, with the suffix 'clipped'. Also, retains metadata and has suitable geo-reference.

The functions pred2db allow you to create a new database, or connect to an existing database in order to create a new table and import data, or import data into an existing table.