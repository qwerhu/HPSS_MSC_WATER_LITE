import ctx
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from service.urls import WsApplication
import asyncio

LST_PORT = ctx.api_port if ctx.api_port else 25098


def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    """ 启动一个服务 """
    ws_app = WsApplication()
    server = HTTPServer(ws_app)
    server.listen(LST_PORT)
    print('后')
    IOLoop.current().start()
    print('下')


def two():
    ws_app = WsApplication()
    server = HTTPServer(ws_app)
    server.start()
    server.listen(30001)
    IOLoop.instance().start()


def three():
    ws_app = WsApplication()
    server = HTTPServer(ws_app)
    server.start()
    server.listen(30002)
    IOLoop.instance().start()


def four():
    ws_app = WsApplication()
    server = HTTPServer(ws_app)
    server.start()
    server.listen(30003)
    IOLoop.instance().start()
