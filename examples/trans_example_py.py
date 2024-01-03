from codes.extraction.ModuleTools import ModuleTools
import traceback

mt = ModuleTools(llm_type="Ernie")
py_path = "example.py"
prompt = ""

md_str = mt.py2md(py_path=py_path, prompt=prompt)

print(md_str)