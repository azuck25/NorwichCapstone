# NorwichCapstone
Backend software to power frontend software through retool. 
System Description
Frontend
•	Our user interface acts as a data-visualization tool for equity instruments. On the first page we have a portfolio that our users can build by entering a ticker representing an equity instrument. By entering a ticker, the user will trigger an API POST method calling data retrieval, formatting, and database commit functions. When a successful API POST is made the frontend will execute DB queries for the corresponding ticker retrieving the data and populating the table. In addition to the portfolio, we have two graphs which can compare the tickers price history in the market to the SP500’s price history. Next to the graphs we have a snapshot of the most traded and most gaining stocks. This gives us insight into where investments are being placed and which stocks are rising the fastest. If our users want better insight into an equity instrument, then by double clicking on a row in the portfolio table the user is taken to page 2. 
•	On page 2 specific details are displayed following the click on the equity instrument. The user can see the last closing price and the performance in the market at that time. By selecting a financial statement for the stock the user can see the statements history by quarter. If a user has questions about what a metric means or how to conduct further analysis of the stock a LLM component provided by retool exists to answer questions. 
Backend
•	The backend software supports the frontend by creating a database, formatting the data, and adding the data to the database. Once an API request is received the ingestion function for equity instruments is received. We then retrieve our financial data from Alpha Vantage API and normalize the data by using Panda’s modules. The data is then committed to the database. To host our API we use a custom Ngrok URL and then run the application over the uvicorn module making the backend accessible from Retool. Our database is also made accessible by forwarding our localhost:3306 service to a TCP Ngrok domain.


Context Diagram
<img width="975" height="1134" alt="image" src="https://github.com/user-attachments/assets/c9b889f3-3fe1-4743-90cb-d3256c148855" />

System Functions
Main.py
from database import initialize_database,Base,engine  # Optional: one-time DB setup
from pyngrok import ngrok
import uvicorn, subprocess

ngrok.set_auth_token("2aPOIu0sWqUH5ijSYf5xr2NFTzD_4Rmhn8BNNkpD4CzGCePGG")

def main():
    #First, we initialize the database, mapping the classes to the database schema
    print("Initializing database...")
    initialize_database()
    # Start a ngrok tunnel to the local FastAPI app
    public_url = ngrok.connect(8000,proto="http",domain="ingestsymbol.ngrok.pro")
    # Run FastAPI app from data_injest.py
    print(f"App is live at: {public_url}")
    uvicorn.run("db_commit:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
•	From the start of the program in main.py we call our database initialization function to create the database. Which will be explained in depth.
o	We then host the database over a public facing TCP connection with ngrok by entering the following command in the terminal which will forward traffic from our localhost service running on 3306 to the Ngrok domain
o	(.venv) PS C:\Users\zuck1\PycharmProjects\capstone_backend> ngrok tcp --remote-addr=5.tcp.ngrok.io:23276 3306
•	Next our backend is exposed to the public facing internet through a custom Ngrok domain > https://ingestsymbol.ngrok.pro/
•	Uvicorn allows our Fast API functions to be access by the frontend software made accessible through the above domain

Functional Decomposition Diagram
<img width="572" height="1073" alt="image" src="https://github.com/user-attachments/assets/5981f526-baa3-43f4-a711-356c0aab6005" />

System Functions
Database Creation and Database Schema 
database.py
•	We create a MySQL database using the following modules
o	Sqlalchemy
	Sqlalchemy.ext.delcarative
	Sqlalchemy.orm
	We use these functions to conduct Object Relational Mapping in Python.
o	Dotenv
	We use this module to create a environment file which contains the values of the user, password, host, port, and db name which are then set to variables needed to form a connection to the db
o	Pymysql
	Python module used to connect to the MySQL database
o	Os
	Module used for basic operating system commands
o	Ngrok
	To make the database accessible to the front end we use ngrok’s tunneling service to host the database over TCP connection on the public facing internet. All traffic from this TCP address is forwarded to the hosting machines localhost at port 3306
•	Database Creation
•	Base = declarative_base()
o	Declarative base function allows for automatic mapping and creation of tables by defining the tables attributes.
•	class Stock(Base):
    __tablename__ = 'stocks'
    ticker = Column(String(20), primary_key=True)

    overview = relationship("Overview", back_populates="stock", cascade="all, delete-orphan")
    balance_sheet = relationship("BalanceSheet", back_populates="stock", cascade="all, delete-orphan")
    income_statement = relationship("IncomeStatement", back_populates="stock", cascade="all, delete-orphan")
    cash_flow = relationship("CashFlow", back_populates="stock", cascade="all, delete-orphan")
    spindex = relationship("SPindex", back_populates="stock", cascade="all, delete-orphan")
    timeseries_daily = relationship("TimeSeriesDaily", back_populates="stock", cascade="all, delete-orphan")
    tbills = relationship("TbillData", back_populates="stock", cascade="all, delete-orphan")
o	We define the parent table for equity instruments by declaring the primary key as the ticker or symbol for the instrument
o	Relationships between the child tables are then set as the ticker back populates into the parent table. The primary key for the child tables is an integer value which increments as data flows into the table. A foreign key is used to tie the relationship back to the parent table Stock
•	.ENV 
o	This file is used to specify the DB’s environment variables. We leave the .env in the same directory as the database generator file so that we can access the file to set the variables with the code below.
o	DB_USER = os.getenv("FIN_DB_USER", "your_user")
DB_PASSWORD = os.getenv("FIN_DB_PASSWORD", "your_password")
DB_HOST = os.getenv("FIN_DB_HOST", "localhost")
DB_PORT = os.getenv("FIN_DB_PORT", "3306")
DB_NAME = os.getenv("FIN_DB_NAME", "fin_data")
•	Pymysql
o	We then use the env variables which have been set to test the connection to the DB
•	try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=int(DB_PORT),
        charset='utf8mb4',
        autocommit=True
    )
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    connection.close()
    print(f"Verified or created MySQL database: {DB_NAME}")
except Exception as e:
    print(f"Error creating database: {e}")
    raise
o	DB creation
•	DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
	We define the URL for the database using the environment variables and setting the character type
	The engine is then created and binds to the session maker to create an accessible session to add, commit, and delete data from the DB using Python.

