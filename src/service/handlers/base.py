import json
import traceback
from tornado.web import RequestHandler
import ctx


class BaseHandler(RequestHandler):
    """
    解决跨域访问问题
    """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def return_success(self, msg=None):
        """返回成功的消息"""
        if msg is None:
            msg = '操作成功'
        res = {'success': True, 'msg': msg}
        res = json.dumps(res)
        self.write(res)

    def return_failed(self, msg=None):
        """返回成功的消息"""
        if msg is None:
            msg = '操作失败'
        res = {'success': False, 'msg': msg}
        res = json.dumps(res)
        self.write(res)

    def options(self):
        self.set_status(200)
        self.finish()

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            excp = kwargs['exc_info'][1]
            tb = kwargs['exc_info'][2]
            stack = traceback.extract_tb(tb)
            clean_stack = [i for i in stack if i[0][-6:] != 'gen.py' and i[0][-13:] != 'concurrent.py']
            error_msg = '{}\n  Exception: {}'.format(''.join(traceback.format_list(clean_stack)), excp)
            ctx.logger.log_status(error_msg, 4)