# chatbot_simbert
检索类型的微信聊天机器人/问答系统，通过API异步通信，实现在微信上交互，可以查询天气、重复问句识别等情况；本项目包括模型和工程化部署一体化。用到SimBert等模型。
## 使用说明
环境准备：安装requirement中的依赖包
下载模型，并放置在code/1.retrieve_match/3.simbert_match/config路径下：
simbert模型：https://github.com/ZhuiyiTechnology/pretrained-models
### 启动：
**1、 启动 code/2.API_serve/KG_service.py
**2、 执行 code/test.py **  
## 实现思路
**后端采用检索匹配模型的方式，结合粗排和精排；
**前后端的交互用sanic实现异步通信。
  模型部分实现的主要流程如下，初始时有个问答库：
**1、先用BM25和Bool检索把问句query和问答库做字词上的粗排，返回topN；
**2、将query和粗排得到的topN用SimBert向量化，再将两者做consine相似度计算得到最相似的top1。
**实现方式：
** 1、在问答库中添加某个意图可能的问法
** 2、通过SimBert精准匹配意图，匹配上则进入该意图的对话管理
**优势： 
1、准确性：如上文所说，常用的意图需要做分类，而分类模型需要有数据支撑才能有比较好的效果； 
2、扩展性：常用的意图分类方式，在新增意图时需要重新训练分类模型；

