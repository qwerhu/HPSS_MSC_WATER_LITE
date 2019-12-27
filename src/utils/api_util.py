from tornado.ioloop import IOLoop


async def call_blocking(blocking_func, *args):
    """
    将堵塞的函数转换成异步的函数
    :param blocking_func:
    :param args:
    :return:
    """
    return await IOLoop.current().run_in_executor(None, blocking_func, *args)
