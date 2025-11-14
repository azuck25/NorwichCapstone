from AV_API_pull import balanceSheet
from database import *
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd


class EquityInstrument:
    def __init__(self, ticker, balancesheet, incomeState, CashFlowStatements):
        self.ticker = ticker
        self.balanceSheet = balancesheet
        self.incomeState = incomeState
        self.CashFlowStatements = CashFlowStatements
        
class SP500data:
    def __init__(self, ticker, daily):
        self.ticker = ticker
        self.daily = daily

class tbillData:
    def __init__(self, ticker, tenYear):
        self.ticker = ticker
        self.tenYear = tenYear


def query_statements(ticker: str):
    EquityInstrument.ticker = ticker
    balancesheetQ = f"SELECT * FROM fin_data.balance_sheet WHERE ticker = '{ticker}'"
    incomeStateQ = f"SELECT * FROM fin_data.income_statement WHERE ticker = '{ticker}'"
    cashFlowStateQ = f"SELECT * FROM fin_data.cash_flow WHERE ticker = '{ticker}'"

    EquityObj = EquityInstrument(ticker,pd.read_sql(balancesheetQ, con=engine),
                            pd.read_sql(incomeStateQ, con=engine),
                            pd.read_sql(cashFlowStateQ,con=engine))
    return EquityObj

def query_tbills(ticker: str):
    tbillData.ticker = ticker
    tbillQ = f"SELECT * FROM fin_data.tbills WHERE ticker = '{ticker}'"
    tbill_obj = tbillData(ticker, pd.read_sql(tbillQ, con=engine))
    return tbill_obj

def query_sp(ticker: str):
    SP500data.ticker = ticker
    SP500IndexQ = "SELECT * FROM fin_data.spindex"
    SPobj = SP500data(ticker, pd.read_sql(SP500IndexQ,con=engine))
    return SPobj

def basic_model(ticker: str):
    equity_obj = query_statements(ticker)
    sp_obj = query_sp("SPY")
    tbill_obj = query_tbills("US10Y")

    tbill_df = tbill_obj.tenYear
    tbill_df['date'] = pd.to_datetime(tbill_df['date'])
    tbill_df.set_index('date',inplace=True)
    print(type(tbill_df))
    print(tbill_df.index.is_monotonic_decreasing)
    tbill_df = tbill_df.sort_index(ascending=True)
    tbill_10y = pd.DataFrame(tbill_df['value'].loc['2014-06-01':'2025-05-01'])









basic_model("IBM")


