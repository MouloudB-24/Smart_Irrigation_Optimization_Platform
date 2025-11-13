import requests
from datetime import date, timedelta
from typing import Tuple
from logging import Logger


def get_soil_temperature(lat: float, lon: float, logger: Logger, timeout: Tuple=(5, 10)) -> dict:
    
    """summary"""
    
    date_ = int((date.today() - timedelta(days=3)).strftime("%Y%m%d"))
    
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=T2M,T2M_MIN,T2M_MAX"
        f"&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={date_}"
        f"&end={date_}"
        f"&format=JSON"
    )
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        soil_temp_data = response.json()
        logger.info("get_soil_temperature - Power NASA API - soil temperature data were obtained")
            
        return soil_temp_data
    
    except requests.exceptions.Timeout:
        logger.debug("get_soil_temperature - Timeout: the server took too long to respond")
        return -1
    
    except requests.exceptions.ConnectionError:
        logger.debug("get_soil_temperature - Connexion impossible: server inaccessible")
        return -1
        
    except requests.exceptions.HTTPError as e:
        logger.debug(f"get_soil_temperature - HTTP error: {e}")
        return -1
    
    except requests.exceptions.RequestException as e:
        logger.debug(f"get_soil_temperature - Unexpected error: {e}")
        return -1
    

if __name__ == "__main__":
    get_soil_temperature()
