import requests
import statistics
import time
import sys

class stock:
    TICKER = ""
    COMPANY_NAME = ""
    INDUSTRY = ""

    def __init__(self, t, n, i):
        self.TICKER = t
        self.COMPANY_NAME = n
        self.INDUSTRY = i

VERSION = int(sys.argv[1])
INPUT_FILE_PATH = input("Input file path:\n")
KEY = input("Key: \n")
NUM_OF_URLS = 3
NUM_OF_STOCKS = int(input("How many stocks?\n"))
QUARTERS_TO_CHECK = int(input("How many quarters to check?\n"))
PORTION_SIZE = int(500/NUM_OF_URLS)
PORTION = 0

if VERSION == 1:
    PORTION_SIZE = NUM_OF_STOCKS

if NUM_OF_STOCKS > PORTION_SIZE:
    if PORTION_SIZE*2 >= NUM_OF_STOCKS:
        PORTION = int(input("Which portion of {}? (1 = stocks 1-{}, 2 = stocks {}-{})\n".format(PORTION_SIZE, PORTION_SIZE, PORTION_SIZE+1, NUM_OF_STOCKS)))
    else:
        PORTION = int(input("Which portion of {}? (1 = stocks 1-{}, 2 = stocks {}-{}, ... , {} = stocks {}-{})\n".format(
            PORTION_SIZE, PORTION_SIZE, PORTION_SIZE+1, PORTION_SIZE*2, int(NUM_OF_STOCKS/PORTION_SIZE)+1, int(NUM_OF_STOCKS/PORTION_SIZE)*PORTION_SIZE+1, NUM_OF_STOCKS)))
else:
    PORTION = 1

LIMIT = PORTION*PORTION_SIZE

if LIMIT > NUM_OF_STOCKS:
    LIMIT = NUM_OF_STOCKS

# Read in the stock info
stocks = []
f = open(INPUT_FILE_PATH, "r")
for i in range(NUM_OF_STOCKS):
    temp = f.readline().split(",")
    stocks.append(stock(temp[0], temp[1], temp[2]))
f.close()

# Resets and writes the heading
if PORTION == 1:
    for q in range(QUARTERS_TO_CHECK):
        r = open("2021_test_data_Q{}.csv".format(q+1), "w")
        r.write("Ticker,Company Name,Sector,Price,Gross Profit,Net Income,Shareholder Equity,Liabilities,Shares Outstanding,Total Assests\n")
        r.close()

for i in range((PORTION-1)*PORTION_SIZE, LIMIT):
    s = stocks[i]
    balanceURL = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={}&apikey={}".format(s.TICKER, KEY)
    incomeURL = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={}&apikey={}".format(s.TICKER, KEY)
    # overviewURL = "https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}".format(s.TICKER, KEY)
    # cashURL = "https://www.alphavantage.co/query?function=CASH_FLOW&symbol={}&apikey={}".format(s.TICKER, KEY)
    monthlyURL = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={}&apikey={}".format(s.TICKER, KEY)

    response = requests.get(balanceURL)
    balanceData = response.json()
    time.sleep(13)  # I use 13 seconds just to be safe
    response = requests.get(incomeURL)
    incomeData = response.json()
    time.sleep(13)
    response = requests.get(monthlyURL)
    monthlyData = response.json()
    time.sleep(13)

    # response = requests.get(cashURL)
    # cashData = response.json()
    # time.sleep(13)
    # response = requests.get(overviewURL)
    # overviewData = response.json()
    # time.sleep(13)

    for q in range(QUARTERS_TO_CHECK):
        # Make sure the stock existed back then
        try:
            m = balanceData["quarterlyReports"][q]["fiscalDateEnding"]
        except IndexError:
            try:
                m = incomeData["quarterlyReports"][q]["fiscalDateEnding"]
            except IndexError:
                out = open("d:/Programs/Python programs/Stock_Tools/2021_test_data_Q{}.csv".format(q+1), "a")
                out.write("{},{},{},N/A,N/A,N/A,N/A,N/A,N/A,N/A\n".format(
                    s.TICKER,
                    s.COMPANY_NAME,
                    s.INDUSTRY
                ))
                out.close()
                continue
        
        completed = False
        d = 31
        price = 0

        # Sometimes the last day of the month isn't a trading day, so it has no price
        # This makes sure that we just get the day closest to the month end and not an error
        while (not completed) and (d > 0):
            try:
                price = monthlyData["Monthly Adjusted Time Series"][m]["4. close"]
                completed = True
            except KeyError:
                t = m.split("-")
                if t[0] == "2021" and int(t[1]) > 3:  # Apparently some idiot wrote 2021-12-31 as the date for their quarterly reports
                    t[0] = "2020"
                m = "{}-{}-{}".format(t[0], t[1], d)
                d -= 1
                completed = False
        if not completed:  # So now I do this just in case something bad like that happens
            price = "ERROR"
        
        # For some reason, some quarters have an income statement but not a balance sheet
        try:
            profit = incomeData["quarterlyReports"][q]["grossProfit"]
        except:
            profit = "N/A"
        try:
            income = incomeData["quarterlyReports"][q]["netIncome"]
        except:
            income = "N/A"
        try:
            equity = balanceData["quarterlyReports"][q]["totalShareholderEquity"]
        except:
            equity = "N/A"
        try:
            liabilities = balanceData["quarterlyReports"][q]["totalLiabilities"]
        except:
            liabilities = "N/A"
        try:
            shares = balanceData["quarterlyReports"][q]["commonStockSharesOutstanding"]
        except:
            shares = "N/A"
        try:
            assets = balanceData["quarterlyReports"][q]["totalAssets"]
        except:
            assets = "N/A"

        out = open("d:/Programs/Python programs/Stock_Tools/2021_test_data_Q{}.csv".format(q+1), "a")
        out.write("{},{},{},{},{},{},{},{},{},{}\n".format(
            s.TICKER,
            s.COMPANY_NAME,
            s.INDUSTRY,
            price,
            profit,
            income,
            equity,
            liabilities,
            shares,
            assets
        ))
        out.close()
        
    spaces = " "*(8-len(s.TICKER))
    percent = round((i+1)/LIMIT, 4)*100
    print("data retrival complete for: {}{}{}%    ({}/{})".format(s.TICKER, spaces, percent, i+1, LIMIT))
