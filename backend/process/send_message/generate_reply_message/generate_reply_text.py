from functools import reduce
import random
import json
import re
import requests
from collections import defaultdict
from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()

def generate_reply_text(self, result, reply_text,last_suggest,code_product):
    # ------------ Tạo ra câu trả lời hoàn chỉnh dựa vào các mã code -------------
    # ------------Đối với những kết quả có lưu image, reset nó về None tránh lưu trữ trên DB------
    # ------------Kịch bản cụ thể xem trên wiki-------------------------
    suggest_reply = ''
    #Xử lý cho case not found size hay not found 
    #Tách ra những mã code return cùng product

    
    return suggest_reply, result, check_end