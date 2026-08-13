import aiohttp as aio
import requests as req
import numpy as np
import pandas as pd
import json
import re
import asyncio
from io import StringIO
from datetime import date
from pandas import DataFrame



class EquitySecurity:
    def __init__(self, overview,
                balance_sheet,
                income_statement,
                cashflow_statement):
        self.overview = overview
        self.balance_sheet = balance_sheet
        self.income_statement = income_statement
        self.cash_flow = cashflow_statement

class PullInstruments:
    def __init__(self, ticker):
        self.ticker = ticker
        self.overview = "OVERVIEW"
        self.balanceSheet = "BALANCE_SHEET"
        self.incomeStatement = "INCOME_STATEMENT"
        self.cashFlow = "CASH_FLOW"
        self.timeSeriesDaily = "TIME_SERIES_DAILY"
        self.attributeArray = [self.overview,
                               self.balanceSheet,
                               self.incomeStatement,
                               self.cashFlow]



    @staticmethod
    async def pull_data(url_a:int, function=None, ticker=None, interval=None):
        url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey=5TFQU47K2QUCZVRF"
        url_daily_price = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&outputsize=full&apikey=5TFQU47K2QUCZVRF"
        url_indexes =  f"https://www.alphavantage.co/query?function='{function}'&symbol='{ticker}'&interval='{interval}'&apikey=5TFQU47K2QUCZVRF"
        market_status = f'https://www.alphavantage.co/query?function={function}&'
        economic_indicators = f"https://www.alphavantage.co/query?function={function}&symbol='{ticker}'&interval='{interval}'&apikey=5TFQU47K2QUCZVRF"
        if url_a == 0:
            url = url_daily_price
        elif url_a == 1:
            url = url
        elif url_a == 2:
            url = url_indexes
        elif url_a == 3:
            url = market_status
        elif url_a == 4:
            url = economic_indicators


        timeout = aio.ClientTimeout(total=120,connect=120,sock_connect=120)

        print("Attempting Connection")
        async with aio.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    print(response)
                    if response.status != 200:
                        raise aio.ClientError
                    data = await response.json()
                    normalized_obj = await Normalizedata.normalize_clean(data)
                    await asyncio.sleep(0.5)
                    return normalized_obj



    @staticmethod
    def iterate_request(ticker: str, statement : str):
        if statement != PullInstruments(ticker).timeSeriesDaily:
            data = PullInstruments.pull_data(1, statement, ticker)
            return data
        else:
            data = PullInstruments.pull_data(1, statement, ticker)
            return data

    @staticmethod
    async def pull_all_statements(attribute_array, ticker):

            tasks = [PullInstruments.iterate_request(ticker, i) for i in attribute_array]
            results = await asyncio.gather(*tasks)
            catch = EquitySecurity(*results)
            print("Statements returned")
            print(catch)
            return catch

        
# class pullGlobalMarketStatus:
#     async def pull_market_status(self):
#         glb_status = await asyncio.get()
#         data = glb_status.json()
#         return Normalizedata.normalize_clean(data)
                
# class pullIndexes:
#     def __init__(self, ticker,interval):
#          self.url = f"https://www.alphavantage.co/query?function='{function1}'&symbol='{ticker}'&interval='{interval}'&apikey="+ apiKey
#          function1 = "INDEX_DATA"
#          self.function2 = "INDEX_CATALOG"
#          interval = "DAILY"
#          self.ticker = ticker
#
#     def pull_Index(self):
#         index = asyncio.get(self.url.format(self.ticker,self.interval))
#         data = index.json()
#         return data
#
#     def pull_Index_Catalog(self):
#         catalog = asyncio.get(f"https://www.alphavantage.co/query?function='{self.function2}'&apikey="+ apiKey)
#         data = catalog.json()
#         return data
#
# class pullEconomicIndicators:
#     def __init__(self, ticker):
#         #needs fixed
#         self.url = f"https://www.alphavantage.co/query?function=INDEX_DATA&symbol='{ticker}'&interval='{ticker}'&apikey=" + apiKey


class Normalizedata:

    @staticmethod
    def set_datatype(df):
        for col in df.columns:
            if col == 'ticker':
                df[col] = df[col].astype('str')
            elif col == 'change_percentage':
                df[col] = df[col].str.rstrip('%')
                df[col] = df[col].astype('float64')
            elif col != 'ticker' and col != 'change_percentage':
                df[col] = df[col].astype('float64')

        return df
    @staticmethod
    async def normalize_clean(data):
        #Index data
        if "data" in data:
            df = pd.json_normalize(data['data'], sep='_')
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype('float64')
            df = df.replace({np.nan: None})
            #print(df)
            return df

        elif "top_gainers" in data:
            df = pd.json_normalize(data['top_gainers'], sep='_')
            df2 = pd.json_normalize(data['top_losers'], sep='_')
            df3 = pd.json_normalize(data['most_actively_traded'], sep='_')

            df = Normalizedata.set_datatype
            df2 = Normalizedata.set_datatype
            df3 = Normalizedata.set_datatype

            return df, df2, df3

        elif isinstance(data, pd.DataFrame) and "close" in data.columns:
            #data.drop(columns=['open', 'high', 'low', 'volume'], inplace=True)

            #data.set_index("timestamp", inplace=True)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            #df = df.replace({np.nan: None})
            return data

        elif "Description" in data and "Beta" in data:
            df = pd.json_normalize(data, sep='_').T
            #print(df.info())
            df.replace("None", 0, inplace=True)
            df.replace("-", 0, inplace=True)
            df = df.T
            df = df.rename(columns={
                '52WeekHigh': '_52WeekHigh',
                '52WeekLow': '_52WeekLow',
                '50DayMovingAverage': '_50DayMovingAverage',
                '200DayMovingAverage': '_200DayMovingAverage'
            })

            return df


        elif "quarterlyReports" in data:
            df = pd.json_normalize(data['quarterlyReports'], sep='_')
            df.drop(columns=['reportedCurrency'], inplace=True)
            df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding']).dt.date
            df.replace("None", np.nan, inplace=True)
            #df = df.where(pd.notnull(df), None)
            if 'grossProfit' in df.columns:
                for col in df.columns:
                    if col != 'fiscalDateEnding':
                        df[col] = df[col].astype('float64')
            df = df.replace({np.nan: None})
            #print(df)
            return df

        elif data is not None:
            df = pd.json_normalize(data)
            return df



            
        

