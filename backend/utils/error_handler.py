import sys, datetime
import traceback
from backend.config.config import get_config
config_app = get_config()
def error_handler(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log = time+'\n'+traceback.format_exc()
    error = str(e).replace(r"_", "-")
    error_type = str(exc_type).split("\'")[1] + ': ' + error
    # print(time)
    with open(config_app['log']['app'], 'a') as app_log:
        app_log.write(log)
    return error_type


# def catch_error(chatbot,data)
#     try:
#         result = chatbot.reply(data)
#     except AssertionError as e:
#         print("AssertionError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}
        
#     except BufferError as e:
#         print("BufferError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except EOFError as e:
#         print("EOFError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except ImportError as e:
#         print("ImportError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except MemoryError as e:
#         print("MemoryError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except NameError as e:
#         print("NameError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except OSError as e:
#         print("OSError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except RuntimeError as e:
#         print("RuntimeError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except SyntaxError as e:
#         print("SyntaxError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except SystemError as e:
#         print("SystemError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except TypeError as e:
#         print("TypeError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except ValueError as e:
#         print("ValueError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except ReferenceError as e:
#         print("ReferenceError")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}

#     except Exception as e:
#         print("Exception")
#         error_type = error_handler(e)
#         return {'suggest_reply': "Hệ thống đang gặp lỗi ({error_type}).\nThông tin sẽ được chuyển cho Admin, quý khách vui lòng đợi trong giây lát"\
#             .format(error_type=error_type), 'confident': 1, 'id_job': 1, 'check_end': False, 'rep_intent': ['BIG ERROR']}