# Stock-data-collector-2021
This is the program we use to gather data with Alpha Vantage's API service.
Alpha Vantage provides free price and fundamental data, but you are only allowed 5 calls per minute (1 call per 12 sec.)
You are also only allowed 500 calls per day per key.

## How to use this program
To run: don't forget that it has one command line argument: VERSION

*ex: python stock_data.py 1*

If you input 1, then it will not limit the program to 500 calls total, which may or may not cause errors, depending on whether Alpha Vantage is feeling nice or not.
Any other input will limit it to 500 calls, and there is an option to continue from where you left off.

It will ask for an input file path. Just input where your input file is.

*ex: c:/users/you/Downloads/input.csv*

*FILE REQUIREMENTS:*
- a csv file
- format: *ticker,company_name,industry/sector*
- no header lines

It will also ask for your key. You can get your free key [here](https://www.alphavantage.co/support/#api-key).

## Output
It is going to output the number that you inputted into "How many quarters to check" amount of csv files with data.
It will also print out the progress in the terminal in case you are curious.

In the output files, you may see these exceptions:
- ERROR: An unknown error has occured
- N/A: The stock didn't exist at the time
