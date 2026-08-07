import AV_API_pull as av
import data_injest as dataStream
import asyncio, aiohttp


async def main():
    tickers = ["IBM","A", "NVDA"]
    tasks = [dataStream.pullEquityData(t) for t in tickers]
    data = await asyncio.gather(*tasks)
    
    for i in data:
        print(i)
        
        
asyncio.run(main())


