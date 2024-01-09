#  调用百川2-192k大模型

import requests
import json

from .tokens import api_key


class Baichuan:
    def __init__(self):
        self.api_key = api_key
        self.model_type = "Baichuan2-Turbo-192k"    # 这里可以选择百川的其它模型

    def get_llm_answer_with_msg(self, msg):
        url = "https://api.baichuan-ai.com/v1/chat/completions"

        data = {
            "model": self.model_type,
            "messages": msg,
            "temperature": 0.1,
            "top_p": 0.85,
            "max_tokens": 196608,
            "with_search_enhance": False,
            "stream": False
        }

        json_data = json.dumps(data)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        response = requests.post(url, data=json_data, headers=headers, timeout=60)

        if response.status_code == 200:
            print("请求成功！")
            # print("响应body:", response.text)
            print("百川2-192K：", response.json()['choices'][0]['message']['content'])
            # print("请求成功，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
            return response.json()['choices'][0]['message']['content']
        else:
            print("请求失败，状态码:", response.status_code)
            print("请求失败，body:", response.text)
            print("请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
            return None

    def get_llm_answer(self, prompt):
        url = "https://api.baichuan-ai.com/v1/chat/completions"

        data = {
            "model": self.model_type,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "top_p": 0.85,
            "max_tokens": 196608,
            "with_search_enhance": False,
            "stream": False
        }

        json_data = json.dumps(data)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        response = requests.post(url, data=json_data, headers=headers, timeout=60)

        if response.status_code == 200:
            print("请求成功！")
            # print("响应body:", response.text)
            print("百川2-192K：", response.json()['choices'][0]['message']['content'])
            # print("请求成功，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
            return response.json()['choices'][0]['message']['content']
        else:
            print("请求失败，状态码:", response.status_code)
            print("请求失败，body:", response.text)
            print("请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
            return None

    def extract_json_from_llm_answer(self, result, start_str="```json", end_str="```", replace_list=["\n"]):
        s_id = result.index(start_str)
        e_id = result.index(end_str, s_id + len(start_str))
        json_str = result[s_id + len(start_str):e_id]
        for replace_str in replace_list:
            json_str = json_str.replace(replace_str, "")
        json_dict = json.loads(json_str)
        return json_dict

    def get_llm_json_answer(self, prompt):
        result = self.get_llm_answer(prompt)
        json_dict = self.extract_json_from_llm_answer(result)
        return json_dict

if __name__ == "__main__":
    Baichuan().get_llm_answer(prompt="你是谁？")
