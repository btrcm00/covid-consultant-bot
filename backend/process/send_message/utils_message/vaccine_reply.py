from unidecode import unidecode
import regex as re
from backend.config.regrex import *
import regex as re

disagree=disagree_reg
argree=agree_reg
def timevaccine(message, last_infor):
    res = {}
    res_code = ''
    num = 0

    if not last_infor['history']['state_vaccine']:
        for ele2 in message.split():
            for x in vaccine:
                if re.search(x, ele2.lower()):
                    res_code = 'inform_time_vaccine' + str(num + 1)
                    res[res_code] = last_infor
                    return res
                num = num + 1
            num = 0
        check = 'time_next'
        last_infor['history']['state_vaccine'] = 'time'
        res['inform_time_vaccine'] = last_infor
        return res
    else:
        for ele2 in message.split():
            for x in vaccine:
                if re.search(x, ele2.lower()):
                    res_code = 'inform_time_vaccine' + str(num + 1)
                    last_infor['history']['state_vaccine'] = ''
                    res[res_code] = last_infor
                    return res
                num = num + 1
            num = 0
    res['inform_time_vaccine'] = last_infor
    return res

def oldd(message, last_infor):
    res = {}
    if not last_infor['history']['state_vaccine']:
        last_infor['history']['state_vaccine'] = 'old'
        res['inform_old_vaccine'] = last_infor
        return res
    else:
        last_infor['history']['state_vaccine'] = ''
        if not re.search(disagree, message):
            last_infor['history']['chongchidinh'] = 'y'
            res['inform_old_vaccine2'] = last_infor
            return res
        else:
            last_infor['history']['chongchidinh'] = 'n'
            res['inform_old_vaccine3'] = last_infor
            return res

def injecc(message, last_infor):
    res = {}
    check = False
    if not last_infor['history']['state_vaccine']:
        last_infor['history']['state_vaccine'] = 'injec'
        res['inform_injected_vaccine'] = last_infor
        return res
    else:
        last_infor['history']['state_vaccine'] = ''
        if re.search(disagree, message) :
            check = False
        else:

            check = True
            if re.search(gan, message):
                last_infor['history']['gan'] = 'y'
            else:
                last_infor['history']['gan'] = 'n'
            if re.search(bia, message):
                last_infor['history']['ruoubia'] = 'y'
            else:
                last_infor['history']['ruoubia'] = 'n'
        if check:
            res['inform_injected_vaccine2'] = last_infor
            return res
        else:
            res['inform_injected_vaccine1'] = last_infor
            return res

def condition(message, last_infor):
    res = {}
    if not last_infor['history']['state_vaccine']:
        last_infor['history']['state_vaccine'] = 'condition'
        res['inform_condition_vaccine'] = last_infor
        return res
    else:
        if last_infor['history']['state_vaccine'] != 'condition2':
            if re.search(disagree, message) == None:

                last_infor['history']['state_vaccine'] = ''
                last_infor['history']['chongchidinh'] = 'y'
                res['inform_condition_vaccine3'] = last_infor
                return res
            else:

                last_infor['history']['state_vaccine'] = 'condition2'
                last_infor['history']['chongchidinh'] = 'n'
                res['request_condition_vaccine1'] = last_infor
                return res
        else:
            check = False
            last_infor['history']['state_vaccine'] = ''
            if re.search(disagree, message):
                check = False
            else:
                check = True
                if re.search(man, message) :
                    last_infor['history']['mantinh'] = 'y'
                else:
                    last_infor['history']['mantinh'] = 'n'

                if re.search(di, message):
                    last_infor['history']['diung'] = 'y'
                else:
                    last_infor['history']['diung'] = 'n'
            if check:
                res['inform_condition_vaccine4'] = last_infor
                return res
            else:
                res['inform_condition_vaccine2'] = last_infor
                return res
def cachdieutri(message, last_infor):
    res={}
    t=last_infor['history']['state_vaccine']
    if last_infor['history']['state_vaccine'] == 'cachdieutri':
        last_infor['history']['state_vaccine'] = ''

    if re.search(r'n[a|ặ]ng',message):
        res['inform_dieutrisautiemvaccine_nang_vaccine'] = last_infor
        return res
    if re.search(r'nh[e|ẹ]\s',message):
        res['inform_dieutrisautiemvaccine_nhe_vaccine'] = last_infor
        return res
    if t!='':
        res['inform_dieutrisautiemvaccine_truonghopkhac_vaccine'] = last_infor
        return res
    res['request_trieuchungsautiemvaccine_vaccine'] = last_infor
    return res

def vaccine_rep(message, last_infor):

    print('\t\t------------------TƯ VẤN VACCINE-------------------')
    check = ''
    res = {}
    checktrieuchung_nhe = re.search(trieuchung_nhe_check, message)
    checktrieuchung_nang = re.search(trieuchung_nang_check, message)
    if checktrieuchung_nang != None:
        message = re.sub(trieuchung_nang_check, ' triệu nặng ', message)
    else:
        if checktrieuchung_nhe != None:
            message = re.sub(trieuchung_nhe_check, ' triệu nhẹ ', message)

    for ele in ques:
        if re.search(ques[ele], message):
            check = ele
            break


    if check=='doituongtiemvaccine':
        res['inform_common_vaccine'] = last_infor
        return res
    elif check=='cachdieutri_trieuchungsautiem':
        return cachdieutri(message, last_infor)

    elif check=='bienchung_trieuchungsautiem':
        if re.search(bienchung_cotiem,message):
            res['inform_bienchung_cotim_vaccine'] = last_infor
            return res
        if re.search(bienchung_huyetkhoi_tieucau,message):
            res['inform_bienchung_huyetkhoigiamtieucau_vaccine'] = last_infor
            return res
        else:
            res['inform_dieutrisautiemvaccine_nang_vaccine'] = last_infor
            return res

    elif check=='thongtin_trieuchungsautiem':
        if re.search(r'n[a|ặ]ng',message):
            res['inform_trieuchungsautiemvaccine_nang_vaccine']=last_infor
            return res
        elif re.search(r'b[a|á]c',message):
            res['inform_candenbacsi_vaccine'] = last_infor
            return res
        else:
            res['inform_trieuchungsautiemvaccine_nhe_vaccine'] = last_infor
            return res
    elif check=='lamgisautiem_chuavenha':
        res['inform_lamgisautiem_chuavenha_vaccine'] = last_infor
        return res
    elif check == 'chuanbitruockhitiem':
        if re.search(r'gi[a|ấ]y',message)!=None:
            res['inform_chuanbitruockhitiem_giay_vaccine'] = last_infor
            return res
        if re.search(r'\s[ă|a]n\s', message) != None:
            res['inform_chuanbitruockhitiem_an_vaccine'] = last_infor
            return res
        res['inform_chuanbitruockhitiem_giay_vaccine-inform_chuanbitruockhitiem_an_vaccine'] = last_infor
        return res
    elif check == 'child':
        res['inform_vaccinecapphatchotreem_vaccine'] = last_infor
        return res

    elif check == 'f1':
        last_infor['history']['f'] = 1
        res['inform_f1_vaccine'] = last_infor
        return res

    elif check == 'f0':
        last_infor['history']['f'] = 0
        res['inform_f0_vaccine'] = last_infor
        return res
    elif check == 'number':
        res['inform_number_vaccine'] = last_infor
        return res
    elif check == 'register':
        res['inform_vaccine_register'] = last_infor
    elif check == 'old' or 'old' in last_infor['history']['state_vaccine']:
        return oldd(message, last_infor)
    elif check == 'women':
        last_infor['history']['cothai'] = 'y'
        last_infor['infor']['sex'] = 'female'
        res['inform_women_vaccine'] = last_infor
        return res
    elif check == 'time' or 'time' in last_infor['history']['state_vaccine']:
        return timevaccine(message, last_infor)
    elif check == 'condition' or 'condition' in last_infor['history']['state_vaccine']:
        return condition(message, last_infor)
    elif check == 'injected' or 'injec' in last_infor['history']['state_vaccine']:
        return injecc(message, last_infor)
    elif 'cachdieutri' in last_infor['history']['state_vaccine']:
        return cachdieutri(message, last_infor)
    if not res:
        res['inform_common_vaccine'] = last_infor
    return res