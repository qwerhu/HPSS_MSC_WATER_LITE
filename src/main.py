"""
主入口
"""
import time
import boss
# from src import boss
import workers
# from src import workers
from workers import hpss_webapi
from multiprocessing import freeze_support
from workers import hpss_proxy_clock, hpss_proxy_robot
# import ctx
from src import  ctx


def main():
    # 启动守护线程
    boss.main()
    # 定时任务
    # add_clock('hpss_online', workers.WORKER_MODE_PROCESS, 'hpss_online_model',
    #           'workers.hpss_online_model', 10)
    # add_robot('hpss_report', workers.WORKER_MODE_PROCESS, 'hpss_report',
    #           'workers.hpss_report', ctx.MSG_REPORT)
    # 开启api进程
    boss.spawn(workers.WORKER_MODE_PROCESS, hpss_webapi.main, 'hpss_webapi')

    # boss.spawn(workers.WORKER_MODE_PROCESS, hpss_webapi.two(), 'hpss_webapi2')
    # boss.spawn(workers.WORKER_MODE_PROCESS, hpss_webapi.three(), 'hpss_webapi3')
    # boss.spawn(workers.WORKER_MODE_PROCESS, hpss_webapi.four(), 'hpss_webapi4')


def _main():
    freeze_support()#在Windows下编译需要加这行
    main()
    while True:
        time.sleep(1048576)


def add_robot(_id, mode, name, module, _in=None, _out=None, args={}):
    conf = {}
    conf['module'] = module
    conf['id'] = _id
    conf['in'] = _in
    conf['out'] = _out
    for k, v in args:
        conf[k] = v
    boss.spawn(mode, hpss_proxy_robot.main, name, kwArgs={'config': conf})


def add_clock(_id, mode, name, module, interval=None, args={}):
    conf = {}
    conf['module'] = module
    conf['id'] = _id
    conf['check_interval'] = interval if interval is not None else hpss_proxy_clock.DEFAULT_CHECK_INTERVAL
    for k, v in args:
        conf[k] = v
    boss.spawn(mode, hpss_proxy_clock.main, name, kwArgs={'config': conf})


if __name__ == '__main__':
    _main()
