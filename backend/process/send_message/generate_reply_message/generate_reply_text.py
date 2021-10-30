from functools import reduce
import random
import json
import re
import requests
from collections import defaultdict
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()

def generate_reply_text(self, result, reply_text,last_suggest):
    
    
    return suggest_reply, result, check_end