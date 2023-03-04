from backend.process.chatbot import CovidBot

def send_message(data):
# ---------------- 4.BOT ---------------- #
    print("\t\t+++Start API send-message +++\n\n")

    ls_param = ['sender_id', 'mid', 'text']
    for ele in ls_param:
        if ele not in data or not data[ele]:
            # THROW ERROR because of not enough param
            return {'suggest_reply': 'ERROR NOT ENOUGH PARAM', 'id_job': '', 'check_end': True}

    # Add values to each of params - Dictionary
    input_data = {ele: data[ele] for ele in ls_param}
    data = input_data

    print("\t\t+++++++++++ 3.BOT +++++++++++")
    chatbot = CovidBot()
    result = chatbot.reply(data)
    # ------------------------------------------- #
    
    return result