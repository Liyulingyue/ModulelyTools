# ModulelyTools
一个基于LLM的函数模块化&amp;说明文档生成小工具，开发中~

## 环境部署
#### python版本
```
python >= 3.7
```
#### 安装依赖
```
pip install -r requirements.txt
```
#### 配置LLM相关参数(token)
```
# 1.复制example.env并命名为.env文件到项目根目录
$ cp example.env .env

# 2.修改.env文件中的token
```

## 关于这个工具
这是一个基于LLM的函数模块化小工具，设计功能是
1. 给定一个.pynb文档，一键生成.py文件，.py文件具有较好的封装性。
2. 给定一个.py文件，一键生成对应的.md文件，.md文件时函数的使用说明书。

## 当前进展
当前这个工具简单地走通了链路
1. 可以抽取ipynb的信息，并将ipynb的信息抽象为对应的函数/类定义。
2. 可以抽取py信息，并将py的函数/类定义抽取出来，送入LLM生成对应函数说明。

## 工作问题
当前这个工作具有很多问题：
1. 根据ipynb信息进行架构设计的思路仍不完善，例如
   - 提示词仍需优化
   - 思维链路需要优化
   - ipynb可能太长，超出LLM承受的Token长度，但是分块输入导致LLM缺失信息从而无法给出准确的架构设计
   - 使用ipynb和架构设计结果进行函数设计的prompt和思维链路需要优化（难点同上）
2. 根据py模块进行说明文档的生成需要优化

## 启发
本项目在[飞桨 x 文心大模型 x Founder Park AGI Hackathon 大模型黑客松](https://aistudio.baidu.com/competition/detail/1103/0/introduction)由 即应&一根腿毛 提出，用于参加盲盒赛道。在比赛结束后，我们希望继续维护这个项目，解决在比赛中仓促开发时为解决的问题，并且让这个仓库成为一个真正实用的工具~
