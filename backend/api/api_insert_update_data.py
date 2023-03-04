from backend.config.config import Config


def insert_update_knn(data):
    for idx in range(len(data['question'])):
        if data['question'][idx] == 'None' or data['answer'][idx] =='None':
            continue
        Config.mycol_response_knn.update({'question': data['question'][idx]}, {'$set': {'answer': data['answer'][idx]}}, upsert= True)
    return 'done'

def insert_update_svm(data):    
    for idx in range(len(data['text'])):
        if 'None' in [data['text'][idx],data['intent'][idx]]:
            continue
        if data['intent'][idx].lower()=='request' and data['sub_intent'][idx]=='None':
            continue
        elif data['intent'][idx].lower()!='request':
            data['sub_intent'][idx]=='None'
        Config.intent_db.update({'text': data['text'][idx]}, 
                     {'$set': {'intent': data['intent'][idx], "sub_intent": data['sub_intent'][idx]}}, upsert= True)
        
    return 'done'

def insert_data(data):
    ls_param = ['text', 'intent', 'sub_intent', 'response']
    for ele in ls_param:
        if ele not in data.keys() or len(data[ele])==0:
            # THROW ERROR because of not enough param
            return {'suggest_reply': 'ERROR NOT ENOUGH PARAM', 'id_job': '', 'check_end': True}
    
    insert_update_svm(data)
    print('Update svm done!')
    data_knn = {
        'question': [],
        'answer': []
    }
    for idx,ele in enumerate(data['text']):
        if (not data['intent'][idx] or data['intent'][idx].lower() != 'request') and \
            data['response'].lower()=='none' and data['sub_intent'].lower() != 'diagnostic':
            continue
        
        data_knn['question'].append(data['text'][idx])
        data_knn['answer'].append(data['response'][idx])
    insert_update_knn(data_knn)
    print('Update knn done!')
    return 'Done'

