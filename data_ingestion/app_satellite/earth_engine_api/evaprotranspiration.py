import ee
from typing import List
from logging import Logger


def get_st_evapotranspiration(bbox_coords: List, start_date: str, end_date: str, logger: Logger, scale=500):
    
    """summary"""
    
    try:
        try:
            ee.Initialize(project='eighth-opus-478010-i8')
            logger.info("get_st_evapotranspiration - Earth Engine successfuly initialized")
        except ee.EEException as e:
            logger.error(f"get_st_evapotranspiration - Earth Engine initialisation error: {e}")
            return -1
        
        # create region
        region = ee.Geometry.Rectangle(bbox_coords)
        
        # Load MOD16A2 collection
        collection = ee.ImageCollection("MODIS/061/MOD16A2").filterDate(start_date, end_date).select("ET")
        
        # et mean
        et_image = collection.mean().clip(region)
        
        # stat
        et_mean = et_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=scale,
            maxPixels=1e9).getInfo()
        
        return  et_mean
    
    except Exception as e:
        logger.error(f"get_st_evapotranspiration - unexpected error: {e}")
        return -1


if __name__ == "__main__":
    bbox_coords=[-1.28, 48.30, -1.12, 48.40]
    start = "2025-06-01"
    end   = "2025-06-09"

    # Initialiser
    result = get_st_evapotranspiration(bbox_coords, start, end, scale=500)
    print(result)