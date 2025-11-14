from datetime import datetime, timedelta
import ee
from typing import List
from logging import Logger

from utils.json_utils import valid_and_pp_response


def get_st_evapotranspiration(bbox_coords: List, logger: Logger, scale=500):
    
    """summary"""
    
    try:
        try:
            ee.Initialize(project='eighth-opus-478010-i8')
            logger.debug("get_st_evapotranspiration - Earth Engine successfuly initialized")
        except ee.EEException as e:
            logger.error(f"get_st_evapotranspiration - Earth Engine initialisation error: {e}")
            return -1
        
        # create region
        region = ee.Geometry.Rectangle(bbox_coords)

        # study period (8 days)
        end_date = datetime.now().date() - timedelta(days=13)
        start_date = end_date - timedelta(days=8)
        start_date_str = (start_date).strftime("%Y-%m-%d")
        end_date_str =(end_date).strftime("%Y-%m-%d")
        
        # Load MOD16A2 collection
        collection = ee.ImageCollection("MODIS/061/MOD16A2").filterDate(start_date_str, end_date_str).select("ET")
        
        # et mean
        et_image = collection.mean().clip(region)
        
        # stat
        et_mean = et_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=scale,
            maxPixels=1e9).getInfo()
        valid_and_pp_response(et_mean, logger)
        
        return  {
            "timestamp": datetime.now().isoformat(),
            "evapostranspiration": {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "ET_mean": et_mean,
                "unit": "kg/m2/8days"
            }
        }
    
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