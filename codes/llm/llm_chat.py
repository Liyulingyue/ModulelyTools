import erniebot
import json
import datetime
# 一个自定义文件用来存放token，请自行到自己账号主页复制自己的token替换erniebot
from .tokens import erniebot_access_token

def get_llm_answer_with_msg(msg):
    erniebot.api_type = 'aistudio'
    erniebot.access_token = erniebot_access_token
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=msg,
        top_p=0,
        temperature = 0.1,
    )
    result = response.get_result()
    return result

def get_llm_answer(prompt):
    erniebot.api_type = 'aistudio'
    erniebot.access_token = erniebot_access_token
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': prompt}],
        top_p=0,
        temperature = 0.1,
    )
    result = response.get_result()
    return result

def extract_json_from_llm_answer(result):
    s_id = result.index('```json')
    e_id = result.index('```', s_id+7)
    json_str = result[s_id+7:e_id]
    json_str = json_str.replace("\n","")
    json_dict = json.loads(json_str)
    return json_dict

def get_llm_json_answer(prompt):
    result = get_llm_answer(prompt)
    json_dict = extract_json_from_llm_answer(result)
    return json_dict