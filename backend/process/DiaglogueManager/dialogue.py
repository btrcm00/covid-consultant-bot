import regex as re

from backend.process.DiaglogueManager.utils_message.symptom_reply import symptom_rep
from backend.process.DiaglogueManager.utils_message.vaccine_reply import vaccine_rep
from backend.process.DiaglogueManager.utils_message.precaution_reply import precaution_rep
from backend.process.DiaglogueManager.utils_message.medication_reply import medication_rep
from backend.process.DiaglogueManager.utils_message.emergency_contact_reply import emergency_contact_rep
from backend.process.DiaglogueManager.utils_message.current_number_reply import current_numbers_rep
from backend.process.DiaglogueManager.utils_message.common_infor_reply import common_infor_rep

from backend.process.PretrainedModel import PretrainedModel
models = PretrainedModel()

def dialogue(last_intent, entity_dict, last_infor, intent):
    new_last_infor = update_slots(entity_dict, last_infor)
    result = predict_reply(last_intent, new_last_infor, intent)
    return result

def update_slots(entity_dict, last_infor):
    return last_infor

def predict_reply(last_intent, last_infor, intent):

    if intent == 'other':
        pass