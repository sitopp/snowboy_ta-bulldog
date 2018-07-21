#!/usr/bin/env python

import sys
import requests  
import logging

logging.basicConfig()
logger = logging.getLogger("snowboy")
logger.setLevel(logging.INFO)

model_no = sys.argv[1]
logger.info(str(model_no))




