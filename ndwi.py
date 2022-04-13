def ndwi(direct):
    
    # Import libraries

    import rasterio
    import numpy as np
    import glob
    from osgeo import gdal
    import natsort
   

    # Search directory for desired bands

    green_f = natsort.natsorted(glob.glob(direct + '**B03.jp2'))
    nir_f = natsort.natsorted(glob.glob(direct + '**B08.jp2'))
    
    for g, n in zip(green_f, nir_f):
        
        # Define a function to calculate NDWI using band arrays for green and NIR

        def ndwi (green, nir):
            return ((green - nir) / (green + nir))
        
        # Open each band using gdal

        green_link = gdal.Open(g)
        nir_link = gdal.Open(n)
        
        # read in each band as array and convert to float for calculations

        green = green_link.ReadAsArray().astype(np.float)
        nir = nir_link.ReadAsArray().astype(np.float)
        
        # Call the ndvw() function on green, NIR band
        ndwi2 = ndwi(green, nir)
        
        # Create output filename based on input name 
        outfile_name = g.split('_B')[0] + '_NDWI.tif'

        x_pixels = ndwi2.shape[0] # number of pixels in x
        y_pixels = ndwi2.shape[1] # number of pixels in y
        
        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')
        
        # Create driver using output filename, x and y pixels, # of bands, and datatype
        ndwi_data = driver.Create(outfile_name,x_pixels, y_pixels, 1, gdal.GDT_Float32)
        
        # Set NDWI array as the 1 output raster band
        ndwi_data.GetRasterBand(1).WriteArray(ndwi2)
        
        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans=green_link.GetGeoTransform() # Grab input GeoTranform information
        proj=green_link.GetProjection() # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        ndwi_data.SetGeoTransform(geotrans) 
        ndwi_data.SetProjection(proj)
        ndwi_data.FlushCache()
        ndwi_data=None