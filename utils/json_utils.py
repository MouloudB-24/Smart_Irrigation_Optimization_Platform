#####################################################################
#
# Project       : Smart Irrigation Optimization Platfom
#
# File          : utils.py
#
# Description   : Some common utility functions
#
# Created       : 30 october 2025
#
# Author        : Mouloud BELLIL
#
# Email         : mouloud.bellil@outlook.fr
#
#######################################################################

import json
from logging import Logger
import os
import sys
from typing import Union
import numpy as np


def valid_and_pp_response(response: Union[str, np.ndarray, any], logger: Logger, indents=4) -> None:
    
    """Console print: display site data only when logging level = debug"""
    
    try:
        logger.debug("data obtained:")
        
        if type(response) is str:
            logger.debug(json.dumps(json.loads(response), indent=indents))
        
        elif type(response) is np.ndarray and not np.isnan(response).all():
            logger.debug(response)
            
        else:
            logger.debug(json.dumps(response, indent=indents))
            
    except Exception as e:
        logger.critical(f"valid_and_pp_response - format of data obtained is invalid: {e}")
        logger.debug(response)
        os._exit(1)


def read_input_data(filepath, logger):
    
    """Lets read entire seed file in"""
    
    sites = []

    logger.info(f"utils.read_input_data Loading file: {filepath}")

    try:
        with open(filepath, "r") as f:
            sites = json.load(f)

    except IOError as e:
        logger.critical(f"utils.read_input_data I/O error: {filepath}: {e}")
        return -1

    except:  # handle other exceptions such as attribute errors
        logger.critical(f"utils.read_file Unexpected error: {filepath}, {sys.exc_info()[1]}")
        return -1

    return sites


def find_site(sites, siteId, logger):
    
    """Find the specific site in array of sites based on siteId"""
    
    logger.info(f"utils.read_site Called, SiteId: {siteId}")
    
    site = None
    found = False
    
    for site in sites:
        if site["siteId"] == siteId:
            
            logger.info(f"utils.find_site Retreived, SiteId: {siteId}")
            
            return site
    
    if not found:
        
        logger.critical(f"utils.find_site Completed, SiteId: {siteId} NOT FOUND")
        
        return -1
    