from .ipynb.ipynb_analyse import parse_ipynb, get_ipynb_content, get_model_list, model_list2python
from .py.py_analyse import extract_function_defs, get_function_defs, get_intro_of_fun

class ModuleTools(object):
    def __init__(self, llm_type="Ernie"):
        super.__init__()
        if llm_type=="Ernie":
            from ..llm.Ernie import Ernie
            self.llm = Ernie()
        else: # default set ernie as used llm
            from ..llm.Ernie import Ernie
            self.llm = Ernie()

    def ipynb2py(self, ipynb_path = "example.ipynb", prompt = ""):
        result = parse_ipynb(ipynb_path)
        ipynb_content = get_ipynb_content(result)
        model_list = get_model_list(ipynb_content, self.llm)
        py_str = model_list2python(model_list, ipynb_content, self.llm)
        return py_str

    def py2md(self, py_path = "example.py", prompt = ""):
        with open(py_path, encoding="utf8") as f:
            py_str = f.read()
        md_str = "# 函数使用说明文档"

        function_defs = get_function_defs(py_str)
        for function in function_defs:
            name = function[0]
            declare = function[0] + '(' + ', '.join(function[2]) + ')'
            try:
                intro = get_intro_of_fun(function[1], self.llm)
            except:
                intro = "生成失败"
            tmp_str = f"""
## {name}

|名称|内容|
|---|---|
|函数名称|{name}|
|函数声明|{declare}|
|函数说明|{intro}|

            """
            md_str += tmp_str
        return md_str