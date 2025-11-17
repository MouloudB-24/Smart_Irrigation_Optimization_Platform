from datetime import datetime, timedelta
import os
from typing import List, Tuple
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

from utils.json_utils import valid_and_pp_response


# Load variables environment
load_dotenv()


def get_st_ndvi(bbox_coords: List, logger: Logger, resolution: int=10, show_image: bool=False) -> dict:
    """
   summary.
    """
    
    try:
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
        # study period (5 days)
        end_date = datetime.now().date() - timedelta(days=30)
        start_date = end_date - timedelta(days=4)
        start_date_str = (start_date).strftime("%Y-%m-%d")
        end_date_str =(end_date).strftime("%Y-%m-%d")
        time_interval=(start_date_str, end_date_str)
        
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
        valid_and_pp_response(ndvi_data, logger)
    
        logger.info(f"get_st_ndvi - ndvi data were obtained")
    
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
            "timestamp": datetime.now().isoformat(),
            "time_interval": time_interval,
            "ndvi_min": float(np.nanmin(ndvi_values)),
            "ndvi_max": float(np.nanmax(ndvi_values)),
            "ndvi_mean": ndvi_mean
        }
        
        return ndvi_dict
    
    except Exception as e:
        logger.critical(f"get_st_ndvi - error obtaining NDVI data: {e}")
        return -1