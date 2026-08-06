import aiohttp as aio
import requests as req
import numpy as np
import pandas as pd
import json
import re
from io import StringIO
from datetime import date

 
apiKey = '5TFQU47K2QUCZVRF'
try:
    session = aio.ClientSession()
except RuntimeError as err:
    print("No Asychronus process spawned : ",err)
    session = req.Session()
    
    
class pullEquity:
    
    def __init__(self, ticker):
        self.ticker = ticker
        statement = ""
        self.url = f"https://www.alphavantage.co/query?function='{statement}'&symbol='{ticker}'&apikey="+ apiKey
        self.overview = "OVERVIEW"
        self.balanceSheet = "BALANCE_SHEET"
        self.incomeStatement = "INCOME_STATEMENT"
        self.cashFlow = "CASH_FLOW"
        self.timeSeriesPrice = "TIME_SERIES_DAILY"
   
    def pull_Overview(self):
        overview = session.get(self.url.format(self.overview,self.ticker))
        data_overview = overview.json()
        return normalizeData.normalizeClean(data_overview)
    def pull_balSheet(self):
        balSheet = session.get(self.url.format(self))
        data_balSheet = balSheet.json()
        return normalizeData.normalizeClean(data_balSheet)
    def pull_incState(self):
        incState = session.get(self.url.format(self.incomeStatement, self.ticker))
        data_incState = incState.json()
        return normalizeData.normalizeClean(data_incState)
    def pull_cashFlow(self):
        cashFlow = session.get(self.url.format(self.cashFlow,self.ticker))
        data_cashFlow = cashFlow.json()
        return normalizeData.normalizeClean(data_cashFlow)
    def pull_dailyPrice(self):
        dailyP = session.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='{self.ticker}'&outputsize=full&apikey=" + apiKey)
        data_dailyTimeSeries = dailyP.json()
        return normalizeData.normalizeClean(data_dailyTimeSeries)
                      
class pullGlobalMarketStatus:
    def pull_MarketStatus():
        glbStatus = session.get('https://www.alphavantage.co/query?function=MARKET_STATUS&'+apiKey)
        data = glbStatus.json()
        return normalizeData.normalizeClean(data)
                
class pullIndexes:
    
    def __init__(self, ticker,interval):
         self.url = f"https://www.alphavantage.co/query?function='{function1}'&symbol='{ticker}'&interval='{interval}'&apikey="+ apiKey
         function1 = "INDEX_DATA"
         self.function2 = "INDEX_CATALOG"
         interval = "DAILY"
         self.ticker = ticker
       
    def pull_Index(self):
        index = session.get(self.url.format(self.ticker,self.interval))
        data = index.json()
        return data

    def pull_Index_Catalog(self):
        catalog = session.get(f"https://www.alphavantage.co/query?function='{self.function2}'&apikey="+ apiKey)
        data = catalog.json()
        return data
    
class pullEconomicIndicators:
    def __init__(self, ticker):
        #needs fixed
        self.url = f"https://www.alphavantage.co/query?function=INDEX_DATA&symbol='{ticker}'&interval='{ticker}'&apikey=" + apiKey


class normalizeData:

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

    def normalizeClean(data):
        #Index data 
        if ("data" in data):
            df = pd.json_normalize(data['data'], sep='_')
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype('float64')
            df = df.replace({np.nan: None})
            #print(df)
            return df

        elif ("top_gainers" in data):
            df = pd.json_normalize(data['top_gainers'], sep='_')
            df2 = pd.json_normalize(data['top_losers'], sep='_')
            df3 = pd.json_normalize(data['most_actively_traded'], sep='_')

            df = normalizeData.set_datatype(df)
            df2 = normalizeData.set_datatype(df2)
            df3 = normalizeData.set_datatype(df3)

            return df, df2, df3

        elif (isinstance(data, pd.DataFrame) and "close" in data.columns):
            #data.drop(columns=['open', 'high', 'low', 'volume'], inplace=True)

            #data.set_index("timestamp", inplace=True)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            #df = df.replace({np.nan: None})
            return data

        elif ("Description" in data and "Beta" in data):
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


        elif ("quarterlyReports" in data):
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
            df = pd.json_normalize
            
            
        else:
            return None
            
        

