import rasterio
import geopandas as gpd
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling

class VectorProc:
    def __init__(self, raster_path: str):
        """
        Initialise RasterProc with input raster dataset (GeoTIFF)

        Parameters:
            raster_path (str): path to raster dataset
        """

        self.raster_path = raster_path
        self.raster_crs = self.get_raster_crs()
    
    def get_raster_crs(self):
        """Get CRS from raster file"""
        with rasterio.open(self.raster_path) as ds:
            return ds.crs


    def reproject_vec2ras(self, vector: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Reprojects geodataframe to match the raster CRS

        Parameters:
            vector (gpd.GeoDataFrame): The vector data to be reprojected.
            raster_path (str): Path to the raster file.

        Returns:
            gpd.GeoDataFrame: The reprojected vector data.
        """

        vector_crs = vector.crs
        print(vector_crs, self.raster_crs)
        if vector_crs != self.raster_crs:
            print(f"Reprojecting vector dataset from {vector_crs} to {self.raster_crs}...")
            return vector.to_crs(self.raster_crs)

    def reproject_Ras2Leaflet(self, reproj_path: str) -> str:
        """
        Reprojects the raster to match the Leaflet CRS (EPSG:3857) an visualise (nearest neighbour resampling).

        Parameters:
        reproj_path (str): Path to save the reprojected raster.

        Returns:
        str: Path to the reprojected raster.
        """
    
        vector_crs = 'EPSG:3857' # for Leaflet
    
        # Open the raster dataset
        with rasterio.open(self.raster_path) as src:
            # Get the transformation and new dimensions for the reprojected raster
            transform, width, height = calculate_default_transform(
                src.crs, vector_crs, src.width, src.height, *src.bounds
            )
        
            # Create a new metadata dictionary for the reprojected raster
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': vector_crs,
                'transform': transform,
                'width': width,
                'height': height
            })

            # Check if 'descriptions' exists in the original raster's metadata
            descriptions = kwargs.get('descriptions', [])
        
            # Open the output raster file to write the reprojected data
            with rasterio.open(reproj_path, 'w', **kwargs) as dst:
                print(f"Total number of bands in the original raster: {src.count}")
            # Loop through all the bands in the original raster
                for i in range(1, src.count + 1):
                    print(f"Reprojecting band {i}/{src.count}...")
                    # Reproject each band
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=vector_crs,
                        resampling=Resampling.nearest
                    )

                    # After writing the bands, set the band descriptions
                if descriptions:
                    for i, band_desc in enumerate(descriptions, start=1):
                        print(f"Setting description for band {i}: {band_desc}")
                        dst.set_band_description(i, band_desc)
        print("-"*40)
        # Return the path to the reprojected raster
        return reproj_path
    
    def reproject_RasByVec(self, vector: gpd.GeoDataFrame, reproj_path: str) -> str:
        """
        Reprojects the raster to match the CRS of the given vector dataset (nearest neighbour resampling).

        Parameters:
        vector (gpd.GeoDataFrame): The vector dataset whose CRS will be used.
        reproj_path (str): Path to save the reprojected raster.

        Returns:
        str: Path to the reprojected raster.
        """
    
        # Get the CRS of the vector dataset
        vector_crs = vector.crs
    
        # Open the raster dataset
        with rasterio.open(self.raster_path) as src:
            # Get the transformation and new dimensions for the reprojected raster
            transform, width, height = calculate_default_transform(
                src.crs, vector_crs, src.width, src.height, *src.bounds
            )
        
            # Create a new metadata dictionary for the reprojected raster
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': vector_crs,
                'transform': transform,
                'width': width,
                'height': height
            })

            # Check if 'descriptions' exists in the original raster's metadata
            descriptions = kwargs.get('descriptions', [])
        
            # Open the output raster file to write the reprojected data
            with rasterio.open(reproj_path, 'w', **kwargs) as dst:
                print(f"Total number of bands in the original raster: {src.count}")
            # Loop through all the bands in the original raster
                for i in range(1, src.count + 1):
                    print(f"Reprojecting band {i}/{src.count}...")
                    # Reproject each band
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=vector_crs,
                        resampling=Resampling.nearest
                    )

                    # After writing the bands, set the band descriptions
                if descriptions:
                    for i, band_desc in enumerate(descriptions, start=1):
                        print(f"Setting description for band {i}: {band_desc}")
                        dst.set_band_description(i, band_desc)
        print("-"*40)
        # Return the path to the reprojected raster
        return reproj_path


