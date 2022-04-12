from backend.process.config import PretrainedModel
import numpy as np

import tensorflow

import requests
import platform
import base64
import io
import json
# from PIL import Image
import json

from backend.config.config import get_config
config_app = get_config()
models = PretrainedModel()

def send_image(data):
    pass