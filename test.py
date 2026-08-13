import time

from pyarrow import time32

import AV_API_pull as av
import data_injest as dataStream
import asyncio, aiohttp
import pandas as pd

async def main():

    #while True:
        #try:
            semaphore = asyncio.Semaphore(30)

            file = open("tickers_.csv", encoding="UTF-8-SIG")

            async with semaphore:
                #file = ['SNAP','VALE','BMY','SIRI',]
                results =  {str(i).strip():await dataStream.pull_equity_data(str(i).strip()) for i in file }


            data = dict(zip(results.keys(),results.values()))
            print(data)

        #     break
        # except Exception as e:
        #     print("Error : ", e)
        #     time.sleep(60)
asyncio.run(main())


