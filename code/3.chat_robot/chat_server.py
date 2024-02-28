import sanic
import httpx
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from sanic.exceptions import NotFound
from sanic.response import html
from jinja2 import Environment, PackageLoader

import os, sys
import json
import urllib.request


env = Environment(loader=PackageLoader('app', 'templates'))

app = Sanic(__name__)


@app.route('/')
async def index(request):
    """
    聊天页面
    """
    template = env.get_template('index.html')
    html_content = template.render(title='聊天机器人')
    return html(html_content)


@app.websocket('/chat')
async def chat(request, ws):
    """
    处理聊天信息，并返回消息
    :param request:
    :param ws:
    :return:
    """
    url = 'http://127.0.0.1:9010/QA'
    

    while True:
        user_msg = await ws.recv()
        print('Received: ' + user_msg)
        app_data = {"request_id": "zhuo", "query": user_msg, "type": "Text"}
        """ 转化为json格式 """
        app_data = json.dumps(app_data).encode("utf-8")
        req = urllib.request.Request(url, app_data)
        try:
            """ 调用服务，得到结果 """
            response = urllib.request.urlopen(req)
            response = response.read().decode("utf-8")

            """ 从json格式中解析出来 """
            response = json.loads(response)
            response = response["answer"]
        except Exception as e:
            print(e)
            response = "亲，暂时还理解不了您的问题，对我耐心点哦~"

        #intelligence_data = {"key": "free", "appid": 0, "msg": user_msg}
        #r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        #chat_msg = r.json()["content"]
        print('Sending: ' + response)
        await ws.send(response)


if __name__ == "__main__":
    app.error_handler.add(
        NotFound,
        lambda r, e: sanic.response.empty(status=404)
    )
    app.run(host="127.0.0.1", port=8000, protocol=WebSocketProtocol, debug=True)

