from backend.config.regrex import symptom_list
import regex as re

def update_symptom(symptom, check_has, last_infor):
    
    for sym in symptom_list[symptom].values():
        last_infor['symptom'][sym] = 1 if check_has else 0