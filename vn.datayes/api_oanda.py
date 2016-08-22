#encoding: UTF-8
"""
Oanda平台的API接口

"""
from api import *

class ConfigOanda(object):
    """
    Json-like config object.

    The Config contains all kinds of settings and user info that
    could be useful in the implementation of Api wrapper.

    privates
    --------
    * head: string; the name of config file.
    * token: string; user's token.
    * body: dictionary; the main content of config.
            - domain: string, api domain.
            - ssl:  boolean, specifes http or https usage.
            - version: string, version of the api. Currently 'v1'.
            - header: dictionary; the request header which contains
                      authorization infomation.

    """
    # 装入配置文件
    jason_file = u'OnadaConfig.json'
    with open(jason_file, 'r') as f:
        val = f.read()
        config_json = json.loads(val)
        f.close()

    head = config_json[u'head']
    # toke_ = config_json[u'toke_']
    token = config_json[u'token']
    body = config_json[u'body']

    def __init__(self, head=None, token=None, body=None):
        """
        Reloaded constructor.

        parameters
        ----------
        * head: string; the name of config file. Default is None.
        * token: string; user's token.
        * body: dictionary; the main content of config
        """
        if head:
            self.head = head
        if token:
            self.token = token
        if body:
            self.body = body

    def view(self):
        """ Prettify printing method. """
        config_view = {
            'config_head': self.head,
            'config_body': self.body,
            'user_token': self.token
        }

        print(json.dumps(config_view,
                         indent=4,
                         sort_keys=True))


#----------------------------------------------------------------------
# Datayes Api class

class PyApiOanda(PyApi):
    """
    Python Oanda Api object.

    PyApiOanda should be initialized with a Config json. The config must be complete,
    in that once constructed, the private variables like request headers,
    tokens, etc. become constant values (inherited from config), and will be
    consistantly referred to whenever make requests.


    privates
    --------
    * _config: Config object; a container of all useful settings when making
      requests.
    * _ssl, _domain, _domain_stream, _version, _header, _account_id:
      boolean, string, string, string, dictionary, integer;
      just private references to the items in Config. See the docs of Config().
    * _session: requests.session object.

    examples
    --------
    """

    # OandaAPI的配置
    _config = ConfigOanda()

    # request stuffs
    _ssl = True
    _domain = ''
    _version = 'v1'
    _header = dict()
    _token = None

    _session = requests.session()

    def __init__(self, config):
        # 更新标志
        self.update_flag = False    # 更新标志，非更新则为数据插入方式

        # 调用基类的构造方法
        super(PyApiOanda, self).__init__(config)

    # ----------------------------------------------------------------------
    def get_oanda_instruments_list(self, output='list'):
        """ 获得合约ID的列表"""
        url = '{}/{}/instruments?'.format(self._domain, self._version)
        params = {"accountId": self._config.config_json["accountId"]}
        try:
            resp = self.__access(url=url, params=params)
            assert len(resp.json()) > 0
            if output == 'df':
                data = Bar(resp.json())
            elif output == 'list':
                instrument_info_list = resp.json()['instruments']
                data = [info[u'instrument'] for info in instrument_info_list]
            return data
        except AssertionError:
            return 0

    # ----------------------------------------------------------------------
    def __overlord(self, db, dName, target1, target2, freq, sessionNum):
        """
        Basic controller of multithreading request.
        Generates a list of all tickers, creates threads and distribute
        tasks to individual #_drudgery() functions.

        parameters
        ----------
        * db: pymongo.db object; the database which collections of bars will
          go into. Note that this database will be transferred to every
          drudgery functions created by controller.

        * start, end: string; Date mark formatted in 'YYYYMMDD'. Specifies the
          start/end point of collections of bars.

        * dName: string; the path of file where all tickers' infomation
          are stored in.

        * target1: method; targetting api method that overlord calls
          to get tasks list.

        * target2: method; the corresponding drudgery function.

        * sessionNum: integer; the number of threads that will be deploied.
          Concretely, the list of all tickers will be sub-divided into chunks,
          where chunkSize = len(allTickers)/sessionNum.

        """
        if os.path.isfile(dName):
            # if directory exists, read from it.
            jsonFile = open(dName, 'r')
            allTickers = json.loads(jsonFile.read())
            jsonFile.close()
        else:
            data = target1()
            allTickers = list(data.body['ticker'])

        chunkSize = len(allTickers) / sessionNum
        taskLists = [allTickers[k:k + chunkSize] for k in range(
            0, len(allTickers), chunkSize)]
        k = 0
        for tasks in taskLists:
            thrd = Thread(target=target2,
                          args=(k, db, freq, tasks))
            thrd.start()
            k += 1
        return 1

    # def get_oanda_D1_mongod(self, db, sessionNum=2):
    #     """
    #     Controller of get equity D1 method.
    #     """
    #     self.__overlord(db=db,
    #                     dName='names/oandaTicker.json',
    #                     target1=self.get_oanda_D1,
    #                     target2=self.get_oanda_D1_drudgery,
    #                     sessionNum=sessionNum)

    def get_oanda_candles_mongod(self, db, freq, sessionNum=2):
        """
        Controller of get equity M1 method.
        """

        # 如果start非空，则清除当前的collection后启动下载
        # TODO: 清空collection

        # 线程任务分配
        self.__overlord(db=db,
                        dName='names/oandaTicker.json',
                        target1=self.get_oanda_candles_max,
                        target2=self.get_oanda_candles_drudgery,
                        freq=freq,
                        sessionNum=sessionNum)

    # ----------------------------------------------------------------------#
    def get_oanda_candles_drudgery(self, id, db, freq, tasks=[]):
        """
        Drudgery function of getting equity_D1 bars.
        This method loops over a list of tasks(tickers) and get D1 bar
        for all these tickers. A new feature 'dateTime', combined by Y-m-d
        formatted date part and H:M time part, will be automatically added into
        every json-like documents. It would be a datetime.datetime() timestamp
        object. In this module, this feature should be the unique index for all
        collections.

        By programatically assigning creating and assigning tasks to drudgery
        functions, multi-threading download of data can be achieved.

        parameters
        ----------
        * id: integer; the ID of Drudgery session.
        * db: pymongo.db object; the database which collections of bars will
          go into.
        * start, end: string; Date mark formatted in 'YYYYMMDD'. Specifies the
          start/end point of collections of bars. Note that to ensure the
          success of every requests, the range amid start and end had better be
          no more than one month.
        * tasks: list of strings; the tickers that this drudgery function
          loops over.

        """
        if len(tasks) == 0:
            return 0

        # str to datetime inline functions.
        todt = lambda str_dt: datetime.strptime(str_dt, '%Y-%m-%dT%H:%M:%S.%fZ')
        update_dt = lambda d: d.update({'dateTime': todt(d['time'])})

        k, n = 1, len(tasks)
        for ticker in tasks:
            # 如果start非空，则获得最后数据的日期
            # find the latest timestamp in collection.
            try:
                coll = db[ticker]
                latest = coll.find_one(
                    sort=[('dateTime', pymongo.DESCENDING)])['dateTime']
                start = datetime.strftime(latest, '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                print('[{}] 目标合约数据集合不在数据库中，创建新集合并设置数据初始时间。'.format(ticker))
                # start = '2000-01-01T00:00:00.000000Z'
                start = '2016-08-01T00:00:00.000000Z'

            # 连续下载数据
            data_end_flag = False
            begin_date = start
            data = None
            block_num=0
            while not data_end_flag:
                try:
                    data = self.get_oanda_candles_max(start=begin_date,
                                              freq=freq,
                                              ticker=ticker,
                                              output='list')
                    map(update_dt, data)  # add datetime feature to docs.
                    coll = db[ticker]
                    block_num += 1

                    # if self.update_flag:
                    # for d in data:
                    #     coll.update({'dateTime':d['dateTime']}, {"$set":d}, True)
                    # else:
                    #     coll.insert_many(data, ordered=True)  # 数据库插入模式，禁止数据索引重复

                    # for d in data:
                    #     coll.update({'dateTime':d['dateTime']}, {"$set":d}, True)

                    # 首个记录使用更新方式插入
                    if len(data):
                        coll.update({'dateTime': data[0]['dateTime']}, {"$set": data[0]}, True)
                        if len(data)>1:
                            coll.insert_many(data[1:], ordered=True)  # 数据库插入模式，禁止数据索引重复

                    # coll.insert_many(data)
                    print('block:[{}:{}:{}] downloaded'.format(id, k, block_num))
                except ConnectionError:
                    # If choke connection, standby for 1sec an invoke again.
                    time.sleep(1)
                    self.get_oanda_candles_drudgery(
                        id, db, tasks)
                except AssertionError:
                    msg = '1:[API|Session{}]: '.format(id) + \
                          'Empty dataset in the response.'
                    print(msg)
                    return -1
                except Exception as e:
                    msg = '2:[API|Session{}]: '.format(id) + \
                          'Exception encountered when ' + \
                          'requesting data; ' + str(e)
                    print(msg)
                    return -1

                # 如果没有新数据则设置标志
                if data is None or len(data)<=1:
                    # print(ticker, '没有新M1数据，下载完成')
                    data_end_flag = True

                    print('[API|Session{}]: '.format(id) + \
                          'Finished {} in {}.'.format(k, n))
                    k += 1
                else:
                    last_data_time_str = data[-1]['time'].encode()
                    last_data_time = datetime.strptime(last_data_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    begin_date_dt = last_data_time + timedelta(minutes=1)
                    begin_date = datetime.strftime(begin_date_dt, '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_oanda_candles_max(self, start='', freq='D', ticker='EUR_USD', output='df'):
        """

        parameters
        ----------
        * field: string; variables that are to be requested. Available variables
          are: (* is unique for securities)

                - secID 				string.
                - tradeDate 			date(?).
                - ticker 				string.
                - secShortName 			string.
                - exchangeCD 			string.
                - preClosePrice 		double.
                - actPreClosePrice*		double.
                - openPrice		 		double.
                - highestPrice	 		double.
                - lowestPrice 			double.
                - closePrice 			double.
                - turnoverVol 			double.
                - turnoverValue 		double.
                - dealAmount* 			integer.
                - turnoverRate	 		double.
                - accumAdjFactor* 		double.
                - negMarketValue* 		double.
                - marketValue* 			double.
                - PE* 					double.
                - PE1* 					double.
                - PB* 					double.

          Field is an optional parameter, default setting returns all fields.

        * start, end: string; Date mark formatted in 'YYYYMMDD'. Specifies the
          start/end point of bar. Start and end are optional parameters. If
          start, end and ticker are all specified, default 'one' value will be
          abandoned.

        * secID: string; the security ID in the form of '000001.XSHG', i.e.
          ticker.exchange.

        * ticker: string; the trading code in the form of '000001'.

        * one: string; Date mark formatted in 'YYYYMMDD'.
          Specifies one date on which data of all tickers are to be requested.
          Note that to get effective json data response, at least one parameter
          in {secID, ticker, tradeDate} should be entered.

        * output: enumeration of strings; the format of output that will be
          returned. default is 'df', optionals are:
                - 'df': returns History object,
                      where ret.body is a dataframe.
                - 'list': returns a list of dictionaries.

        """
        # 'https://api-fxpractice.oanda.com/v1/candles?candleFormat=midpoint&end=2016-06-02T00%3A00%3A00.000000Z
        # &start=2016-06-01T00%3A00%3A00.000000Z&instrument=EUR_USD&granularity=M1'
        url = '{}/{}/candles?'.format(
            self._domain, self._version)

        params = {
            'candleFormat':'midpoint',
            'instrument':ticker,
            'granularity':freq,
            'start':start,
            'count':5000    # Oanda服务器限制的最大数据请求量
            # 'dailyAlignment':0,
            # 'alignmentTimezone':'Asia%2FHong_Kong'
        }
        try:
            resp = self.__access(url=url, params=params)
            if not resp:
                return []

            assert len(resp.json()) > 0
            if output == 'df':
                data = History(resp.json())
            elif output == 'list':
                data = resp.json()['candles']
            return data
        # return resp
        except AssertionError:
            return 0

    def __access(self, url, params, method='GET'):
        """ 因为是私有方法，故拷贝过来
        request specific data from given url with parameters.

        parameters
        ----------
        * url: string.
        * params: dictionary.
        * method: string; 'GET' or 'POST', request method.

        """
        try:
            assert type(url) == str
            assert type(params) == dict
        except AssertionError as e:
            raise e('[API]: Unvalid url or parameter input.')
        if not self._session:
            s = requests.session()
        else:
            s = self._session

        # prepare and send the request.
        resp = ''
        try:
            req = requests.Request(method,
                                   url=url,
                                   headers=self._header,
                                   params=params)
            prepped = s.prepare_request(req)  # prepare the request
            resp = s.send(prepped, stream=False, verify=True)
            if method == 'GET':
                # 204是没有返回内容，意味着没有新数据
                assert resp.status_code == 200  # or resp.status_code == 204
            elif method == 'POST':
                assert resp.status_code == 201
            return resp
        except AssertionError:
            if resp:
                if resp.status_code == 204:     # 无内容返回
                    return

            msg = '[API]: Bad request, unexpected response status: ' + \
                  str(resp.status_code)
            raise VNPAST_RequestError(msg)
            pass
        except Exception as e:
            msg = '[API]: Bad request.' + str(e)
            raise VNPAST_RequestError(msg)
