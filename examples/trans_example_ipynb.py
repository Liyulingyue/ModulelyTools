from codes.extraction.ModuleTools import ModuleTools
import traceback

mt = ModuleTools(llm_type="Ernie")
ipynb_path = "example.ipynb"
prompt = ""

py_str = mt.ipynb2py(ipynb_path=ipynb_path, prompt=prompt)

print(py_str)