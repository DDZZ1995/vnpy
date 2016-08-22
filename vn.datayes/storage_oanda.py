# encoding: UTF-8
from storage import *
from api_oanda import *

class DBConfigOanda(Config):
    """
	Json-like config object; inherits from Config()

	Contains all kinds of settings relating to database settings.

	privates
	--------
	Inherited from api.Config, plus:

	* client: pymongo.MongoClient object, the connection
	  that is to be used for this session.
	* body: dictionary; the main content of config.

			- client: pymongo.MongoClient(), refers to self.client.

			- dbs: dictionary, is a mapping from database alias
				   to another dictionary, which inclues configurations
				   and themselves(i.e. pymongo.database entity)
				   Concretely, dbs has the structure like:
				   {
				   		alias1 : {
				   			'self': client[dbName1],
				   			'index': dbIndex1,
				   			'collNames': collectionNameType1
				   		},
				   		alias2 : {
				   			'self': client[dbName2],
				   			'index': dbIndex2,
				   			'collNames': collectionNameType2
				   		}, ...
				   }
				   where alias#: string;
				   		 dbs.alias#.self: pymongo.database;
				   		 dbs.alias#.index: string;
				   		 dbs.alias#.collNames: string;

			- dbNames: list; a list of database alias.

	"""
    head = 'Oanda DB config '

    client = pymongo.MongoClient()
    body = {
        'client': client,
        'dbs': {
            'OANDA_M1': {
                'self': client['DATAYES_OANDA_M1'],
                'index': 'dateTime',
                'collNames': 'oandaTicker'
            },
            'OANDA_D1': {
                'self': client['DATAYES_OANDA_D1'],
                'index': 'dateTime',
                'collNames': 'oandaTicker'
            }
        },
        'dbNames': ['OANDA_M1', 'OANDA_D1'],
        'initDate': '2000-01-01T00:00:00.000000Z'  # 下载数据的初始日期设定
    }

    def __init__(self, head=None, token=None, body=None):
        """
		Inherited constructor.

		parameters
		----------
		* head: string; the name of config file. Default is None.
		* token: string; user's token.
		* body: dictionary; the main content of config
		"""
        super(DBConfigOanda, self).__init__(head, token, body)

    def view(self):
        """ Reloaded Prettify printing method. """
        config_view = {
            'dbConfig_head': self.head,
            'dbConfig_body': str(self.body),
        }
        print(json.dumps(config_view,
                         indent=4,
                         sort_keys=True))


# MongoDB Controller class
class MongodControllerOanda(MongodController):
    # _config = DBConfigOanda()
    # _api = None
    #
    # _client = None
    # _dbs = None
    # _dbNames = []
    # _collNames = dict()
    # _connected = False
    #
    # _mapTickersToSecIDs = dict()

    def __init__(self, config, api):
        """
        Constructor.

        parameters
        ----------
        * config: DBConfig object; specifies database configs.
        * api: PyApi object.

        """
        super(MongodControllerOanda, self).__init__(config, api)

    # ----------------------------------------------------------------------
    """
    Decorator;
    Targeting at path dName, if exists, read data from this file;
    if not, execute handle() which returns a json-like data and
    stores the data at dName path.

    parameters
    ----------
    * dName: string; the specific path of file that __md looks at.
    """

    def __md(dName):
        def _md(get):
            def handle(*args, **kwargs):
                try:
                    if os.path.isfile(dName):
                        # if directory exists, read from it.
                        jsonFile = open(dName, 'r')
                        data = json.loads(jsonFile.read())
                        jsonFile.close()
                    else:
                        # if not, get data via *get method,
                        # then write to the file.
                        data = get(*args, **kwargs)
                        jsonFile = open(dName, 'w+')
                        jsonFile.write(json.dumps(data))
                        jsonFile.close()
                    # print data
                    return data
                except Exception as e:
                    raise e

            return handle

        return _md

    @__md('names/oandaTicker.json')
    def _allOandaTickers(self):
        """get all equity tickers, decorated by @__md()."""
        data = self._api.get_oanda_instruments_list()
        allEquTickers = data
        return allEquTickers

    def _get_coll_names(self):
        """
        get all instruments'names and store them in self._collNames.

        """
        try:
            if not os.path.exists('names'):
                os.makedirs('names')

            self._collNames['oandaTicker'] = self._allOandaTickers()

            print '[MONGOD]: Collection names gotten.'
            return 1
        except AssertionError:
            warning = '[MONGOD]: Warning, collection names ' + \
                      'is an empty list.'
            print warning
        except Exception as e:
            msg = '[MONGOD]: Unable to set collection names; ' + \
                  str(e)
            raise VNPAST_DatabaseError(msg)

    def update_oanda_candles(self, freq, sessionNum=2):
        """
        自动数据维护方法
        """
        try:
            if freq == 'M1':
                db = self._dbs['OANDA_M1']['self']
            elif freq == 'D':
                db = self._dbs['OANDA_D1']['self']

            self._api.get_oanda_candles_mongod(db, freq, sessionNum)
        except Exception as e:
            msg = '[MONGOD]: Unable to download data; ' + str(e)
            raise VNPAST_DatabaseError(msg)

    def fetch(self, dbName, ticker, start, end, output='list'):
        """

        """
        # check inputs' validity.
        if output not in ['df', 'list', 'json']:
            raise ValueError('[MONGOD]: Unsupported output type.')
        if dbName not in self._dbNames:
            raise ValueError('[MONGOD]: Unable to locate database name.')

        db = self._dbs[dbName]
        dbSelf = db['self']
        dbIndex = db['index']
        try:
            coll = db[ticker]
            if len(start) == 8 and len(end) == 8:
                # yyyymmdd, len()=8
                start = datetime.strptime(start, '%Y%m%d')
                end = datetime.strptime(end, '%Y%m%d')
            elif len(start) == 14 and len(end) == 14:
                # yyyymmdd HH:MM, len()=14
                start = datetime.strptime(start, '%Y%m%d %H:%M')
                end = datetime.strptime(end, '%Y%m%d %H:%M')
            else:
                pass
            docs = []

            # find in MongoDB.
            for doc in coll.find(filter={dbIndex: {'$lte': end,
                                                   '$gte': start}}, projection={'_id': False}):
                docs.append(doc)

            if output == 'list':
                return docs[::-1]

        except Exception as e:
            msg = '[MONGOD]: Error encountered when fetching data' + \
                  'from MongoDB; ' + str(e)
            return -1

    def fetch2(self, dbName, ticker, start, end, output='list'):
        """

        """
        # check inputs' validity.
        if output not in ['df', 'list', 'json']:
            raise ValueError('[MONGOD]: Unsupported output type.')
        # if dbName not in self._dbNames:
        # 	raise ValueError('[MONGOD]: Unable to locate database name.')

        db = self._dbs[dbName]
        dbSelf = db['self']
        dbIndex = db['index']
        try:
            coll = dbSelf[ticker]
            if len(start) == 8 and len(end) == 8:
                # yyyymmdd, len()=8
                start = datetime.strptime(start, '%Y%m%d')
                end = datetime.strptime(end, '%Y%m%d')
            elif len(start) == 14 and len(end) == 14:
                # yyyymmdd HH:MM, len()=14
                start = datetime.strptime(start, '%Y%m%d %H:%M')
                end = datetime.strptime(end, '%Y%m%d %H:%M')
            else:
                pass
            docs = []

            # find in MongoDB.
            for doc in coll.find(filter={dbIndex: {'$lte': end,
                                                   '$gte': start}}, projection={'_id': False}):
                docs.append(doc)

            if output == 'list':
                return docs[::-1]

        except Exception as e:
            msg = '[MONGOD]: Error encountered when fetching data' + \
                  'from MongoDB; ' + str(e)
            return -1


if __name__ == '__main__':
    dc = DBConfigOanda()
    api = PyApiOanda(ConfigOanda())
    mc = MongodControllerOanda(dc, api)
    concurrent_limit = 2  # 并发线程

    mc._get_coll_names()
    mc._ensure_index()

    # 注意OANDA服务器限制连接并发数为2
    # mc.update_oanda_candles('D', concurrent_limit)
    mc.update_oanda_candles('M1', 2)

    # # 显示数据
    # # rates = mc.fetch2('OANDA_D1', 'EUR_USD', '20000101', '20170101')
    # # rates = mc.fetch2('OANDA_D1', 'NAS100_USD', '20000101', '20170101')
    # rates = mc.fetch2('OANDA_M1', 'SG30_SGD', '20160101', '20160201')
    # close_price_list = [d['closeMid'] for d in rates]
    #
    # import matplotlib.pyplot as plt
    # plt.plot(close_price_list)
    # plt.show()
    #
    # input()

    # ["AU200_AUD", "AUD_CAD", "AUD_CHF", "AUD_HKD", "AUD_JPY", "AUD_NZD", "AUD_SGD", "AUD_USD", "BCO_USD", "CAD_CHF",
    # "CAD_HKD", "CAD_JPY", "CAD_SGD", "CH20_CHF", "CHF_HKD", "CHF_JPY", "CHF_ZAR", "CORN_USD", "DE10YB_EUR", "DE30_EUR",
    # "EU50_EUR", "EUR_AUD", "EUR_CAD", "EUR_CHF", "EUR_CZK", "EUR_DKK", "EUR_GBP", "EUR_HKD", "EUR_HUF", "EUR_JPY",
    # "EUR_NOK", "EUR_NZD", "EUR_PLN", "EUR_SEK", "EUR_SGD", "EUR_TRY", "EUR_USD", "EUR_ZAR", "FR40_EUR", "GBP_AUD",
    # "GBP_CAD", "GBP_CHF", "GBP_HKD", "GBP_JPY", "GBP_NZD", "GBP_PLN", "GBP_SGD", "GBP_USD", "GBP_ZAR", "HK33_HKD",
    # "HKD_JPY", "JP225_USD", "NAS100_USD", "NATGAS_USD", "NL25_EUR", "NZD_CAD", "NZD_CHF", "NZD_HKD", "NZD_JPY",
    # "NZD_SGD", "NZD_USD", "SG30_SGD", "SGD_CHF", "SGD_HKD", "SGD_JPY", "SOYBN_USD", "SPX500_USD", "SUGAR_USD",
    # "TRY_JPY", "UK100_GBP", "UK10YB_GBP", "US2000_USD", "US30_USD", "USB02Y_USD", "USB05Y_USD", "USB10Y_USD",
    # "USB30Y_USD", "USD_CAD", "USD_CHF", "USD_CNH", "USD_CZK", "USD_DKK", "USD_HKD", "USD_HUF", "USD_INR",
    # "USD_JPY", "USD_MXN", "USD_NOK", "USD_PLN", "USD_SAR", "USD_SEK", "USD_SGD", "USD_THB", "USD_TRY", "USD_ZAR",
    # "WHEAT_USD", "WTICO_USD", "XAG_AUD", "XAG_CAD", "XAG_CHF", "XAG_EUR", "XAG_GBP", "XAG_HKD", "XAG_JPY", "XAG_NZD",
    # "XAG_SGD", "XAG_USD", "XAU_AUD", "XAU_CAD", "XAU_CHF", "XAU_EUR", "XAU_GBP", "XAU_HKD", "XAU_JPY", "XAU_NZD",
    # "XAU_SGD", "XAU_USD", "XAU_XAG", "XCU_USD", "XPD_USD", "XPT_USD", "ZAR_JPY"]
