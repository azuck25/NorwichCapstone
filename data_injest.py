# data_ingest.py
from database import *
import AV_API_pull as alphaVantageAPI
import asyncio
import aiohttp, pandas, datetime

#Function triggers pulling, formating, and adding for the SP500
def ingest_index(portfolioId: str, sp: str):
    print("Function Triggered")
    session = Session()
    sp_data = normalizeClean(pull_SP500(sp))
    print(sp_data)
    portfolio = session.query(Portfolio).filter_by(portfolioName=portfolioId).first()
    if not portfolio and sp_data is not None:
        print("SP500 data not found adding...")
        portfolio = Stock(ticker=sp)
        session.add(portfolio)
        session.commit()
        sp_data = normalizeClean(pull_SP500(sp))
        #print(sp_data)
        if sp_data is not None:
            for _,row in sp_data.iterrows():
                add_sp = SPindex(ticker=sp,portId=portfolioId, **row)
                session.add(add_sp)
            session.commit()
            session.close()

            return {"status": "success", "ticker": sp}
    elif portfolio:
        return {"status": "data exists"}

    return None

def ingest_tbill(portfolioId: str, ticker: str):
    session = Session()
    portfolio = session.query(Portfolio).filter_by(portfolioName=portfolioId).first()
    print(portfolio)
    if not portfolio:
        print("10Y TBILL data not found adding...")
        tbill_data = normalizeClean(pull_TbilltenY(ticker))
        
        if tbill_data is not None:
            print("Printing TBILL Data")
            print(tbill_data)
            portfolio = Portfolio(portfolioName=portfolioId)
            session.add(portfolio)
            session.commit()
            for _,row in tbill_data.iterrows():
                tbill_obj = TbillData(ticker=ticker,portId=portfolioId,**row)
                session.add(tbill_obj)
                
        session.commit()
        session.close()
    # Else if the stock is found and the function that adds data hasnt been triggered
    # Then delete the corresponding ticker data and recursively call the function to
    # refresh the data
    elif portfolio:
        session.delete(portfolio)
        session.commit()
        ingest_tbill(portfolioId,ticker)
        print("Refreshing T-Bill Data...")
    return None

async def pullEquityData(ticker : str):
    session = Session()
    queryDB = session.query(Stock).filter_by(ticker=ticker).first()
    
    if queryDB is None:
        alphaV = alphaVantageAPI.pullEquity(ticker=ticker)
        equityData = await alphaV.pull_allStatements()
        return equityData
        
               
    else:
        lastRefresh = queryDB.api_queryDate[0]
        callRefresh = bool(lastRefresh.datetime.date < datetime.datetime.now().date)
        
        if(callRefresh):
            alphaV = alphaVantageAPI.pullEquity(ticker=ticker)
            equityData = await alphaV.pull_allStatements()
            return equityData

            
       
        
        # dateUploaded = session.execute(queryDate)
        # print(queryDate)
        # checkDay = bool(dateUploaded.day < datetime.datetime.now().day)
        # checkYear = bool(dateUploaded.year < datetime.datetime.now().year)
        # #if checkDay or checkYear:
            
        
    
async def streamEquityDataToDB(portfolioId: str, ticker: str):
    
    x = 0

    zip_Df = pullEquityData(ticker=ticker)
    
    
    
    
    y = True
    # If stock is not found and the first data frame is not empty
    if not stock and overview is not None:
        print("Stock not found updating entry...")
        print(stock)
        stock = Stock(ticker=ticker, portId=portfolioId, api_queryDate=datetime.datetime.now())
        session.add(stock)
        session.commit()

        if time_series is not None:
            for _,row in time_series.iterrows():
                time_obj = TimeSeriesDaily(ticker=ticker, **row)
                session.add(time_obj)

        # ---- Insert Overview ----
        if overview is not None:
            row = overview.iloc[0].to_dict()
            overview_obj = Overview(ticker=ticker, **row)
            session.add(overview_obj)

        # ---- Insert Balance Sheet ----
        if balance_sheet is not None:
            print("Printing Balance Sheet...", balance_sheet)
            for _, row in balance_sheet.iterrows():
                bs_obj = BalanceSheet(ticker=ticker, **row.to_dict())
                session.add(bs_obj)

        # ---- Insert Income Statement ----
        if income_statement is not None:
            print("Printing Income Statement...", income_statement)
            for _, row in income_statement.iterrows():
                inc_obj = IncomeStatement(ticker=ticker, **row.to_dict())
                session.add(inc_obj)

        # ---- Insert Cash Flow ----
        if cash_flow is not None:
            print("Printing Cash Flow...", cash_flow)
            for _, row in cash_flow.iterrows():
                cf_obj = CashFlow(ticker=ticker, **row.to_dict())
                session.add(cf_obj)

        session.commit()
        session.close()
        x += 1
        print(x)
        return {"status": "success", "ticker": ticker}
    #Else if the stock is found and the function that adds data hasnt been triggered
    #Then delete the corresponding ticker data and recursively call the function to
    #refresh the data

    elif stock and x == 0:
        print("Stock exists, overwriting data to avoid collision")
        session.delete(stock)
        session.commit()
        ingest_stock_data(portfolioId, ticker)
        print("recursive function called")

    else:
        y = False
        return y



def ingest_important_data():
    session = Session()
    top_winners, top_losers, most_traded = normalizeClean(pull_topMovers())
    t = top_winners['ticker'].iloc[0]
    print(t)
    stock = session.query(TopWinners).filter_by(ticker=t).first()
    print(stock)
    if not stock:
        #If the dataframe is not empty
        if top_winners is not None:
            print("Entering into data pipeline")
            #iterate by index, row and add the rows contents
            for _,row in top_winners.iterrows():
                #print("1\n")
                winner_obj = TopWinners(**row)
                session.add(winner_obj)
            for _,row in top_losers.iterrows():
                losers_obj = TopLosers(**row)
                session.add(losers_obj)
            for _,row in most_traded.iterrows():
                mover_obj = MostTraded(**row)
                session.add(mover_obj)

            session.commit()
            session.close()
            return "success"
        else:
            return "failure"
    else:

        print("Data exists...")
        return "success"