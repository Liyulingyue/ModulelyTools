from codes.extraction.py.py_analyse import *
import traceback

py_path = "example.py"
prompt = ""

with open(py_path, encoding="utf8") as f:
    py_str = f.read()
md_str = "# 函数使用说明文档"

function_defs = get_function_defs(py_str)
for function in function_defs:
    name = function[0]
    declare = function[0]+'('+', '.join(function[2])+')'
    try:
        intro = get_intro_of_fun(function[1])
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
print(md_str)