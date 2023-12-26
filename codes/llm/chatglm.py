# 调用chatglm
from transformers import AutoTokenizer, AutoModel


def chatglm_6b(prompt):
    model_path = "E:\k-agent\chatglm3-6b-model"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().quantize(4).cuda()  # .quantize(4)是量化为int4的意思
    chatglm = model.eval()
    # 调用大模型，生成回答
    response, history = chatglm.chat(tokenizer, prompt, history=[])
    return response
