import requests
import statistics
import time
import sys

INPUT_FILE_PATH = input("Input file path:\n")
KEY = input("Key: \n")
MAX_CALLS = 500
NUM_OF_URLS = 3
NUM_OF_STOCKS = int(input("How many stocks?\n"))
QUARTERS_TO_CHECK = int(input("How many quarters to check?\n"))
PORTION_SIZE = int(MAX_CALLS/NUM_OF_URLS)
PORTION = 0

OUT_OF_CALLS = False

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
    temp = f.readline()
    stocks.append(temp)
f.close()

# Resets and writes the heading
if PORTION == 1:
    for q in range(QUARTERS_TO_CHECK):
        r = open("Q{}.csv".format(q+1), "w")
        r.write("Ticker,Price,Gross Profit,Net Income,Shareholder Equity,Liabilities,Shares Outstanding,Total Assests\n")
        r.close()

for i in range((PORTION-1)*PORTION_SIZE, LIMIT):
    s = stocks[i]
    monthlyURL = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={}&apikey={}".format(s, KEY)
    balanceURL = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={}&apikey={}".format(s, KEY)
    incomeURL = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={}&apikey={}".format(s, KEY)
    # overviewURL = "https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}".format(s, KEY)
    # cashURL = "https://www.alphavantage.co/query?function=CASH_FLOW&symbol={}&apikey={}".format(s, KEY)

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
                out = open("Q{}.csv".format(q+1), "a")
                out.write("{},N/A,N/A,N/A,N/A,N/A,N/A,N/A\n".format(s))
                out.close()
                continue
        except KeyError:
            OUT_OF_CALLS = True
            break
        
        completed = False
        d = 31
        price = 0

        # Sometimes the last day of the month isn't a trading day, so it has no price
        # This makes sure that we just get the day closest to the month end and not an error
        while (not completed) and (d > 0):
            try:
                price = monthlyData["Monthly Adjusted Time Series"][m]["5. adjusted close"]
                completed = True
            except KeyError:
                t = m.split("-")
                if t[0] == "2021" and int(t[1]) > 3:  # Apparently some idiot wrote 2021-12-31 as the date for their quarterly reports
                    t[0] = "2020"
                m = "{}-{}-{}".format(t[0], t[1], d)
                d -= 1
                completed = False
        if not completed:    # So now I do this just in case something bad like that happens
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

        out = open("Q{}.csv".format(q+1), "a")
        out.write("{},{},{},{},{},{},{},{}\n".format(
            s,
            price,
            profit,
            income,
            equity,
            liabilities,
            shares,
            assets
        ))
        out.close()
    
    if OUT_OF_CALLS:
        break
    
    spaces = " "*(8-len(s.TICKER))
    num = i+1-(PORTION-1)*PORTION_SIZE
    den = LIMIT-(PORTION-1)*PORTION_SIZE
    percent = round(num/den*100, 2)
    print("data retrival complete for: {}{}{}%    ({}/{})".format(s.TICKER, spaces, percent, num, den), end='\n', flush=True)  # Adding flush ensures it doesn't get stuck buffering sometimes.

if OUT_OF_CALLS:
    print("--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---")
    print("You have run out of calls...")
    print("Please try again tomorrow without using any calls ahead of time.")
