# data_ingest.py
from database import *
from AV_API_pull import *

#Function triggers pulling, formating, and adding for the SP500
def ingest_sp5(sp: str):
    print("Function Triggered")
    session = Session()
    sp_data = normalizeClean(pull_SP500(sp))
    print(sp_data)
    stock = session.query(Stock).filter_by(ticker=sp).first()
    if not stock and sp_data is not None:
        print("SP500 data not found adding...")
        stock = Stock(ticker=sp)
        session.add(stock)
        session.commit()
        sp_data = normalizeClean(pull_SP500(sp))
        #print(sp_data)
        if sp_data is not None:
            for _,row in sp_data.iterrows():
                add_sp = SPindex(ticker=sp, **row)
                session.add(add_sp)
            session.commit()
            session.close()

            return {"status": "success", "ticker": sp}
    elif stock:
        return {"status": "data exists"}

    return None

def ingest_tbill(ticker: str):
    session = Session()
    stock = session.query(Stock).filter_by(ticker=ticker).first()
    if not stock:
        tbill_data = normalizeClean(pull_TbilltenY(ticker))
        print("TBILL data not found adding...")

        if tbill_data is not None:
            stock = Stock(ticker=ticker)
            session.add(stock)
            session.commit()
            for _,row in tbill_data.iterrows():
                tbill_obj = TbillData(ticker=ticker,**row)
                session.add(tbill_obj)
        session.commit()
        session.close()
    # Else if the stock is found and the function that adds data hasnt been triggered
    # Then delete the corresponding ticker data and recursively call the function to
    # refresh the data
    elif stock:
        session.delete(stock)
        session.commit()
        ingest_tbill(ticker)
        print("recursive function call updates Tbill data...")
    return None

def ingest_stock_data(ticker: str):
    session = Session()
    x = 0
    # Ensure stock record exists
    stock = session.query(Stock).filter_by(ticker=ticker).first()
    # Pull and Normalize Data
    overview = normalizeClean(pull_Overview(ticker))
    balance_sheet = normalizeClean(pull_balSheet(ticker))
    income_statement = normalizeClean(pull_incState(ticker))
    cash_flow = normalizeClean(pull_cashFlow(ticker))
    time_series = normalizeClean(pull_timeSeriesPriceDaily(ticker))
    y = True
    # If stock is not found and the first data frame is not empty
    if not stock and overview is not None:
        print("Stock not found updating entry...")
        print(stock)
        stock = Stock(ticker=ticker)
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
        ingest_stock_data(ticker)
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