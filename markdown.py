def get_header():
    markdown_str = """
    # Modulely Tools
    **Modulely Tools** 是一个模块化集成器，当你在进行代码开发时，你可能会在notebook的不同cell中验证不同的功能，例如
    ```
    In cell1: 
        import xxx
        k = xxx.app()
        # some outputs
        
    In cell2:
        import ast
        ast(k)
        # some outputs
        
    In cell3:
        ...
    ```
    当你验证完毕所有功能时，为了方便下次调用，你需要将他们封装在一起，并写一个使用说明书/函数说明书。
    不幸的，大部分程序员开发完毕流程后，已经没有更多地精力/兴趣/动力将碎片代码集成成一个优雅的整体，更不要说给出一个使用说明书了。
    更加不幸的是，我们能从大量的Github项目中直观地感受到这一点，以至于我们使用api的时候无从下手。
    
    但是现在！你可以使用我们的工具，一键整合你凌乱且优雅的代码，并且封装成为一个带有说明文档的模块！
    """
    return markdown_str