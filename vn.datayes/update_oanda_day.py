# encoding: UTF-8
""" OANDA平台傻瓜式数据维护工具 v0.8 by DDZZ1995 联系 Q:2215712
"""
from storage_oanda import *
from api_oanda import *

if __name__ == '__main__':
    dc = DBConfigOanda()
    api = PyApiOanda(ConfigOanda())
    mc = MongodControllerOanda(dc, api)
    concurrent_limit = 2  # 并发线程

    mc._get_coll_names()
    mc._ensure_index()

    # 注意OANDA服务器限制连接并发数为2
    # 维护日线数据
    mc.update_oanda_candles('D', concurrent_limit)

