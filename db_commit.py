# data_ingest.py
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data_injest import ingest_stock_data, ingest_sp5, ingest_tbill, ingest_important_data
from fastapi import FastAPI, HTTPException
from financial_models import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your Retool domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test_api():
    return {"message": "API is running"}

@app.post("/ingest/refresh_movers")
def ingest_refresh_movers():
    try:
        result = ingest_important_data()
        print(f"message : {result}")
    except Exception as e3:
        print(f"message : error in data pipeline")
        raise HTTPException(status_code=500, detail=str(e3))


@app.post("/ingest/{ticker}")
def ingest_ticker(ticker: str):
    spy_check = "SPY"
    tbill_check = "US10Y"

    try:

        if spy_check in ticker:
            result = ingest_sp5(ticker.upper())
            print(f"Success : {ticker} data commited to database")
        elif tbill_check in ticker:
            result = ingest_tbill(ticker.upper())
            print(f"Success : {ticker} data commited to database")
        else:
            result = ingest_stock_data(ticker.upper())
            if result is True:
                print(f"Success : {ticker} data commited to database")
            elif result is False:
                raise HTTPException(status_code=404, detail="Invalid ticker")

    except Exception as e1:
        print(e1)
        raise HTTPException(status_code=500, detail=str(e1))

    print(f"Starting modeling software for : {ticker}")
    #interact(ticker.upper())


    #trigger fin modeling here

