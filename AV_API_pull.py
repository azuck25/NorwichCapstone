import aiohttp as aio
import requests as req
import numpy as np
import pandas as pd
import json
import re
import asyncio
from io import StringIO
from datetime import date

 

class equitySecurity:
    def __int__(self, ticker, overview, balanceSheet, 
                incomeStatement, cashFlowStatement, historicalPrice):
        
        self.ticker = ticker
        self.summary = pd.DataFrame(overview)
        self.balSheet = pd.DataFrame(balanceSheet)
        self.incStatement = pd.DataFrame(incomeStatement)
        self.cashFlw = pd.DataFrame(cashFlowStatement)
        self.histPrice = pd.DataFrame(historicalPrice)
 
       
        
class pullEquity:
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
                               self.cashFlow,
                               self.timeSeriesDaily]


   
    async def pull_Data(self,urlA,statement,ticker):
        url = f"https://www.alphavantage.co/query?function={statement}&symbol={ticker}&apikey=5TFQU47K2QUCZVRF"
        urlDailyPrice = f"https://www.alphavantage.co/query?function={statement}&symbol={ticker}&outputsize=full&apikey=5TFQU47K2QUCZVRF"
        
        if(urlA == 1):
            urlA = urlDailyPrice
        elif(urlA == 0):
            urlA = url
        
        async with aio.ClientSession() as session:
            async with session.get(urlA) as response:
                print(response)
                data = await response.json()
                print(data)
                normalizedObj = normalizeData.normalizeClean(data)
                return normalizedObj
    
    async def iterateRequest(self,statement : str):
        if(statement != self.timeSeriesDaily):
            data = pullEquity.pull_Data(self,0,statement,self.ticker)
            return data
            
    async def pull_allStatements(self):
        tasks = [pullEquity.iterateRequest(i) for i in self.attributeArray]
        results = await asyncio.gather(*tasks) 
        equityObj = equitySecurity().__int__(self.ticker,*results) 
        return equityObj
        
                    
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
        
        #elif data is not None:
            #df = pd.json_normalize()
            
            
        else:
            return None
            
        

