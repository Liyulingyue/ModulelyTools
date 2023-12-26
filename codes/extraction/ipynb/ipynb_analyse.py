import nbformat
from ...llm.llm_chat import *


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
    """
    从已解析的Jupyter Notebook单元格中提取代码单元格的内容。

    参数:
    parsed_cells (list): 包含已解析的Jupyter Notebook单元格的列表。每个单元格应为一个字典，
                         至少包含'属性'和'内容'两个键。'属性'键的值应为"Code"或"Markdown"，
                         '内容'键的值应为单元格的实际内容。

    返回:
    str: 包含所有代码单元格内容的字符串。每个代码单元格的内容前都会加上"[Cell No. {i}]"，
         其中{i}为该代码单元格在输入列表中的索引。
    """

    ipynb_content = ""  # 初始化一个空字符串，用于存储提取出的代码单元格内容

    # 遍历输入列表中的每个单元格
    for i in range(len(parsed_cells)):
        # 如果当前单元格的属性为"Code"，则将其内容添加到结果字符串中
        if parsed_cells[i]['属性'] == "Code":
            ipynb_content += f"[Cell No. {i}]\n {parsed_cells[i]['内容']}\n\n"

    return ipynb_content  # 返回结果字符串


def get_model_list(ipynb_content):
    """
    从给定的ipynb_content中提取模型列表，并以特定的JSON格式返回。

    参数:
    ipynb_content (str): NoteBook中的代码内容。

    返回:
    list[dict]: JSON格式的模型列表，其中每个元素都是一个包含模块信息的字典。
    """

    # 构建提示信息，向LLM（大型语言模型）请求答案
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

    # 通过调用get_llm_json_answer函数，获取LLM返回的JSON格式答案
    json_data = get_llm_json_answer(prompt)

    # 从JSON答案中提取出模块列表，并返回
    return json_data["模块"]


def model_list2python(model_list, ipynb_content):
    """
    将模型列表转化为Python代码字符串。

    参数:
    model_list (list): 包含模型信息的字典列表，每个字典应包含"Name"（模型名称）、"Type"（模型类型）和"Introduction"（模型介绍）等键。
    ipynb_content (str): Notebook中的代码内容，用于提供给大型语言模型（LLM）作为上下文或测试代码。

    返回:
    str: 生成的Python代码字符串，其中包含根据模型列表中的信息实现的模型代码。
    """
    py_str = ""  # 初始化一个空字符串，用于存储生成的Python代码

    for model_dict in model_list:  # 遍历模型列表中的每个模型字典
        model_name = model_dict["Name"]  # 获取模型名称
        model_type = model_dict["Type"]  # 获取模型类型
        model_intro = model_dict["Introduction"]  # 获取模型介绍

        # 构建提示信息，请求LLM根据模型信息和Notebook代码生成模型的实现代码
        prompt = \
            f"""   
我将给你一个模块名称和模块类型，以及一些Notebook中的测试代码，并根据代码内容实现这个模块，使用json格式返回设计结果。  
模块名称是{model_name}，请定义为一个{model_type}，模块的功能是{model_intro}，NoteBook中的代码是{ipynb_content}。  
Json返回的内容格式为：  
{{"代码":multi-lines str}}  
“代码”信息是一个多行字符串，内容是你根据NoteBook中的代码和模块的功能，对模块{model_name}的程序实现，请保证生成的代码可以直接运行，解释说明的内容采用注释标记。  
"""

        try:
            # 通过调用get_llm_answer函数获取LLM的返回值，然后从中提取出生成的模型实现代码
            result_ = get_llm_answer(prompt)  # 调用函数获取LLM的答案（此处函数未在代码中定义，可能是外部API调用或内部其他模块的函数）
            model_impl = extract_json_from_llm_answer(result_)  # 从LLM的答案中提取出生成的模型实现代码（此处函数未在代码中定义，可能是内部其他模块的函数）
            py_str += model_impl["代码"]  # 将提取出的模型实现代码添加到py_str中
        except:
            # 如果在获取或提取LLM答案的过程中出现异常，则在py_str中添加一条错误信息
            py_str += f"# 模块{model_name}，类型是{model_type}，生成失败"

        py_str += "\n\n"  # 在每个模型实现代码之间添加空行，以提高可读性

    return py_str  # 返回生成的Python代码字符串