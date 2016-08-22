#!/usr /bin/env python
# -*- coding: utf-8 -*-

"""
.生成配置文件
.生成合约列表文件
"""
import json as json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    config_json = {
        u'head' : u'my config',
        u'token' : u"此处填写获得的TOKEN",
        u"accountId": u"此处填写获得的账号",
        u"settingName": u"practice"
    }

    config_json[u'body'] = {
        u'ssl': True,
        u'domain': u'api-fxpractice.oanda.com', # api-fxpractice.oanda.com/v1/instruments
        # 'https://stream-fxpractice.oanda.com'
        #  https://api-fxtrade.oanda.com
        u'version': u'v1',
        u'header': {
            u'Connection': u'keep-alive',
            u'Authorization': u'Bearer ' + config_json[u'token']
        }
        # '/v1/instruments'
        # 'path': '/v1/candles'
        # 'https://api-fxpractice.oanda.com/v1/instruments?accountId=7352060'
        # 'https://api-fxpractice.oanda.com/v1/candles?count=5000&candleFormat=midpoint&end=2016-06-02T00%3A00%3A00.000000Z&start=2000-01-01T00%3A00%3A00.000000Z&instrument=EUR_USD&granularity=D'
        # 'https://api-fxpractice.oanda.com/v1/candles?count=5000&candleFormat=midpoint&start=2000-01-01T00%3A00%3A00.000000Z&instrument=EUR_USD&granularity=D'
        # 'https://api-fxpractice.oanda.com/v1/candles?count=5000&candleFormat=midpoint&start=2000-01-01T00%3A00%3A00.000000Z&instrument=EUR_USD&granularity=M1'
        # https://api-fxpractice.oanda.com/v1/candles?count=10&candleFormat=midpoint&start=2000-01-01T00%3A00%3A00.000000Z&instrument=EUR_USD&granularity=M1
        # 获取某天的1M数据
        # 'https://api-fxpractice.oanda.com/v1/candles?candleFormat=midpoint&end=2016-06-02T00%3A00%3A00.000000Z&start=2016-06-01T00%3A00%3A00.000000Z&instrument=EUR_USD&granularity=M1'
        # {'endDate': 20170101, 'secID': '', 'tradeDate': '', 'beginDate': 20000101, 'field': '', 'ticker': u'EUR_USD'}
        # 过程中获得 'https://api-fxpractice.oanda.com/v1/api/market/getBarHistDateRange.json?endDate=20170101&secID=&tradeDate=&beginDate=20000101&field=&ticker=CHF_HKD'
        # candleFormat = midpoint start=2000-01-01T00%3A00%3A00.000000Z  instrument=EUR_USD granularity=M1 end=2016-06-02T00%3A00%3A00.000000Z
        # https://api-fxpractice.oanda.com/v1/candles?candleFormat=midpoint&start=2000-01-01T00%3A00%3A00.000000Z&instrument=EUR_USD&granularity=M1

        # curl -X GET "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=120&candleFormat=midpoint&granularity=M1&dailyAlignment=0&alignmentTimezone=America%2FNew_York"
        # 读取一天的M1数据，长度限制只能读取三天的数据，<=5000
        # https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&start=2007-01-02T00%3A00%3A00.000000Z&end=2007-01-03T00%3A00%3A00.000000Z&candleFormat=midpoint&granularity=M1

        # 'https://api-fxpractice.oanda.com/v1/candles?instrument=SG30_SGD&candleFormat=midpoint&end=2016-08-22T09%3A43%3A09.377000Z&start=2016-08-22T21%3A00%3A00.000000Z&granularity=D'
    }

    body_dict = config_json[u'body']

    # 产生URL
    # url = '{}/{}/api/market/getBarHistDateRange.json'.format(
    url = '{}/{}/candles'.format(
        body_dict[u'domain'], body_dict[u'version'])
    config_json[u'bar_history_url'] = url


    with open(u'oandaConfig.json', 'w') as f:
        f.write(json.dumps(config_json, ensure_ascii=False, indent=4))

    f.close()

    instrument_response_dict = {u'instruments': [
        {u'pip': u'1.0', u'instrument': u'AU200_AUD', u'maxTradeUnits': 200, u'displayName': u'Australia 200'},
        {u'pip': u'0.0001', u'instrument': u'AUD_CAD', u'maxTradeUnits': 10000000, u'displayName': u'AUD/CAD'},
        {u'pip': u'0.0001', u'instrument': u'AUD_CHF', u'maxTradeUnits': 10000000, u'displayName': u'AUD/CHF'},
        {u'pip': u'0.0001', u'instrument': u'AUD_HKD', u'maxTradeUnits': 10000000, u'displayName': u'AUD/HKD'},
        {u'pip': u'0.01', u'instrument': u'AUD_JPY', u'maxTradeUnits': 10000000, u'displayName': u'AUD/JPY'},
        {u'pip': u'0.0001', u'instrument': u'AUD_NZD', u'maxTradeUnits': 10000000, u'displayName': u'AUD/NZD'},
        {u'pip': u'0.0001', u'instrument': u'AUD_SGD', u'maxTradeUnits': 10000000, u'displayName': u'AUD/SGD'},
        {u'pip': u'0.0001', u'instrument': u'AUD_USD', u'maxTradeUnits': 10000000, u'displayName': u'AUD/USD'},
        {u'pip': u'0.01', u'instrument': u'BCO_USD', u'maxTradeUnits': 10000, u'displayName': u'Brent Crude Oil'},
        {u'pip': u'0.0001', u'instrument': u'CAD_CHF', u'maxTradeUnits': 10000000, u'displayName': u'CAD/CHF'},
        {u'pip': u'0.0001', u'instrument': u'CAD_HKD', u'maxTradeUnits': 10000000, u'displayName': u'CAD/HKD'},
        {u'pip': u'0.01', u'instrument': u'CAD_JPY', u'maxTradeUnits': 10000000, u'displayName': u'CAD/JPY'},
        {u'pip': u'0.0001', u'instrument': u'CAD_SGD', u'maxTradeUnits': 10000000, u'displayName': u'CAD/SGD'},
        {u'pip': u'1.0', u'instrument': u'CH20_CHF', u'maxTradeUnits': 100, u'displayName': u'Swiss 20'},
        {u'pip': u'0.0001', u'instrument': u'CHF_HKD', u'maxTradeUnits': 10000000, u'displayName': u'CHF/HKD'},
        {u'pip': u'0.01', u'instrument': u'CHF_JPY', u'maxTradeUnits': 10000000, u'displayName': u'CHF/JPY'},
        {u'pip': u'0.0001', u'instrument': u'CHF_ZAR', u'maxTradeUnits': 10000000, u'displayName': u'CHF/ZAR'},
        {u'pip': u'0.01', u'instrument': u'CORN_USD', u'maxTradeUnits': 150000, u'displayName': u'Corn'},
        {u'pip': u'0.01', u'instrument': u'DE10YB_EUR', u'maxTradeUnits': 6000, u'displayName': u'Bund'},
        {u'pip': u'1.0', u'instrument': u'DE30_EUR', u'maxTradeUnits': 250, u'displayName': u'Germany 30'},
        {u'pip': u'1.0', u'instrument': u'EU50_EUR', u'maxTradeUnits': 300, u'displayName': u'Europe 50'},
        {u'pip': u'0.0001', u'instrument': u'EUR_AUD', u'maxTradeUnits': 10000000, u'displayName': u'EUR/AUD'},
        {u'pip': u'0.0001', u'instrument': u'EUR_CAD', u'maxTradeUnits': 10000000, u'displayName': u'EUR/CAD'},
        {u'pip': u'0.0001', u'instrument': u'EUR_CHF', u'maxTradeUnits': 10000000, u'displayName': u'EUR/CHF'},
        {u'pip': u'0.0001', u'instrument': u'EUR_CZK', u'maxTradeUnits': 10000000, u'displayName': u'EUR/CZK'},
        {u'pip': u'0.0001', u'instrument': u'EUR_DKK', u'maxTradeUnits': 10000000, u'displayName': u'EUR/DKK'},
        {u'pip': u'0.0001', u'instrument': u'EUR_GBP', u'maxTradeUnits': 10000000, u'displayName': u'EUR/GBP'},
        {u'pip': u'0.0001', u'instrument': u'EUR_HKD', u'maxTradeUnits': 10000000, u'displayName': u'EUR/HKD'},
        {u'pip': u'0.01', u'instrument': u'EUR_HUF', u'maxTradeUnits': 10000000, u'displayName': u'EUR/HUF'},
        {u'pip': u'0.01', u'instrument': u'EUR_JPY', u'maxTradeUnits': 10000000, u'displayName': u'EUR/JPY'},
        {u'pip': u'0.0001', u'instrument': u'EUR_NOK', u'maxTradeUnits': 10000000, u'displayName': u'EUR/NOK'},
        {u'pip': u'0.0001', u'instrument': u'EUR_NZD', u'maxTradeUnits': 10000000, u'displayName': u'EUR/NZD'},
        {u'pip': u'0.0001', u'instrument': u'EUR_PLN', u'maxTradeUnits': 10000000, u'displayName': u'EUR/PLN'},
        {u'pip': u'0.0001', u'instrument': u'EUR_SEK', u'maxTradeUnits': 10000000, u'displayName': u'EUR/SEK'},
        {u'pip': u'0.0001', u'instrument': u'EUR_SGD', u'maxTradeUnits': 10000000, u'displayName': u'EUR/SGD'},
        {u'pip': u'0.0001', u'instrument': u'EUR_TRY', u'maxTradeUnits': 10000000, u'displayName': u'EUR/TRY'},
        {u'pip': u'0.0001', u'instrument': u'EUR_USD', u'maxTradeUnits': 10000000, u'displayName': u'EUR/USD'},
        {u'pip': u'0.0001', u'instrument': u'EUR_ZAR', u'maxTradeUnits': 10000000, u'displayName': u'EUR/ZAR'},
        {u'pip': u'1.0', u'instrument': u'FR40_EUR', u'maxTradeUnits': 200, u'displayName': u'France 40'},
        {u'pip': u'0.0001', u'instrument': u'GBP_AUD', u'maxTradeUnits': 10000000, u'displayName': u'GBP/AUD'},
        {u'pip': u'0.0001', u'instrument': u'GBP_CAD', u'maxTradeUnits': 10000000, u'displayName': u'GBP/CAD'},
        {u'pip': u'0.0001', u'instrument': u'GBP_CHF', u'maxTradeUnits': 10000000, u'displayName': u'GBP/CHF'},
        {u'pip': u'0.0001', u'instrument': u'GBP_HKD', u'maxTradeUnits': 10000000, u'displayName': u'GBP/HKD'},
        {u'pip': u'0.01', u'instrument': u'GBP_JPY', u'maxTradeUnits': 10000000, u'displayName': u'GBP/JPY'},
        {u'pip': u'0.0001', u'instrument': u'GBP_NZD', u'maxTradeUnits': 10000000, u'displayName': u'GBP/NZD'},
        {u'pip': u'0.0001', u'instrument': u'GBP_PLN', u'maxTradeUnits': 10000000, u'displayName': u'GBP/PLN'},
        {u'pip': u'0.0001', u'instrument': u'GBP_SGD', u'maxTradeUnits': 10000000, u'displayName': u'GBP/SGD'},
        {u'pip': u'0.0001', u'instrument': u'GBP_USD', u'maxTradeUnits': 10000000, u'displayName': u'GBP/USD'},
        {u'pip': u'0.0001', u'instrument': u'GBP_ZAR', u'maxTradeUnits': 10000000, u'displayName': u'GBP/ZAR'},
        {u'pip': u'1.0', u'instrument': u'HK33_HKD', u'maxTradeUnits': 400, u'displayName': u'Hong Kong 33'},
        {u'pip': u'0.0001', u'instrument': u'HKD_JPY', u'maxTradeUnits': 10000000, u'displayName': u'HKD/JPY'},
        {u'pip': u'1.0', u'instrument': u'JP225_USD', u'maxTradeUnits': 100, u'displayName': u'Japan 225'},
        {u'pip': u'1.0', u'instrument': u'NAS100_USD', u'maxTradeUnits': 400, u'displayName': u'US Nas 100'},
        {u'pip': u'0.01', u'instrument': u'NATGAS_USD', u'maxTradeUnits': 250000, u'displayName': u'Natural Gas'},
        {u'pip': u'0.01', u'instrument': u'NL25_EUR', u'maxTradeUnits': 2000, u'displayName': u'Netherlands 25'},
        {u'pip': u'0.0001', u'instrument': u'NZD_CAD', u'maxTradeUnits': 10000000, u'displayName': u'NZD/CAD'},
        {u'pip': u'0.0001', u'instrument': u'NZD_CHF', u'maxTradeUnits': 10000000, u'displayName': u'NZD/CHF'},
        {u'pip': u'0.0001', u'instrument': u'NZD_HKD', u'maxTradeUnits': 10000000, u'displayName': u'NZD/HKD'},
        {u'pip': u'0.01', u'instrument': u'NZD_JPY', u'maxTradeUnits': 10000000, u'displayName': u'NZD/JPY'},
        {u'pip': u'0.0001', u'instrument': u'NZD_SGD', u'maxTradeUnits': 10000000, u'displayName': u'NZD/SGD'},
        {u'pip': u'0.0001', u'instrument': u'NZD_USD', u'maxTradeUnits': 10000000, u'displayName': u'NZD/USD'},
        {u'pip': u'0.1', u'instrument': u'SG30_SGD', u'maxTradeUnits': 300, u'displayName': u'Singapore 30'},
        {u'pip': u'0.0001', u'instrument': u'SGD_CHF', u'maxTradeUnits': 10000000, u'displayName': u'SGD/CHF'},
        {u'pip': u'0.0001', u'instrument': u'SGD_HKD', u'maxTradeUnits': 10000000, u'displayName': u'SGD/HKD'},
        {u'pip': u'0.01', u'instrument': u'SGD_JPY', u'maxTradeUnits': 10000000, u'displayName': u'SGD/JPY'},
        {u'pip': u'0.01', u'instrument': u'SOYBN_USD', u'maxTradeUnits': 60000, u'displayName': u'Soybeans'},
        {u'pip': u'1.0', u'instrument': u'SPX500_USD', u'maxTradeUnits': 800, u'displayName': u'US SPX 500'},
        {u'pip': u'0.0001', u'instrument': u'SUGAR_USD', u'maxTradeUnits': 4000000, u'displayName': u'Sugar'},
        {u'pip': u'0.01', u'instrument': u'TRY_JPY', u'maxTradeUnits': 10000000, u'displayName': u'TRY/JPY'},
        {u'pip': u'1.0', u'instrument': u'UK100_GBP', u'maxTradeUnits': 100, u'displayName': u'UK 100'},
        {u'pip': u'0.01', u'instrument': u'UK10YB_GBP', u'maxTradeUnits': 6000, u'displayName': u'UK 10Y Gilt'},
        {u'pip': u'0.01', u'instrument': u'US2000_USD', u'maxTradeUnits': 1000, u'displayName': u'US Russ 2000'},
        {u'pip': u'1.0', u'instrument': u'US30_USD', u'maxTradeUnits': 100, u'displayName': u'US Wall St 30'},
        {u'pip': u'0.01', u'instrument': u'USB02Y_USD', u'maxTradeUnits': 6000, u'displayName': u'US 2Y T-Note'},
        {u'pip': u'0.01', u'instrument': u'USB05Y_USD', u'maxTradeUnits': 6000, u'displayName': u'US 5Y T-Note'},
        {u'pip': u'0.01', u'instrument': u'USB10Y_USD', u'maxTradeUnits': 6000, u'displayName': u'US 10Y T-Note'},
        {u'pip': u'0.01', u'instrument': u'USB30Y_USD', u'maxTradeUnits': 6000, u'displayName': u'US T-Bond'},
        {u'pip': u'0.0001', u'instrument': u'USD_CAD', u'maxTradeUnits': 10000000, u'displayName': u'USD/CAD'},
        {u'pip': u'0.0001', u'instrument': u'USD_CHF', u'maxTradeUnits': 10000000, u'displayName': u'USD/CHF'},
        {u'pip': u'0.0001', u'instrument': u'USD_CNH', u'maxTradeUnits': 10000000, u'displayName': u'USD/CNH'},
        {u'pip': u'0.0001', u'instrument': u'USD_CZK', u'maxTradeUnits': 10000000, u'displayName': u'USD/CZK'},
        {u'pip': u'0.0001', u'instrument': u'USD_DKK', u'maxTradeUnits': 10000000, u'displayName': u'USD/DKK'},
        {u'pip': u'0.0001', u'instrument': u'USD_HKD', u'maxTradeUnits': 10000000, u'displayName': u'USD/HKD'},
        {u'pip': u'0.01', u'instrument': u'USD_HUF', u'maxTradeUnits': 10000000, u'displayName': u'USD/HUF'},
        {u'pip': u'0.01', u'instrument': u'USD_INR', u'maxTradeUnits': 10000000, u'displayName': u'USD/INR'},
        {u'pip': u'0.01', u'instrument': u'USD_JPY', u'maxTradeUnits': 10000000, u'displayName': u'USD/JPY'},
        {u'pip': u'0.0001', u'instrument': u'USD_MXN', u'maxTradeUnits': 10000000, u'displayName': u'USD/MXN'},
        {u'pip': u'0.0001', u'instrument': u'USD_NOK', u'maxTradeUnits': 10000000, u'displayName': u'USD/NOK'},
        {u'pip': u'0.0001', u'instrument': u'USD_PLN', u'maxTradeUnits': 10000000, u'displayName': u'USD/PLN'},
        {u'pip': u'0.0001', u'instrument': u'USD_SAR', u'maxTradeUnits': 10000000, u'displayName': u'USD/SAR'},
        {u'pip': u'0.0001', u'instrument': u'USD_SEK', u'maxTradeUnits': 10000000, u'displayName': u'USD/SEK'},
        {u'pip': u'0.0001', u'instrument': u'USD_SGD', u'maxTradeUnits': 10000000, u'displayName': u'USD/SGD'},
        {u'pip': u'0.01', u'instrument': u'USD_THB', u'maxTradeUnits': 10000000, u'displayName': u'USD/THB'},
        {u'pip': u'0.0001', u'instrument': u'USD_TRY', u'maxTradeUnits': 10000000, u'displayName': u'USD/TRY'},
        {u'pip': u'0.0001', u'instrument': u'USD_ZAR', u'maxTradeUnits': 10000000, u'displayName': u'USD/ZAR'},
        {u'pip': u'0.01', u'instrument': u'WHEAT_USD', u'maxTradeUnits': 150000, u'displayName': u'Wheat'},
        {u'pip': u'0.01', u'instrument': u'WTICO_USD', u'maxTradeUnits': 10000, u'displayName': u'West Texas Oil'},
        {u'pip': u'0.0001', u'instrument': u'XAG_AUD', u'maxTradeUnits': 50000, u'displayName': u'Silver/AUD'},
        {u'pip': u'0.0001', u'instrument': u'XAG_CAD', u'maxTradeUnits': 50000, u'displayName': u'Silver/CAD'},
        {u'pip': u'0.0001', u'instrument': u'XAG_CHF', u'maxTradeUnits': 50000, u'displayName': u'Silver/CHF'},
        {u'pip': u'0.0001', u'instrument': u'XAG_EUR', u'maxTradeUnits': 50000, u'displayName': u'Silver/EUR'},
        {u'pip': u'0.0001', u'instrument': u'XAG_GBP', u'maxTradeUnits': 50000, u'displayName': u'Silver/GBP'},
        {u'pip': u'0.0001', u'instrument': u'XAG_HKD', u'maxTradeUnits': 50000, u'displayName': u'Silver/HKD'},
        {u'pip': u'1.0', u'instrument': u'XAG_JPY', u'maxTradeUnits': 50000, u'displayName': u'Silver/JPY'},
        {u'pip': u'0.0001', u'instrument': u'XAG_NZD', u'maxTradeUnits': 50000, u'displayName': u'Silver/NZD'},
        {u'pip': u'0.0001', u'instrument': u'XAG_SGD', u'maxTradeUnits': 50000, u'displayName': u'Silver/SGD'},
        {u'pip': u'0.0001', u'instrument': u'XAG_USD', u'maxTradeUnits': 50000, u'displayName': u'Silver'},
        {u'pip': u'0.01', u'instrument': u'XAU_AUD', u'maxTradeUnits': 2000, u'displayName': u'Gold/AUD'},
        {u'pip': u'0.01', u'instrument': u'XAU_CAD', u'maxTradeUnits': 2000, u'displayName': u'Gold/CAD'},
        {u'pip': u'0.01', u'instrument': u'XAU_CHF', u'maxTradeUnits': 2000, u'displayName': u'Gold/CHF'},
        {u'pip': u'0.01', u'instrument': u'XAU_EUR', u'maxTradeUnits': 2000, u'displayName': u'Gold/EUR'},
        {u'pip': u'0.01', u'instrument': u'XAU_GBP', u'maxTradeUnits': 2000, u'displayName': u'Gold/GBP'},
        {u'pip': u'0.01', u'instrument': u'XAU_HKD', u'maxTradeUnits': 2000, u'displayName': u'Gold/HKD'},
        {u'pip': u'10', u'instrument': u'XAU_JPY', u'maxTradeUnits': 2000, u'displayName': u'Gold/JPY'},
        {u'pip': u'0.01', u'instrument': u'XAU_NZD', u'maxTradeUnits': 2000, u'displayName': u'Gold/NZD'},
        {u'pip': u'0.01', u'instrument': u'XAU_SGD', u'maxTradeUnits': 2000, u'displayName': u'Gold/SGD'},
        {u'pip': u'0.01', u'instrument': u'XAU_USD', u'maxTradeUnits': 2000, u'displayName': u'Gold'},
        {u'pip': u'0.01', u'instrument': u'XAU_XAG', u'maxTradeUnits': 2000, u'displayName': u'Gold/Silver'},
        {u'pip': u'0.0001', u'instrument': u'XCU_USD', u'maxTradeUnits': 250000, u'displayName': u'Copper'},
        {u'pip': u'0.01', u'instrument': u'XPD_USD', u'maxTradeUnits': 500, u'displayName': u'Palladium'},
        {u'pip': u'0.01', u'instrument': u'XPT_USD', u'maxTradeUnits': 500, u'displayName': u'Platinum'},
        {u'pip': u'0.01', u'instrument': u'ZAR_JPY', u'maxTradeUnits': 10000000, u'displayName': u'ZAR/JPY'}]}

    # 生成合约字典
    instrument_dict = instrument_response_dict[u'instruments']
    # 生成合约列表
    instrument_list = [d[u'instrument'] for d in instrument_dict]
    # test_list
    test_list = instrument_list[:60]

    with open(u'names/oandaTicker.json', 'w') as f:
        f.write(json.dumps(test_list, ensure_ascii=False, indent=4))
    f.close()
