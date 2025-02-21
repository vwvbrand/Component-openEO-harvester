import xarray as xr
import rioxarray
import rasterio
import numpy as np

def check_res_nc(ds: str, bands: list):
    
    '''
    Checks spatial resolution for netcdf datasets

    Parameters:
    ds (str): netcdf file
    bands (list): names of bands (dimensions, variables) in netcdf
    '''

    '''print("Dimensions:", ds.dims)
    print("Coordinates:", ds.coords)'''

    ds = xr.open_dataset(ds)

    for band in bands:
        #  get the spatial resolution by checking the 'x' and 'y' coordinates for each band
        if band in ds:
            x_res = ds.coords['x'].diff('x').mean().values
            y_res = ds.coords['y'].diff('y').mean().values
            print(f"Spatial resolution for band {band}:")
            print(f"X: {x_res}")
            print(f"Y: {y_res}")
        else:
            print(f"Band {band} is not available.")
    print("-"*40)

def check_res_tif(ds: str):
    '''
    Checks spatial resolution for geotiff datasets

    Parameters:
    ds (str): geotiff file
     '''
    with rasterio.open(ds) as dataset:
        for i in range(1, dataset.count + 1):  # loop over bands
            print(f"Band {i} resolution: {dataset.res}")
        print("-"*40)

def check_stats_nc(ds: str, bands: list):
    '''
    Checks spatial resolution for netcdf datasets, each variable/dimension

    Parameters:
    ds (str): netcdf file
    bands (list): names of bands (dimensions, variables) in netcdf

    Returns:
    stats (list): tuples - name of band, minimum value in band, no data value in band
    '''
    ds = xr.open_dataset(ds)
    stats = []
    
    # basic info
    print("NetCDF Dataset Info:")
    print("-" * 40)
    """
    print("Dimensions:")
    print(ds.dims)
    print("Variables:")
    print(ds.variables)
    """

    # temporal dimension
    if 't' in ds.dims:
        print(f"Number of timestamps: {ds.dims['t']}")
        print(f"Time range: {ds['t'].values[0]} to {ds['t'].values[-1]}")
        
    for band in bands:
        if band in ds:
            print(f"{band} band shape: {ds[band].shape}")
            # stats ignoring nodata value
            band_data = ds[band].values # extract as a numpy array
            band_mean = np.nanmean(band_data) 
            band_min = np.nanmin(band_data)
            band_max = np.nanmax(band_data)
            band_std = np.nanstd(band_data)
            band_sum = np.nansum(band_data)

            nodata_val = ds[band].rio.nodata

            stats.append((band, band_min, nodata_val))

            print(f"Stats:")
            print(f"  Nodata value: {nodata_val}")
            print(f"  Mean: {band_mean}")
            print(f"  Min: {band_min}")
            print(f"  Max: {band_max}")
            print(f"  Standard deviation: {band_std}")
            print("-" * 40)
            
        else:
            print(f"Band {band} is not available.")
            print("-" * 40)

    return(stats)
            