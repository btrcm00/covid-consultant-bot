from unidecode import unidecode
import regex as re
from backend.config.regrex import *
import regex as re


def timevaccine(message, reply_text, last_infor, last_intent):
    res = {}
    t = ''
    num = 0

    if not last_infor['history']['state_vaccine']:
        for ele2 in message.split():
            for x in vaccine:
                if re.search(x, ele2.lower()):
                    t = 'inform_time_vaccine' + str(num + 1)
                    res[t] = last_infor
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
                    t = 'inform_time_vaccine' + str(num + 1)
                    last_infor['history']['state_vaccine'] = ''
                    res[t] = last_infor
                    return res
                num = num + 1
            num = 0
    res['inform_time_vaccine'] = last_infor
    return res


def womenn(message, intent, last_infor, last_intent):
    res = {}
    last_infor['history']['cothai'] = 'y'
    last_infor['infor']['sex'] = 'nu'
    res['inform_women_vaccine'] = last_infor
    return res


def oldd(message, intent, last_infor, last_intent):
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


def injecc(message, intent, last_infor, last_intent):
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


def condition(message, intent, last_infor, last_intent):
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


def vaccine_rep(message, reply_text, last_infor, intent, last_intent):

    print('\t\t------------------TƯ VẤN VACCINE-------------------')
    check = ''
    res = {}
    for ele in ques:
        for x in ques[ele]:
            if re.search(x, message):
                check = ele
        if check:
            break
    if not last_infor['history']['state_vaccine']:
        if check == 'f1':
            last_infor['history']['f'] = 1
            res['inform_f1_vaccine'] = last_infor
            return res
        elif check == 'f0':
            last_infor['history']['f'] = 0
            res['inform_f0_vaccine'] = last_infor
            return res
        elif check == 'old':
            return oldd(message, intent, last_infor, last_intent)
        elif check == 'women':
            return womenn(message, intent, last_infor, last_intent)
        elif check == 'time':
            return timevaccine(message, intent, last_infor, last_intent)
        elif check == 'injected':
            return injecc(message, intent, last_infor, last_intent)
        elif check == 'condition':
            return condition(message, intent, last_infor, last_intent)
        elif check == 'number':
            res['inform_number_vaccine'] = last_infor
            return res
        elif check == 'register':
            res['inform_common_vaccine'] = last_infor
    else:

        if 'old' in last_infor['history']['state_vaccine']:
            return oldd(message, intent, last_infor, last_intent)
        elif 'time' in last_infor['history']['state_vaccine']:
            return timevaccine(message, intent, last_infor, last_intent)
        elif 'injec' in last_infor['history']['state_vaccine']:
            return injecc(message, intent, last_infor, last_intent)
        elif 'condition' in last_infor['history']['state_vaccine']:
            return condition(message, intent, last_infor, last_intent)
    if not res:
        res['inform_common_vaccine'] = last_infor
    return res