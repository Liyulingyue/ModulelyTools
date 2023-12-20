import nbformat
from llm_chat import *


def parse_ipynb(file_path):
    """
    # 示例：使用函数解析一个ipynb文件
    file_path = 'main.ipynb'  # 请将此处替换为您的ipynb文件路径
    result = parse_ipynb(file_path)
    print(result)
    """
    # 读取ipynb文件
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

        # 初始化结果列表
    parsed_cells = []

    # 对每一个cell进行处理
    for cell in nb.cells:
        cell_dict = {}
        if cell.cell_type == 'markdown':
            cell_dict['属性'] = 'Markdown'
            cell_dict['内容'] = cell.source
            cell_dict['输出'] = ''
        elif cell.cell_type == 'code':
            cell_dict['属性'] = 'Code'
            cell_dict['内容'] = cell.source
            cell_dict['输出'] = ''
        else:
            raise ValueError(f"Unsupported cell type: {cell.cell_type}")
        parsed_cells.append(cell_dict)
    return parsed_cells


def get_ipynb_content(parsed_cells):
    ipynb_content = ""

    for i in range(len(parsed_cells)):
        if parsed_cells[i]['属性'] == "Code":
            ipynb_content += f"[Cell No. {i}]\n {parsed_cells[i]['内容']}\n\n"

    return ipynb_content


def get_model_list(ipynb_content):
    prompt = \
f""" 
我将给你一些NoteBook中的测试代码，请你阅读这些代码，并根据代码内容进行架构设计，使用json格式返回设计结果。
NoteBook中的代码是{ipynb_content}
Json返回的内容格式为：
{str('{')}
"模块":list[dict{str('{')}"Name":str, "Type":str, "Introduction":str{str('}')}]
{str('}')}
“模块”信息是一个list，每个元素是一个字典，包括了模块名称，模块类型(取值为"class"或"function")，模块介绍
"""
    json_data = get_llm_json_answer(prompt)
    return json_data["模块"]


def model_list2python(model_list, ipynb_content):
    py_str = ""
    for model_dict in model_list:
        model_name = model_dict["Name"]
        model_type = model_dict["Type"]
        model_intro = model_dict["Introduction"]

        prompt = \
f""" 
我将给你一个模块名称和模块类型，以及一些Notebook中的测试代码，并根据代码内容实现这个模块，使用json格式返回设计结果。
模块名称是{model_name}，请定义为一个{model_type}，模块的功能是{model_intro}，NoteBook中的代码是{ipynb_content}。
Json返回的内容格式为：
{str('{')}
"代码":multi-lines str
{str('}')}
“代码”信息是一个多行字符串，内容是你根据NoteBook中的代码和模块的功能，对模块{model_name}的程序实现，请保证生成的代码可以直接运行，解释说明的内容采用注释标记。
"""

        # model_impl = get_llm_json_answer(prompt)
        try:
            result_ = get_llm_answer(prompt)
            model_impl = extract_json_from_llm_answer(result_)
            py_str += model_impl["代码"]
        except:
            py_str += f"# 模块{model_name}，类型是{model_type}，生成失败"
        py_str += "\n\n"
    return py_str