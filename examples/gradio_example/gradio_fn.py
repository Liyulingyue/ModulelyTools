from codes.extraction.py.py_analyse import *
from codes.extraction.ipynb.ipynb_analyse import *
import traceback
import shutil
import os
import gradio as gr

def fn_ipynb2py(ipynb_path, prompt):
    py_str = get_py_str(ipynb_path, prompt)
    py_path = fn_py2file(py_str)
    return py_path, py_str

def get_py_str(ipynb_path, prompt):
    try:
        if isinstance(ipynb_path, list):
            ipynb_path = ipynb_path[0]
        ipynb_path = os.path.join(os.path.dirname(__file__), ipynb_path.name)
        result = parse_ipynb(ipynb_path)
        ipynb_content = get_ipynb_content(result)
        model_list = get_model_list(ipynb_content)
        py_str = model_list2python(model_list, ipynb_content)
        return py_str
    except:
        return traceback.format_exc()

def fn_py2file(py_str):
    py_path = "converted.py"
    with open(py_path, 'w', encoding="utf8") as f:
        f.write(py_str)
    return py_path

def fn_py2markdown(py_path):
    md_str, debug_py = get_md_str(py_path)
    md_path = fn_markdown2file(md_str)
    return md_path, md_str, gr.update(value=md_str), debug_py

def get_md_str(py_path):
    try:
        if isinstance(py_path, list):
            py_path = py_path[0]
        py_path = os.path.join(os.path.dirname(__file__), py_path.name)
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
            print(tmp_str)
            md_str += tmp_str
        return md_str, ""
    except:
        return "", traceback.format_exc()

def fn_markdown2file(md_str):
    md_path = "converted.md"
    with open(md_path, 'w') as f:
        f.write(md_str)
    return md_path

def fn_markdown2file2(md_str):
    md_path = fn_markdown2file(md_str)
    return md_path, gr.update(value=md_str)

def fn_ipynb2markdown(ipynb_path, prompt):
    py_path, py_str = fn_ipynb2py(ipynb_path, prompt)
    md_path, md_str, _, _ = fn_py2markdown(py_path)
    return py_path, py_str, md_path, md_str, gr.update(value=md_str)

def fn_changemd(cb_showmd):
    t_label = cb_showmd
    m_label = not cb_showmd
    return gr.update(visible=t_label), gr.update(visible=m_label)

def fn_updatepy(py_path):
    try:
        if isinstance(py_path, list):
            py_path = py_path[0]
        py_path = os.path.join(os.path.dirname(__file__), py_path.name)
        with open(py_path, encoding="utf8") as f:
            py_str = f.read()
    except:
        py_str = ""
    return py_str
