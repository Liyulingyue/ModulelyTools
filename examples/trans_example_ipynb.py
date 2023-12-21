from codes.extraction.ipynb.ipynb_analyse import *
import traceback

ipynb_path = "example.ipynb"
prompt = ""

result = parse_ipynb(ipynb_path)
ipynb_content = get_ipynb_content(result)
model_list = get_model_list(ipynb_content)
py_str = model_list2python(model_list, ipynb_content)
print(py_str)