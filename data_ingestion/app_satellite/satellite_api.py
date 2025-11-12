import os
import ee
from typing import List, Tuple
import requests
import numpy as np
import matplotlib.pyplot as plt
from logging import Logger
from dotenv import load_dotenv
from sentinelhub import (
    SHConfig,
    DataCollection,
    SentinelHubRequest,
    BBox,
    bbox_to_dimensions,
    CRS,
    MimeType)


# Load variables environment
load_dotenv()


def get_st_temperature(lat: float, lon: float, date: int, logger: Logger, timeout: Tuple=(5, 10)) -> dict:
    
    """summary"""
    
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=T2M,T2M_MIN,T2M_MAX"
        f"&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={date}"
        f"&end={date}"
        f"&format=JSON"
    )
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        logger.debug("get_st_temperature - Timeout: the server took too long to respond")
    
    except requests.exceptions.ConnectionError:
        logger.debug("get_st_temperature - Connexion impossible: server inaccessible")
        
    except requests.exceptions.HTTPError as e:
        logger.debug(f"get_st_temperature - HTTP error: {e}")
    
    except requests.exceptions.RequestException as e:
        logger.debug(f"get_st_temperature - Unexpected error: {e}")


def get_st_ndvi(bbox_coords: List, time_interval: Tuple, logger: Logger, resolution: int=10, show_image: bool=False) -> dict:
    """
   summary.
    """

    # Copernicus API access configuration
    config = SHConfig()
    config.sh_client_id = os.environ["CLIENT_ID"]
    config.sh_client_secret = os.environ["CLIENT_SECRET"]
    config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    config.sh_base_url = "https://sh.dataspace.copernicus.eu"

    # define the study location
    aoi_bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)
    aoi_size = bbox_to_dimensions(aoi_bbox, resolution=resolution)

    # ndvi script
    evalscript_ndvi = """
    //VERSION=3
    function setup() {
    return {
        input: ["B04", "B08"],
        output: {
        id: "default",
        bands: 1,
        sampleType: "FLOAT32" 
        }
    };
    }

    function evaluatePixel(sample) {
    let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
    return [ndvi];
    }
    """

    # Sentinel Hub query
    request_ndvi = SentinelHubRequest(
        evalscript=evalscript_ndvi,
        input_data=[
            SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A.define_from(
                name="s2", service_url="https://sh.dataspace.copernicus.eu"),
            time_interval=time_interval,
            other_args={"dataFilter": {"mosaickingOrder": "leastCC", "maxCloudCoverage": 30}},)
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=aoi_bbox,
        size=aoi_size,
        config=config)

    # retreive data
    ndvi_data = request_ndvi.get_data()[0]
  
    # separation NDVI / mask
    ndvi_values = ndvi_data if ndvi_data.ndim == 2 else ndvi_data[:, :, 0]
    mask =  ndvi_data if ndvi_data.ndim == 2 else  ndvi_data[:, :, 1]

    # filter the values
    ndvi_valid = ndvi_values[mask > 0]
    ndvi_mean = float(np.nanmean(ndvi_valid))

    # optionel display
    if show_image:
        plt.figure(figsize=(10, 10))
        plt.imshow(ndvi_values, cmap="RdYlGn", vmin=-1, vmax=1)
        plt.colorbar(label="NDVI")
        plt.title(f"NDVI - Moyenne = {ndvi_mean:.3f}")
        plt.axis("off")
        plt.show()
    
    ndvi_dict = {
        "time_interval": time_interval,
        "ndvi_min": float(np.nanmin(ndvi_values)),
        "ndvi_max": float(np.nanmax(ndvi_values)),
        "ndvi_mean": ndvi_mean
    }
    logger.info(f"satellite_api.get_st_ndvi - The NDVIs ware successfully calculated")
    
    return ndvi_dict


def get_st_evapotranspiration(bbox_coords: List, start_date: str, end_date: str, logger: Logger="", scale=500):
    
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
    # ndvi = get_st_ndvi(
    #     bbox_coords=[-1.28, 48.30, -1.12, 48.40], # bbox Fougères
    #     time_interval=("2025-06-01", "2025-06-10")
    # )
    # print(ndvi)
    
    bbox_coords=[-1.28, 48.30, -1.12, 48.40]
    start = "2025-06-01"
    end   = "2025-06-09"

    # Initialiser
    result = get_st_evapotranspiration(bbox_coords, start, end, scale=500)
    print(result)