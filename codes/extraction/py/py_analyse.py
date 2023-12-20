import ast
from llm_chat import *


def extract_function_defs(node, function_defs):
    if isinstance(node, ast.FunctionDef):
        function_source = ast.unparse(node)
        function_defs.append([node.name, function_source, [arg.arg for arg in node.args.args], ast.get_docstring(node)])
    elif isinstance(node, ast.ClassDef):
        function_source = ast.unparse(node)
        function_defs.append([node.name, function_source, [stmt.name for stmt in node.body if isinstance(stmt, ast.FunctionDef)], ast.get_docstring(node)])
    else:
        for child in ast.iter_child_nodes(node):
            extract_function_defs(child, function_defs)


def get_function_defs(code):
    tree = ast.parse(code)
    function_defs = []
    extract_function_defs(tree, function_defs)
    return function_defs  # a list, each element is [define of function/class, docstring]


def get_intro_of_fun(fun_str):
    try:
        prompt = f"""
        请帮我为这个函数或者类写一段说明介绍，并且以json的形式返回给我。
        需要解读的函数或者类是{fun_str}
        Json返回的内容格式为：
        {str('{')}"
        "说明介绍":str
        {str('}')}
        """
        result = get_llm_answer(prompt)
        try:
            json_dict = extract_json_from_llm_answer(result)
            return json_dict["说明介绍"]
        except:
            return result
    except:
        return "输出失败"

