import os
import time
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from utils.date_util import get_dirname


class HpLog(object):
    """
    @param:
    1. name => log.write_name
    2. username => log.username 
    3. path => log.write_path
    4. fmt => log.user-info-format
    5. datefmt => timestamp
    6. logging level => default is Logging.INFO
    
    @method:
    log_status => msg = "logging message"
                  method_level = "message level"
    """
    name = "hp {}.log".format(time.strftime("%Y-%m-%d %H-%M-%S")[2:])
    username = "HPSS"
    parpath = get_dirname(__file__, 3)
    # parpath = os.path.expanduser('~')
    path = os.path.join(parpath, "logs")
    keep_time = 3600 * 24 * 30  # 保留30天的日志文件

    def __init__(self,
                 name=None,
                 username=None,
                 path=None,
                 fmt="%(asctime)-15s %(name)s %(levelname)s: %(message)s",
                 datafmt="%Y-%m-%d %H:%M:%S",
                 level=logging.INFO,
                 ):

        self.name = self.__get_log_name(name)
        self.username = self.__get_log_username(username)
        self.path = self.__get_log_path(path)
        self.level = self.__get_log_level(level)

        fmt = self.__get_log_fmt(fmt)
        datefmt = self.__get_log_datafmt(datafmt)

        self.fmtter = self.__get_log_formatter(fmt, datefmt)
        self.handler = self.__get_log_handler()
        self.logger = self.__get_logger()

    def __get_log_name(self, name):

        if name is None:
            name = HpLog.name
        # else:
        #     name

        return name

    def __get_log_username(self, name):

        if name is None:
            name = HpLog.username

        return name

    def __get_log_path(self, path=None):

        if path is None:
            path = HpLog.path

        # set path if(!exist)
        if not os.path.exists(path):
            os.mkdir(path)
            os.chdir(path)
        # or clear futile logs
        else:
            os.chdir(path)
            logs = os.listdir(path)
            for log_ in logs:
                ctime = os.path.getctime(log_)
                if time.time() - ctime >= self.keep_time:
                    try:
                        os.remove(log_)
                    except PermissionError:
                        pass

        return path

    def __get_log_level(self, level):

        assert level in (logging.INFO, logging.WARN, logging.DEBUG, logging.ERROR, logging.CRITICAL), \
            "Level should be within [logging.INFO, logging.WARN, logging.DEBUG, logging.ERROR, logging.CRITICAL]"

        return level

    def __get_log_fmt(self, fmt):

        if fmt is None:
            fmt = "%(asctime)-15s %(name)s : %(message)s"
        return fmt

    def __get_log_datafmt(self, datefmt):

        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"
        return datefmt

    def __get_log_formatter(self, fmt=None, datefmt=None):

        fmt = self.__get_log_fmt(fmt)
        datefmt = self.__get_log_datafmt(datefmt)
        fmtter = logging.Formatter(fmt, datefmt)

        return fmtter

    def __get_log_handler(self):

        log_path = self.path + os.sep + self.name
        # fh = logging.FileHandler(log_path, mode='w')
        fh = ConcurrentRotatingFileHandler(log_path, maxBytes=1024 * 1024 * 10, backupCount=50)
        fh.setLevel(self.level)
        fh.setFormatter(self.fmtter)

        return fh

    def __get_logger(self):

        name = self.username
        logger = logging.getLogger(name)
        logger.addHandler(self.handler)
        logger.setLevel(self.level)
        logger.propagate = False

        return logger

    def log_status(self, msg, method_level=2):
        """
        @note: for user to log
        """
        method_dict = {1: "debug",
                       2: "info",
                       3: "warning",
                       4: "error",
                       5: "critical"}

        getattr(self.logger, method_dict[method_level])(msg)


if __name__ == "__main__":
    # test
    logger = HpLog()

    logger.log_status("Very good!")
    logger.log_status("Very good!", 1)
    logger.log_status("Very good!", 3)
    logger.log_status("Very good!", 4)
    logger.log_status("Very good!", 5)
