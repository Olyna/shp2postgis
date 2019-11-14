"""
!/usr/bin/env python3
 -*- coding: utf-8 -*-
Created on Mon Oct  7 18:16:12 2019

@author: olyna
"""
import os
import psycopg2 as ps
import osgeo.ogr



def createsdb(host, dbname, user, password):
    """Create new postgres database.

    Args:
    host: IP or Localhost, as string.
    dbname: New database name, as string.
    user: Name of existin user, as string.
    password: User password, as string.

    Returns:
    Returns 0.
    """
    # Connect to default system database just to create a new user
    defaultcon = ps.connect(host='localhost', dbname='postgres', user='postgres', password='1234')
    defaultcon.autocommit = True
    # Open a cursor to perform database operations
    cur = defaultcon.cursor()

    try:
        # Create another, new database
        cur.execute("DROP DATABASE IF EXISTS "+str(dbname)+";")
        cur.execute("CREATE DATABASE "+str(dbname)+" WITH OWNER="+str(user)+" ENCODING='UTF8';")
        cur.execute("GRANT ALL PRIVILEGES ON DATABASE "+str(dbname)+" TO "+str(user)+";")
    finally:
        # Close communication with the database
        cur.close()
        defaultcon.close()
    return 0


def creategeotable(cursor, tablename):
    """Create new table & postgis extension.

    Args:
    cursor: existing psycopg2 cursor.
    tablename: Name of the new table, as string.

    Returns:
    Returns 0.
    """
    # Add postgis extension to current database
    cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    # Create table
    cursor.execute("DROP TABLE IF EXISTS "+str(tablename)+";")
    cmd = "CREATE TABLE "+str(tablename)+" (id SERIAL PRIMARY KEY, raster_val int, geom geometry(Polygon,4326));"
    cursor.execute(cmd)
    
    # Create index on geometry field
    cursor.execute("DROP INDEX IF EXISTS idx;")
    cursor.execute("CREATE INDEX idx ON "+str(tablename)+" USING GIST(geom);")
    return 0


def shp2table(cursor, shpname, tablename):
    """Shapefile to database table.

    Args:
    cursor: existing psycopg2 cursor.
    shpname: Path to input shapefile's folder, as string.
    tablename: Name of target table, as string.

    Returns:
    Returns 0.
    """
    srcFile = str(shpname)
    shapefile = osgeo.ogr.Open(srcFile)    
    layer = shapefile.GetLayer(0)
    print("Insert shapefile:...{}\nin database:...{}".format(shpname, tablename))
    print("Features in this shapefile:...{}".format(layer.GetFeatureCount()))
    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)  
        dn = feature.GetField("raster_val")
        wkt = feature.GetGeometryRef().ExportToWkt()  
        cursor.execute("INSERT INTO "+str(tablename)+"(raster_val, geom) VALUES\
                    ({}, ST_GeometryFromText('{}', 4326))".format(dn, wkt))

        if i == int(layer.GetFeatureCount() * 0.9):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.8):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.7):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.6):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.5):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.4):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.3):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.2):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        elif i == int(layer.GetFeatureCount() * 0.1):
            print("Proccess:...{}".format(round(i*100/layer.GetFeatureCount(), 2)))
        else:
            pass
    return 0