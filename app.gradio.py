import os
os.system("pip install erniebot")
os.system("pip install nbformat")
os.system("pip install nbconvert")


import gradio as gr
from markdown import *
from gradio_fn import *


with gr.Blocks() as demo:
    gr.Markdown(get_header())
    with gr.Tab("Notebook 转 Modules"):
        gr.Markdown("在本页面中，你可以上传一个.ipynb模块，将它转化为.py文件，并获得对应的使用说明书")
        with gr.Row():
            file_ipynb = gr.File(label="请上传.ipynb文件", file_count="single", file_types=[".ipynb"],scale=1)
            prompt_ipynb = gr.Text(label=".ipynb文件描述", info="请输出你写这段代码的目标，例如“我写这段代码是为了{你的功能}，我希望将封装后保留一些函数接口可以实现{目标效果}”", scale=3)
        with gr.Row():
            with gr.Column():
                file_py = gr.File(label="py文件", file_count="single")
                text_py = gr.Text(label="py文件预览", lines=2, max_lines=20)
                debug_py = gr.Text(label="py文件错误信息")
            with gr.Column():
                file_md = gr.File(label="md文件", file_count="single", interactive=False)
                text_md = gr.Text(label="md文件预览", lines=2, max_lines=20)
                markdown_md = gr.Markdown(label="md文档预览",visible=False)
        with gr.Row():
            btn_ipynb2py = gr.Button("转换Notebook到Python")
            btn_py2file = gr.Button("更新Python文件")
            btn_py2markdown = gr.Button("转换Python到MarkDown")
            btn_markdown2file = gr.Button("更新Markdown文件")
            btn_ipynb2markdown = gr.Button("一键转换")
            cb_showmd = gr.Checkbox(label="MD文档编辑", value=True)

        btn_ipynb2py.click(fn=fn_ipynb2py, inputs=[file_ipynb, prompt_ipynb], outputs=[file_py, text_py])
        btn_py2file.click(fn=fn_py2file, inputs=[text_py], outputs=[file_py])
        btn_py2markdown.click(fn=fn_py2markdown, inputs=[file_py], outputs=[file_md, text_md, markdown_md, debug_py])
        btn_markdown2file.click(fn=fn_markdown2file2, inputs=[text_md], outputs=[file_md, markdown_md])
        btn_ipynb2markdown.click(fn=fn_ipynb2markdown, inputs=[file_ipynb, prompt_ipynb], outputs=[file_py, text_py, file_md, text_md, markdown_md])
        cb_showmd.change(fn=fn_changemd, inputs=[cb_showmd], outputs=[text_md, markdown_md])
        file_py.change(fn_updatepy, inputs=[file_py], outputs=[text_py])

demo.launch()