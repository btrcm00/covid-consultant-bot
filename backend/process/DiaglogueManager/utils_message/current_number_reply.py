import urllib.request, json 
import regex as re
from unidecode import unidecode

def current_numbers_rep(intent,last_infor):
    #----------------------------------------------#
    # - Bắt địa chỉ trong câu của bệnh nhân (tỉnh thành)
    # - Nếu bắt được thì sẽ reply theo tỉnh thành đó
    # - Nếu không thì mặc định là số liệu cho cả nước VN.
    #----------------------------------------------#
    print('\t\t------------------THÔNG TIN SỐ CA NHIỄM-------------------')
    data = {}
    res = {}
    
    with urllib.request.urlopen("https://api.apify.com/v2/key-value-stores/EaCBL1JNntjR3EakU/records/LATEST?disableRedirect=true") as url:
        data = json.loads(url.read().decode())
    infected = data['infected']
    recovered = data['recovered']
    died = data['died']
    loc = 'Việt Nam'
    
    try:
        loc,infected,died = [(ele['name'],ele['cases'], ele['death'])\
            for ele in data['locations'] if unidecode(ele['name'].lower()) in intent][0]
    except:
        pass
    recovered = 0
    res_code = 'inform_current_numbers+{}+{}+{}'.format(loc,infected,recovered)
    res[res_code] = last_infor
    return res