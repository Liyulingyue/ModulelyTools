import os

import erniebot
import json

if os.getenv('erniebot_access_token'):
    erniebot.access_token = os.getenv('erniebot_access_token')
else:
    raise Exception("erniebot_access_token未配置：\n"
                    "请移步百度文心一言!https://aistudio.baidu.com/index/accessToken\n"
                    "将token替换到.env的erniebot_access_token中")


def get_llm_answer_with_msg(msg):
    erniebot.api_type = 'aistudio'
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=msg,
        top_p=0,
        temperature=0.1,
    )
    result = response.get_result()
    return result


def get_llm_answer(prompt):
    erniebot.api_type = 'aistudio'
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': prompt}],
        top_p=0,
        temperature=0.1,
    )
    result = response.get_result()
    return result


def extract_json_from_llm_answer(result, start_str="```json", end_str="```", replace_list=["\n"]):
    s_id = result.index(start_str)
    e_id = result.index(end_str, s_id + len(start_str))
    json_str = result[s_id + len(start_str):e_id]
    for replace_str in replace_list:
        json_str = json_str.replace(replace_str, "")
    json_dict = json.loads(json_str)
    return json_dict


def get_llm_json_answer(prompt):
    result = get_llm_answer(prompt)
    json_dict = extract_json_from_llm_answer(result)
    return json_dict
