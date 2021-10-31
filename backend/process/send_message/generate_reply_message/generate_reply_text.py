from functools import reduce
import random
import json
import re
import requests
from collections import defaultdict
from backend.process.PretrainedModel import PretrainedModel

def generate_reply_text(self, result, reply_text):
    res_code = list(result.keys())[0]
    suggest_reply = ""
    check_end = False
    
    if res_code == 'hello':
        suggest_reply = reply_text['hello']
    elif res_code.startswith('inform_current_numbers'):
        loc,infected,recovered = res_code.split('-')[1:]
        suggest_reply = reply_text['inform_current_numbers'].format(loc,infected,recovered)
    elif res_code in ['request_age','request_sex','request_usual_symptom','request_rare_symptom','request_serious_symptom']:
        suggest_reply = reply_text[res_code]
    else:
        suggest_reply = reply_text['other']

    
    return suggest_reply, result, check_end