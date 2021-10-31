import urllib.request, json 
import regex as re
from backend.config.constant import province_lst

def current_numbers_rep(text, reply_text):
    #----------------------------------------------#
    # - Bắt địa chỉ trong câu của bệnh nhân (tỉnh thành)
    # - Nếu bắt được thì sẽ reply theo tỉnh thành đó
    # - Nếu không thì mặc định là số liệu cho cả nước VN.
    #----------------------------------------------#
    
    data = {}
    with urllib.request.urlopen("https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true") as url:
        data = json.loads(url.read().decode())
    infected = data['infected']
    recovered = data['recovered']
    died = data['died']
    loc = 'Việt Nam'
    text = re.sub(r'hcm|sài gòn|tphcm|tp\.hcm|sg', 'tp. hồ chí minh', text)
    text = re.sub(r'huế', 'thừa thiên huế', text)
    text = re.sub(r'vtau|vung\s*tau|vũng tàu|vt', 'bà rịa – vũng tàu', text)

    for pro in province_lst:
        if pro.lower() in text:
            loc,infected,died = [(ele['name'],ele['cases'], ele['death']) for ele in data['locations'] if ele['name'].lower() == pro.lower()][0]
            recovered = 0
    res_code = 'inform_current_number'
    return res[0].format(loc, infected, recovered, died)
