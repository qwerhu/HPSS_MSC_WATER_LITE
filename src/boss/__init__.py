# coding=utf-8
import logging
import time
import workers as worker

workers = []


def spawn(mode=worker.WORKER_MODE_PROCESS, target=None, name=None, args=(), kwArgs={}, protect=True, sys=True, auto=True, cid=None):
    if target is None:
        raise Exception('target is None')
    if mode == worker.WORKER_MODE_PROCESS:
        m = worker.ProcessWorker(target, name, args, kwArgs, protect, sys, cid)
        workers.append(m)
    elif mode == worker.WORKER_MODE_THRED:
        m = worker.ThreadWorker(target, name, args, kwArgs, protect, sys, cid)
        workers.append(m)
    else:
        raise Exception('unkown mode "%s"' % mode)

    if auto:
        m.start()


def killall_process():
    """结束所有进行进程"""
    for w in workers:
        if isinstance(w, worker.ProcessWorker):
            w.terminate()


def protect():
    while True:
        for w in workers:
            if w.protect and w.state == worker.PROCESS_STATE_RUNNING and not w.is_alive():
                logging.error('worker dead ... %s(%s)' % (w.name, w.id))
                w.start()
                logging.error('worker restarted ... %s(%s)' % (w.name, w.id))
            elif w.state == worker.PROCESS_STATE_ABORT:
                w.state = worker.PROCESS_STATE_HALT
                logging.error('worker aborted ... %s(%s)' % (w.name, w.id))
        time.sleep(5.0)


def main():
    """启动守护线程"""
    spawn(worker.WORKER_MODE_THRED, protect, 'watchdog')
