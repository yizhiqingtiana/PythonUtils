#encoding: utf-8
'''
Created on 2013-9-12

@author: zuojingchao01
'''
import logging
class Log():
    '''
    该类提供获取一个log对象的方法
    '''
    DEBUG = logging.DEBUG
    INFO  = logging.INFO
    WARN  = logging.WARN
    ERROR = logging.ERROR
    @staticmethod
    def get_logger(name, levelname = DEBUG):
        log = logging.getLogger(name)
        log.setLevel(levelname);
        sh = logging.StreamHandler()
        fmt = logging.Formatter('%(asctime)s %(filename)s %(lineno)d %(levelname)s: %(name)s %(message)s')
        #fmt = logging.Formatter('%(asctime)s %(levelname)s: %(name)s %(message)s')
        sh.setFormatter(fmt)
        log.addHandler(sh)
        return log
