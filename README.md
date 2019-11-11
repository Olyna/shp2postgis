# shp2postgis

This library serves to import a geo-referenced vector file (or part of it) into a spatial database. It also enables the conversion of a raster file into a vector when it consists of a channel.
Initially, class GeoImClip allows the creation of an object, which consists only of the full-path in which one or more raster files are located. Allows the user to clip the area of ​​interest from a normalized image by entering the corresponding geographical coordinates. The coordinates could be user-selected and represent any area of ​​the image, or they can be derived from the function quadrants_coords(), which returns the geographical coordinates of an image's quadrants.

The functions pred2db allow you to create a new database, or connect to an existing database in order to create a new table and import data, or import data into an existing table.