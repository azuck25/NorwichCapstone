import AV_API_pull as av
import data_injest as dataStream
import asyncio, aiohttp
import pandas as pd

async def main():
    tickers = ["IBM","A", "NVDA"]
    results = [dataStream.pullEquityData(i) for i in tickers]
    data = await asyncio.gather(*results)
    
    
    
        
asyncio.run(main())


