# Stock-data-collector-2021
This is the program we use to gather data with Alpha Vantage's API service.
Alpha Vantage provides free price and fundamental data, but you are only allowed 5 calls per minute (1 call per 12 sec.)
You are also only allowed 500 calls per day per key. Thus, it will take around 1 hour 40 mins to finish.

You can minimize the window and let it run in the background, but ***DO NOT PUT YOUR COMPUTER TO SLEEP MODE***

## How to use this program
To run: just run it like any other python program.

*ex: python stock_data.py*

Libraries to install:
- Requests

If you don't have it, type this into command prompt:

- WINDOWS: *python -m pip install requests*
- MAC: *pip install requests*

It will ask for an input file path. Just input where your input file is.

*ex: c:/users/you/Downloads/input.csv*

*FILE REQUIREMENTS:*
- a csv file
  - format: One ticker per line
  - *ex: AAPL*
  - *ex: BRK.A*
- no header lines

It will also ask for your key. You can get your free key [here](https://www.alphavantage.co/support/#api-key).

## Output
For each quarter you check, it will output one csv file with data from that quarter.
It will also print out the progress in the terminal in case you are curious.

In the output files, you may see these exceptions:
- ERROR: An unknown error has occured
- N/A: This data is not available or recorded
