import json 
import regex as re
import urllib.request

from backend.config.constant import province_lst
from backend.config.config import Config

def current_numbers_rep(text, last_infor):
    #----------------------------------------------#
    # - Bắt địa chỉ trong câu của bệnh nhân (tỉnh thành)
    # - Nếu bắt được thì sẽ reply theo tỉnh thành đó
    # - Nếu không thì mặc định là số liệu cho cả nước VN.
    #----------------------------------------------#
    print('\t\t------------------THÔNG TIN SỐ CA NHIỄM-------------------')
    data = {}
    res = {}
    
    with urllib.request.urlopen(Config.current_number_url) as url:
        data = json.loads(url.read().decode())
        
    infected = data['infected']
    recovered = data['recovered']
    died = data['died']
    caseToday = data['infectedToday']
    loc = 'Việt Nam'
    text = re.sub(r'sài gòn|hồ chí minh|tphcm', 'tp. hồ chí minh', text)
    text = re.sub(r'huế', 'thừa thiên huế', text)
    text = re.sub(r'vũng tàu', 'bà rịa – vũng tàu', text)

    for pro in province_lst:
        if pro.lower() in text.lower():
            loc,caseToday,recovered,infected,died = [(ele['name'],ele['casesToday'],ele['recovered'],ele['cases'], ele['death']) \
                                            for ele in data['locations'] if ele['name'].lower() == pro.lower()][0]
    res_code = 'inform_current_numbers+{}+{}+{}+{}'.format(loc,infected,caseToday,died)
    res[res_code] = last_infor
    return res