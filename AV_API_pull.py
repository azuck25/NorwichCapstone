import requests
import numpy as np
import pandas as pd
import json
import re
from io import StringIO
from datetime import date

apiKey = 'NNWS39IGZJ1O7OZM'
balanceSheet = "BALANCE_SHEET"
incomeStatement = "INCOME_STATEMENT"
cashFlow = "CASH_FLOW"

url = 'https://www.alphavantage.co/query?function='
function = 'TREASURY_YIELD'
function2 = 'TIME_SERIES_DAILY'
function3 = 'OVERVIEW'
function4 = 'CASH_FLOW'
function5 = 'TOP_GAINERS_LOSERS'

#symbol1 = "IBM"
#symbol3 = "SPY"

def pull_Overview(symbol):
    overview = requests.get(url + function3 + '&symbol=' + symbol + '&apikey=' + apiKey)
    data_overview = overview.json()
    return data_overview
def pull_balSheet(symbol):
    balSheet = requests.get(url + balanceSheet + '&symbol=' + symbol + '&apikey=' + apiKey)
    data_balSheet = balSheet.json()
    return data_balSheet
def pull_incState(symbol):
    incState = requests.get(url + incomeStatement + '&symbol=' + symbol + '&apikey=' + apiKey)
    data_incState = incState.json()
    return data_incState
def pull_TbilltenY(symbol):
    TbilltenY = requests.get(url + function + '&interval=monthly&maturity=10year' + '&apikey=' + apiKey)
    data_TbilltenY = TbilltenY.json()
    return data_TbilltenY
def pull_timeSeriesPriceDaily(symbol):
    timeSeriesPriceDaily = requests.get(url + function2 + '&symbol=' + symbol + '&apikey=' + apiKey + "&datatype=csv&outputsize=full")
    data_dailyTimeSeries = pd.read_csv(StringIO(timeSeriesPriceDaily.text))
    return data_dailyTimeSeries
def pull_SP500(symbol):
    SnP500_meanR = requests.get(url + function2 + '&symbol=' + symbol + '&apikey=' + apiKey + "&datatype=csv&outputsize=full")
    data_SP500 = pd.read_csv(StringIO(SnP500_meanR.text))
    return data_SP500
def pull_cashFlow(symbol):
    cashFlow = requests.get(url + function4 + '&symbol=' + symbol + '&apikey=' + apiKey)
    data_cashFlow = cashFlow.json()
    return data_cashFlow
def pull_topMovers():
    topMovement = requests.get(url + function5 + '&symbol=' + '&apikey=' + apiKey)
    data_topMovement = topMovement.json()
    return data_topMovement


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

        df = set_datatype(df)
        df2 = set_datatype(df2)
        df3 = set_datatype(df3)

        return df, df2, df3

    elif (isinstance(data, pd.DataFrame) and "close" in data.columns):
        data.drop(columns=['open', 'high', 'low', 'volume'], inplace=True)

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

    else:
        return None