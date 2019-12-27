# coding=utf-8
import cx_Oracle
import logging
# import encrypt
from . import encrypt
from DBUtils.PooledDB import PooledDB
import ctx


class Oracle(object):
    __pool = {}

    def __init__(self):
        pass

    @staticmethod
    def getDB(host, port, username, password, database):
        key = '%s-%s-%s' % (host, port, username)
        password = encrypt.decode(password)
        db = Oracle.__pool.get(key)
        if db is None:
            # 池化，并且线程/进程安全
            db = PooledDB(cx_Oracle, **{'user': username, 'password': password, 'encoding': 'utf-8',
                                        'dsn': cx_Oracle.makedsn(host, port, database)})
            Oracle.__pool[key] = db
        return db


def _make_dict_factory(cursor):
    """ 用于将查询结果转换为dict """
    columns = [str(d[0]).upper() for d in cursor.description]

    def create_row(*args):
        return dict(zip(columns, args))

    return create_row


def _rows_to_dict(cursor):
    """ 用于将查询结果转换为dict """
    columns = [str(d[0]).upper() for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def query(db, sql):
    """执行查询的sql，并返回结果"""
    r = None
    conn = db.connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        # cur.rowfactory = _make_dict_factory(cur)
        # r = cur.fetchall()
        r = _rows_to_dict(cur)

    except Exception as ex:
        msg = 'query sql error %s, sql: [%s]' % (str(ex), sql)
        ctx.logger.log_status(msg, 4)
        logging.error(msg)
    finally:
        cur.close()
        conn.close()
    return r


def fetch_all(db, sql):
    """
    @note: 返回原始结果
    """
    r = None
    conn = db.connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        # cur.rowfactory = _make_dict_factory(cur)
        r = [line[0] for line in cur.fetchall()]

    except Exception as ex:
        msg = 'query sql error %s, sql: [%s]' % (str(ex), sql)
        ctx.logger.log_status(msg, 4)
        logging.error(msg)
    finally:
        cur.close()
        conn.close()
    return r


def execute(db, sql):
    """ 执行sql """
    conn = db.connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        msg = 'execute sql error %s, sql: [%s]' % (str(ex), sql)
        ctx.logger.log_status(msg, 4)
        logging.error(msg)
    finally:
        cur.close()
        conn.close()


def execute_many(db, sql_list):
    """ 执行sql """
    conn = db.connection()
    cur = conn.cursor()
    try:
        cur.executemany(sql_list)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        msg = 'execute sql error %s, sql: [%s]' % (str(ex), str(sql_list))
        ctx.logger.log_status(msg, 4)
        logging.error(msg)
    finally:
        cur.close()
        conn.close()


def count(db, sql):
    """ 获取计数结果 """
    conn = db.connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        r = cur.fetchone()
        if r is not None:
            return int(r[0])
    except Exception as ex:
        msg = 'count sql error %s, sql: [%s]' % (str(ex), sql)
        ctx.logger.log_status(msg, 4)
        logging.error(msg)
    finally:
        cur.close()
        conn.close()
    return 0
