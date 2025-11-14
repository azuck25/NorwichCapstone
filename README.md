# NorwichCapstone
Backend software to power frontend software through retool. 
System Description

Frontend

•	Our user interface acts as a data-visualization tool for equity instruments. On the first page we have a portfolio that our users can build by entering a ticker representing an equity instrument. By entering a ticker, the user will trigger an API POST method calling data retrieval, formatting, and database commit functions. When a successful API POST is made the frontend will execute DB queries for the corresponding ticker retrieving the data and populating the table. In addition to the portfolio, we have two graphs which can compare the tickers price history in the market to the SP500’s price history. Next to the graphs we have a snapshot of the most traded and most gaining stocks. This gives us insight into where investments are being placed and which stocks are rising the fastest. If our users want better insight into an equity instrument, then by double clicking on a row in the portfolio table the user is taken to page 2. 

•	On page 2 specific details are displayed following the click on the equity instrument. The user can see the last closing price and the performance in the market at that time. By selecting a financial statement for the stock the user can see the statements history by quarter. If a user has questions about what a metric means or how to conduct further analysis of the stock a LLM component provided by retool exists to answer questions. 
Backend

•	The backend software supports the frontend by creating a database, formatting the data, and adding the data to the database. Once an API request is received the ingestion function for equity instruments is received. We then retrieve our financial data from Alpha Vantage API and normalize the data by using Panda’s modules. The data is then committed to the database. To host our API we use a custom Ngrok URL and then run the application over the uvicorn module making the backend accessible from Retool. Our database is also made accessible by forwarding our localhost:3306 service to a TCP Ngrok domain.



Context Diagram

•	The following diagram describes how the different components of the data visualization software communicate. Describing the data's path as it flows through the software and becomes refined for visualization on retool frontend.
<img width="975" height="1134" alt="image" src="https://github.com/user-attachments/assets/c9b889f3-3fe1-4743-90cb-d3256c148855" />

Functional Decomposition Diagram

•	Here we describe how the main.py functions are implemented and triggered from the frontend software.
<img width="572" height="1073" alt="image" src="https://github.com/user-attachments/assets/ff8d7ce5-38ac-4ad2-b137-33265e4aaf65" />

<img width="896" height="960" alt="image" src="https://github.com/user-attachments/assets/5ee553d6-2498-4448-93ba-0b09696b1103" />


Database ERD Diagram

•	Database relational diagram with primary keys. In this software one stock has many statements ordered in a timeseries within the dbms.
<img width="975" height="1025" alt="image" src="https://github.com/user-attachments/assets/989f6044-83a8-4a40-b16b-62663118eeec" />


Retool Frontend in Action

https://github.com/user-attachments/assets/fa48e382-4f1f-400e-91f7-7860b7d704c3


