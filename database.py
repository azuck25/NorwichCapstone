from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import pymysql
import os
from pathlib import Path

load_dotenv()

Base = declarative_base()

# --- Models ---
class Stock(Base):
    __tablename__ = 'stocks'
    ticker = Column(String(20), primary_key=True)

    overview = relationship("Overview", back_populates="stock", cascade="all, delete-orphan")
    balance_sheet = relationship("BalanceSheet", back_populates="stock", cascade="all, delete-orphan")
    income_statement = relationship("IncomeStatement", back_populates="stock", cascade="all, delete-orphan")
    cash_flow = relationship("CashFlow", back_populates="stock", cascade="all, delete-orphan")
    spindex = relationship("SPindex", back_populates="stock", cascade="all, delete-orphan")
    timeseries_daily = relationship("TimeSeriesDaily", back_populates="stock", cascade="all, delete-orphan")
    tbills = relationship("TbillData", back_populates="stock", cascade="all, delete-orphan")

class TbillData(Base):
    __tablename__ = 'tbills'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(20), ForeignKey('stocks.ticker', ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)

    stock = relationship("Stock", back_populates="tbills")

class TimeSeriesDaily(Base):
    __tablename__ = 'timeseries_daily'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(20),ForeignKey('stocks.ticker', ondelete="CASCADE"), nullable=False)

    timestamp = Column(Date, nullable=False)
    close = Column(Float, nullable=False)

    stock = relationship("Stock", back_populates="timeseries_daily")

class SPindex(Base):
    __tablename__ = 'spindex'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), ForeignKey('stocks.ticker', ondelete="CASCADE"), nullable=False)
    timestamp = Column(Date,nullable=False)
    close = Column(Float, nullable=False)

    stock = relationship("Stock", back_populates="spindex")

class Overview(Base):
    __tablename__ = 'overview'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), ForeignKey('stocks.ticker', ondelete="CASCADE"), nullable=False)

    Symbol = Column(String(20))
    AssetType = Column(String(50))
    Name = Column(String(255))
    Description = Column(String(2000))
    CIK = Column(String(20))
    Exchange = Column(String(50))
    Currency = Column(String(10))
    Country = Column(String(50))
    Sector = Column(String(50))
    Industry = Column(String(100))
    Address = Column(String(255))
    OfficialSite = Column(String(255))
    FiscalYearEnd = Column(String(20))
    LatestQuarter = Column(String(20))

    MarketCapitalization = Column(BigInteger)
    EBITDA = Column(BigInteger)
    PERatio = Column(Float)
    PEGRatio = Column(Float)
    BookValue = Column(Float)
    DividendPerShare = Column(Float)
    DividendYield = Column(Float)
    EPS = Column(Float)
    RevenuePerShareTTM = Column(Float)
    ProfitMargin = Column(Float)
    OperatingMarginTTM = Column(Float)
    ReturnOnAssetsTTM = Column(Float)
    ReturnOnEquityTTM = Column(Float)
    RevenueTTM = Column(BigInteger)
    GrossProfitTTM = Column(BigInteger)
    DilutedEPSTTM = Column(Float)
    QuarterlyEarningsGrowthYOY = Column(Float)
    QuarterlyRevenueGrowthYOY = Column(Float)

    AnalystTargetPrice = Column(Float)
    AnalystRatingStrongBuy = Column(Integer)
    AnalystRatingBuy = Column(Integer)
    AnalystRatingHold = Column(Integer)
    AnalystRatingSell = Column(Integer)
    AnalystRatingStrongSell = Column(Integer)

    TrailingPE = Column(Float)
    ForwardPE = Column(Float)
    PriceToSalesRatioTTM = Column(Float)
    PriceToBookRatio = Column(Float)
    EVToRevenue = Column(Float)
    EVToEBITDA = Column(Float)
    Beta = Column(Float)

    _52WeekHigh = Column(Float)
    _52WeekLow = Column(Float)
    _50DayMovingAverage = Column(Float)
    _200DayMovingAverage = Column(Float)

    SharesOutstanding = Column(BigInteger)
    SharesFloat = Column(BigInteger)
    PercentInsiders = Column(Float)
    PercentInstitutions = Column(Float)
    DividendDate = Column(String(20))
    ExDividendDate = Column(String(20))

    stock = relationship("Stock", back_populates="overview")

class BalanceSheet(Base):
    __tablename__ = 'balance_sheet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), ForeignKey('stocks.ticker', ondelete="CASCADE"), nullable=False)
    fiscalDateEnding = Column(Date, nullable=False)

    totalAssets = Column(Float)
    totalCurrentAssets = Column(Float)
    cashAndCashEquivalentsAtCarryingValue = Column(Float)
    cashAndShortTermInvestments = Column(Float)
    inventory = Column(Float)
    currentNetReceivables = Column(Float)
    totalNonCurrentAssets = Column(Float)
    propertyPlantEquipment = Column(Float)
    accumulatedDepreciationAmortizationPPE = Column(Float)
    intangibleAssets = Column(Float)
    intangibleAssetsExcludingGoodwill = Column(Float)
    goodwill = Column(Float)
    investments = Column(Float)
    longTermInvestments = Column(Float)
    shortTermInvestments = Column(Float)
    otherCurrentAssets = Column(Float)
    otherNonCurrentAssets = Column(Float)
    totalLiabilities = Column(Float)
    totalCurrentLiabilities = Column(Float)
    currentAccountsPayable = Column(Float)
    deferredRevenue = Column(Float)
    currentDebt = Column(Float)
    shortTermDebt = Column(Float)
    totalNonCurrentLiabilities = Column(Float)
    capitalLeaseObligations = Column(Float)
    longTermDebt = Column(Float)
    currentLongTermDebt = Column(Float)
    longTermDebtNoncurrent = Column(Float)
    shortLongTermDebtTotal = Column(Float)
    otherCurrentLiabilities = Column(Float)
    otherNonCurrentLiabilities = Column(Float)
    totalShareholderEquity = Column(Float)
    treasuryStock = Column(Float)
    retainedEarnings = Column(Float)
    commonStock = Column(Float)
    commonStockSharesOutstanding = Column(Float)

    stock = relationship("Stock", back_populates="balance_sheet")

class IncomeStatement(Base):
    __tablename__ = 'income_statement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), ForeignKey('stocks.ticker', ondelete="CASCADE"), nullable=False)
    fiscalDateEnding = Column(Date, nullable=False)

    grossProfit = Column(Float)
    totalRevenue = Column(Float)
    costOfRevenue = Column(Float)
    costofGoodsAndServicesSold = Column(Float)
    operatingIncome = Column(Float)
    sellingGeneralAndAdministrative = Column(Float)
    researchAndDevelopment = Column(Float)
    operatingExpenses = Column(Float)
    investmentIncomeNet = Column(Float)
    netInterestIncome = Column(Float)
    interestIncome = Column(Float)
    interestExpense = Column(Float)
    nonInterestIncome = Column(Float)
    otherNonOperatingIncome = Column(Float)
    depreciation = Column(Float)
    depreciationAndAmortization = Column(Float)
    incomeBeforeTax = Column(Float)
    incomeTaxExpense = Column(Float)
    interestAndDebtExpense = Column(Float)
    netIncomeFromContinuingOperations = Column(Float)
    comprehensiveIncomeNetOfTax = Column(Float)
    ebit = Column(Float)
    ebitda = Column(Float)
    netIncome = Column(Float)

    stock = relationship("Stock", back_populates="income_statement")

class CashFlow(Base):
    __tablename__ = 'cash_flow'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), ForeignKey('stocks.ticker', ondelete="CASCADE"), nullable=False)
    fiscalDateEnding = Column(Date, nullable=False)

    operatingCashflow = Column(Float)
    paymentsForOperatingActivities = Column(Float)
    proceedsFromOperatingActivities = Column(Float)
    changeInOperatingLiabilities = Column(Float)
    changeInOperatingAssets = Column(Float)
    depreciationDepletionAndAmortization = Column(Float)
    capitalExpenditures = Column(Float)
    changeInReceivables = Column(Float)
    changeInInventory = Column(Float)
    profitLoss = Column(Float)
    cashflowFromInvestment = Column(Float)
    cashflowFromFinancing = Column(Float)
    proceedsFromRepaymentsOfShortTermDebt = Column(Float)
    paymentsForRepurchaseOfCommonStock = Column(Float)
    paymentsForRepurchaseOfEquity = Column(Float)
    paymentsForRepurchaseOfPreferredStock = Column(Float)
    dividendPayout = Column(Float)
    dividendPayoutCommonStock = Column(Float)
    dividendPayoutPreferredStock = Column(Float)
    proceedsFromIssuanceOfCommonStock = Column(Float)
    proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet = Column(Float)
    proceedsFromIssuanceOfPreferredStock = Column(Float)
    proceedsFromRepurchaseOfEquity = Column(Float)
    proceedsFromSaleOfTreasuryStock = Column(Float)
    changeInCashAndCashEquivalents = Column(Float)
    changeInExchangeRate = Column(Float)
    netIncome = Column(Float)

    stock = relationship("Stock", back_populates="cash_flow")

class TopWinners(Base):
    __tablename__ = 'top_winners'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    change_amount = Column(Float, nullable=False)
    change_percentage = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)



class TopLosers(Base):
    __tablename__ = 'top_losers'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    change_amount = Column(Float, nullable=False)
    change_percentage = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)



class MostTraded(Base):
    __tablename__ = 'most_traded'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    change_amount = Column(Float, nullable=False)
    change_percentage = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)



# --- DB Connection Setup ---
DB_USER = os.getenv("FIN_DB_USER", "your_user")
DB_PASSWORD = os.getenv("FIN_DB_PASSWORD", "your_password")
DB_HOST = os.getenv("FIN_DB_HOST", "localhost")
DB_PORT = os.getenv("FIN_DB_PORT", "3306")
DB_NAME = os.getenv("FIN_DB_NAME", "fin_data")

# Ensure the database exists
try:
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

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def initialize_database():
    Base.metadata.create_all(engine)
    print(f"MySQL database '{DB_NAME}' initialized at {DB_HOST}:{DB_PORT}")