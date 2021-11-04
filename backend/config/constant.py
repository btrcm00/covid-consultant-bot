import regex as re
import os
import json
from backend.config.regrex import *
from backend.config.config import get_config
config_app = get_config()

with open(config_app['models_chatbot']['emergency_contact'], encoding='utf-8') as f:
    contact_emergency = json.load(f)

CODE_RETURN = [
    'inform_symptoms_info','request_age','request_sex', 'request_serious_symptom',
    'request_usual_symptom', 'request_rare_symptom', 'inform_high_prop', 'inform_low_prop',
    'inform_current_numbers', 'inform_covid_infor', 'inform_how_spreading', 'inform_precautions',
    'inform_medication', 'inform_common_contact', 'inform_tophanungnhanh','inform_tramyte',
    'inform_common_vaccine', 'inform_time_vaccine', 'inform_time_vaccine1', 'inform_time_vaccine2', 'inform_time_vaccine3', 'inform_time_vaccine4', 'inform_f1_vaccine','inform_f0_vaccine',
    'inform_women_vaccine','inform_old_vaccine','inform_old_vaccine2','inform_old_vaccine3','inform_injected_vaccine','inform_injected_vaccine1','inform_injected_vaccine2','inform_condition_vaccine','inform_condition_vaccine1','inform_condition_vaccine2','inform_condition_vaccine3','inform_condition_vaccine4',
    'hello','other','ok','req'
]

province_lst = ["Bắc Giang","Bắc Kạn","Cao Bằng","Hà Giang","Lạng Sơn","Phú Thọ","Quảng Ninh","Thái Nguyên","Tuyên Quang","Lào Cai","Yên Bái","Điện Biên","Hòa Bình","Lai Châu","Sơn La","Bắc Ninh","Hà Nam","Hải Dương","Hưng Yên","Nam Định","Ninh Bình","Thái Bình","Vĩnh Phúc","Hà Nội","Hải Phòng","Hà Tĩnh","Nghệ An","Quảng Bình","Quảng Trị","Thanh Hóa","Thừa Thiên Huế","Đắk Lắk","Đắk Nông","Gia Lai","Kon Tum","Lâm Đồng","Bình Định","Bình Thuận","Khánh Hòa","Ninh Thuận","Phú Yên","Quảng Nam","Quảng Ngãi","Đà Nẵng","Bà Rịa–Vũng Tàu","Bình Dương","Bình Phước","Đồng Nai","Tây Ninh","TP. Hồ Chí Minh","An Giang","Bạc Liêu","Bến Tre","Cà Mau","Đồng Tháp","Hậu Giang","Kiên Giang","Long An","Sóc Trăng","Tiền Giang","Trà Vinh","Vĩnh Long","Cần Thơ"] 

MAP_TO_DISTRICT_HCM = {'q1': r'quận 1', 'q2': r'quận 2', 'q3': r'quận 3', 'q4': r'quận 4', 'q5': r'quận 5', 'q6': r'quận 6', 'q7': r'quận 7', 'q8': r'quận 8', 'q9': r'quận 9',
                       'q10': r'quận 10', 'q11': r'quận 11', 'q12': r'quận 12'}
DISTRICT = r'([1-9]+|b[i|ì]nh\s*th[a|ạ]nh|t[a|â]n\s*ph[u|ú]|b[i|ì]nh\s*t[a|â]n|b[i|ì]nh\s*ch[a|á]nh|nh[a|à]\s*b[e|è]|g[o|ò]\s*v[a|á|ấ|â]p|ph[u|ú]\s*nhu[a|ạ|â|ậ]n|t[a|â]n\s*b[i|ì][|n]h|th[u|ủ]\s[d|đ][u|ú|ư|ứ]c|c[a|à|ầ|â]n\s*gi[o|ơ|ờ]|c[u|ủ]\schi|h[o|ó]c\s*m[o|ô]n)'
