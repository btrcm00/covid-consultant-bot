from unidecode import unidecode
import regex as re
from backend.config.regrex import *

def buy_medicine(message, last_infor, last_intent):
    res = {}
    if not last_infor['history']['state_medication']:
        last_infor['history']['state_medication'] ='buymedicine'
        if re.search(ques['f1'], message) or re.search(ques['f0'], message) or last_infor['history']['f']==0:
            res['medication_buymedicine_replyf1f0'] = last_infor
        else:
            res['medication_buymedicine_checkvaccine']=last_infor
        return res
    else:
        if "checkvaccine" in last_intent:
            if re.search(disagree, message):
                last_infor['history']['state_medication'] = ''
                res['medication_buymedicine_normal'] = last_infor
            else:
                res['medication_buymedicine_checkf1f0'] = last_infor
            return res
        if "checkf1f0" in last_intent:
            last_infor['history']['state_medication'] = ''
            if re.search(disagree, message):
                res['medication_buymedicine_replyf1f0'] = last_infor
            else:
                res['medication_buymedicine_normal'] = last_infor
            return res
        res['other']=last_infor
        return res
def spo_oxy(message, last_infor):
    res={}
    print("spo_oxy")
    if re.search(cachdo, message):
        res['medication_spo_cachdo']=last_infor
    elif re.search(r'mua', message):
        res['medication_spo_cachdo'] = last_infor
    else:
        res['medication_spo_thongtin'] = last_infor
    return res
def device(message, last_infor):
    res={}
    if re.search(f0_macbenh, message) or last_infor['history']['f']==0:
        res['medication_spo_thietbichonguoibenh']=last_infor
    else:
        res['medication_spo_thietbichongbthhoacf>1'] = last_infor
    return res
def saukhithiem_vaccine(message, last_infor):
    res={}
    if not last_infor['history']['state_medication']:
        last_infor['history']['state_medication'] = 'saukhitiemvaccine'
        res['medication_vaccine_check']=last_infor
    else:
        last_infor['history']['state_medication'] = ''
        if re.search(disagree,message):
            res['medication_vaccine_replynot'] = last_infor
        else:
            res['medication_vaccine_replyok']=last_infor
    return res

def thuoc_chonguoi_bicovid(message, last_infor):
    res={}
    res_code=''
    if last_infor['symptom']['ho']!=0 or last_infor['symptom']['dau-hong']!=0 :
        res_code=res_code+'medication_maccovid_ho'
    if last_infor['symptom']['tieu-chay']!=0:
        res_code=res_code+'-'+'medication_maccovid_tieuchay'
    if last_infor['symptom']['dau-nhuc'] != 0 or last_infor['symptom']['met-moi']!=0 or last_infor['symptom']['sot']!=0  :
        res_code=res_code+'-'+'medication_maccovid_sotgiamdau'
    if  re.search(daubung,message):
        res_code = res_code + '-' + 'medication_maccovid_daubung'
    if last_infor['symptom']['mat-vi-giac']!= 0 or last_infor['symptom']['tim-tai']!= 0 or last_infor['symptom']['noi-man']!= 0 or last_infor['symptom']['kho-tho']!= 0 or last_infor['symptom']['tuc-nguc']!= 0:
        res_code='medication_maccovid_nghiemtrong'
    for intensity_sym in symptom_list:
        for sym in symptom_list[intensity_sym]:
            symp = symptom_list[intensity_sym][sym]
            last_infor['symptom'][symp] = ''
    res[res_code]=last_infor
    return res
def thuoc_chonguoi_khongbicovid(message, last_infor):
    res={}
    res_code=''
    if last_infor['symptom']['ho']!=0 or last_infor['symptom']['dau-hong']!=0 :
        res_code=res_code+'medication_khongmaccovid_ho'
    if last_infor['symptom']['tieu-chay']!=0:
        res_code=res_code+'-'+'medication_khongmaccovid_daubung'
    if last_infor['symptom']['dau-nhuc'] != 0 or last_infor['symptom']['met-moi']!=0 or last_infor['symptom']['sot']!=0  :
        res_code=res_code+'-'+'medication_khongmaccovid_sot'
    if  re.search(daubung,message):
        res_code = res_code + '-' + 'medication_khongmaccovid_daubung'
    if  last_infor['symptom']['kho-tho']!= 0 or last_infor['symptom']['tuc-nguc']!= 0:
        res_code=res_code + '-' + 'medication_khongmaccovid_khotho'
    if last_infor['symptom']['mat-vi-giac'] != 0 or last_infor['symptom']['tim-tai'] != 0 or last_infor['symptom']['noi-man'] != 0:
        res_code = 'medication_khongmaccovid_conlai'

    for intensity_sym in symptom_list:
        for sym in symptom_list[intensity_sym]:
            symp = symptom_list[intensity_sym][sym]
            last_infor['symptom'][symp] =''
    res[res_code]=last_infor
    return res

def cotrieuchung(message, last_infor):
    res = {}
    if last_infor['history']['state_medication'] == '':
        for intensity_sym in symptom_list:
            for sym in symptom_list[intensity_sym]:
                if re.search(sym, message):
                    assign = 1
                else:
                    assign = 0
                symp = symptom_list[intensity_sym][sym]
                if last_infor['symptom'][symp] == '':
                    last_infor['symptom'][symp] = assign
        last_infor['history']['state_medication']='maccovid'
        res['medication_maccovid_check']=last_infor
        return res
    else:
        last_infor['history']['state_medication'] = ''
        if re.search(disagree, message):
            return thuoc_chonguoi_khongbicovid(message, last_infor)
        else:
            return thuoc_chonguoi_bicovid(message, last_infor)
def medication_rep(message, last_infor, last_intent):
    print('\t\t------------------THÔNG TIN THUỐC-------------------')
    check = ''
    message = message
    res = {}
    for ele in medication_reg:
        if re.search(medication_reg[ele], message):
            check = ele
            break

    if not last_infor['history']['state_medication']:
        for intensity_sym in symptom_list:
            for sym in symptom_list[intensity_sym]:
                if re.search(sym, message):
                    symp = symptom_list[intensity_sym][sym]
                    if last_infor['symptom'][symp] == '' :
                        check='co_trieuchung'
        if re.search(r'v[a|á|â|ạ|ã|ả|â|ấ][c|t|g]|ti(e|ê)m',message):
            return saukhithiem_vaccine(message, last_infor)
        if re.search(r'th(a|aa|â)i',message):
            res['medication_cothai']=last_infor
            return res
        if check=='co_trieuchung':
            return cotrieuchung(message, last_infor)
        if check=='damac_covid_chuaco_trieuchung':
            last_infor['history']['state_medication'] = 'damac_covid_chuaco_trieuchung'
            res['request_age'] = last_infor
            return res
        if check == 'binhoxy':
            res['medication_huongdansudungbinhoxy'] = last_infor
            return res
        if check=='buy_medicine':
            return buy_medicine(message, last_infor, last_intent)
        if check=='spo':
            return spo_oxy(message, last_infor)
        if check=='5k':
            res['medication_spo_5k']=last_infor
            return res
        if check == 'device':
            return device(message, last_infor)
    else:
        if 'buymedicine' in last_intent:
            return buy_medicine(message, last_infor, last_intent)
        if 'prop' in last_intent:
            last_infor['history']['state_medication'] = ''
            return thuoc_chonguoi_bicovid(message, last_infor)
        if 'vaccine_check' in last_intent:
            return saukhithiem_vaccine(message, last_infor)
        if 'maccovid_check' in last_intent:
            return cotrieuchung(message, last_infor)

    res['other'] = last_infor
    return res