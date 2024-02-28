# coding=utf8
import os, sys
import json
import urllib.request


def chat_service(content, send_name, type_, port):
    """ 1: 服务的ip和端口号 """
    # url = 'http://0.0.0.0:{}/QA'.format(port)  # 要把模型部署到服务器上 'http://0.0.0.0:8000/QA'
    url = 'http://127.0.0.1:{}/QA'.format(port)
    app_data = {"request_id": send_name, "query": content, "type": type_}

    """ 转化为json格式 """
    app_data = json.dumps(app_data).encode("utf-8")

    req = urllib.request.Request(url, app_data)
    try:
        """ 调用服务，得到结果 """
        response = urllib.request.urlopen(req)
        response = response.read().decode("utf-8")

        """ 从json格式中解析出来 """
        response = json.loads(response)
    except Exception as e:
        print(e)
        response = "亲，暂时还理解不了您的问题，对我耐心点哦~"
    if type(response) is not str:
        return response["answer"]
    else:
        return response


if __name__ == '__main__':
    content = "请列举stm32的四个驱动单元"
    print("Question: {} ".format( str(content) ) )
    answer = chat_service(content, 'zhuo', "Text", 9010)
    print("Answer  : {} ".format(str(answer)))

    content = "抢占优先级和子优先级可以配置成哪些优先级顺序"
    print("Question: {} ".format( str(content) ) )
    answer = chat_service(content, 'zhuo', "Text", 9010)
    print("Answer  : {} ".format(str(answer)))

    content = "中断控制器NVIC的配置流程是什么"
    print("Question: {} ".format( str(content) ) )
    answer = chat_service(content, 'zhuo', "Text", 9010)
    print("Answer  : {} ".format(str(answer)))


    content = "EXTI3的五种输入源是什么"
    print("Question: {} ".format( str(content) ) )
    answer = chat_service(content, 'zhuo', "Text", 9010)
    print("Answer  : {} ".format(str(answer)))

    content = "仲裁器如何管理DMA请求呢"
    print("Question: {} ".format( str(content) ) )
    answer = chat_service(content, 'zhuo', "Text", 9010)
    print("Answer  : {} ".format(str(answer)))

