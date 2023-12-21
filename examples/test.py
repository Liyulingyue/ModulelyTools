import codes.extraction.py as py

def hello_test():
    print("hello")

with open("test.py", encoding="utf8") as f:
    py_str = f.read()
function_defs = py.py_analyse.get_function_defs(py_str)
print(function_defs)