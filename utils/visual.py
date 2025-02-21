import matplotlib.pyplot as plt
import xarray as xr

class Visual:
    def __init__(self, slice):
        """
        Initialise the class for visualisation of datacube slices from xarray DataArray

        Parameters:
        slice (xr.DataArray or xr.Dataset): a single slice of the xarray object.
        """
        self.slice = slice
        
    def map(self):
        crs = self.slice.attrs.get('crs', 'CRS not found') # extract crs from metadata
        print(crs)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        im = self.slice.plot.imshow(cmap='viridis', add_colorbar=False)
        cbar = fig.colorbar(im, ax=ax) #add colourbar
        cbar.set_label("Water Quality Index (WQI)") 

        timestamp = self.slice.coords['t'].values
        timestamp_str = str(timestamp)

        # axes
        ax.set_title(f"Water Quality Index (WQI), t = {timestamp_str}\n CRS = {crs}")
        ax.set_xlabel("X coordinate")
        ax.set_ylabel("Y coordinate")