#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt # Alternative way to import the above
from tqdm import tqdm
from datetime import datetime, timedelta

#
# LINKS FOR REFERENCE
#
# Pandas Tutorial:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
#
# Pandas DataFrames:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
#
# Pandas Series:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series
#
# Datetime:
# https://docs.python.org/3/library/datetime.html
#
#

# Globals
tickerSymbol = 'TSLA'
startDate = datetime(2020, 1, 1)
#endDate = datetime(2020, 8, 22)
endDate = datetime.today()

#
def main():
    
    # Get Ticker Data
    print("Getting Ticker Data...")
    tickerData = yf.Ticker(tickerSymbol)
    data = yf.download(tickerSymbol, start=startDate, end=endDate)
   
    # Calculate Moving Averages
    numDays = 20
    number_series = data # Copy over the data
    windows = number_series.rolling(numDays) # using Pandas DataFrame Rolling time frame 
    moving_averages = windows.mean() # Using Pandas Window Average
    
    # Printing our Table w/ Moving Averages 
    strRow = 'Close'
    
    plt.close('all')
    plt.figure()
    plt.plot(moving_averages[strRow])
    plt.plot(data[strRow])
    plt.title(strRow)
    plt.ylabel('Price')
    plt.xlabel('Dates')
    # plt.show()


    # Doing a Monte Carlo Prediciton
    prediction_days = 50 
    number_simulation = 5
    
    # Common Parameters of our math function
    returns = data.pct_change()
    last_price = data[strRow]
    avg_daily_ret = returns.var()
    variance = returns.var()
    daily_vol = returns.std()
    daily_drift = avg_daily_ret - (variance / 2)
    drift = daily_drift - 0.5 * daily_vol ** 2

    # Setup the results Indexes
    results = pd.DataFrame()

    # Doing the Prediciton Math

    print("Performing Monte Carlo Math...")
    for i in tqdm(range(number_simulation)): 
        prices = []
        prices.append(data['Close'].iloc[-1])
        for d in range(prediction_days):
            shock = [drift + daily_vol * np.random.normal()]
            shock = np.mean(shock)
            price = prices[-1] * np.exp(shock)
            prices.append(price)
        results[i] = prices

    # set realEndDate, as our endDate above could have been a non-market day
    realEndDate = data.index[-1]

    # Let's generate the next market days for our future dataFrame (just doing M-F, ignoring Holidays for now)
    # print("Real End Date day of week:" + str(realEndDate.weekday())) 

    endDateWeekday = realEndDate.weekday() # Monday = 0, Tuesday = 1 ... Sunday = 6
    if endDateWeekday > 4 : # If weekday is greater than Friday yFinance gave us a weekend?
        print("Something has gone wrong, yFinance returned a non-market day as the last day")
        exit(-1)
    

    # Make days list 
    days = []

    # Get day of week 
    realEndDay = realEndDate.weekday()
      
    currDate = realEndDate
    days.append(currDate)
    for i in range(prediction_days) :
        if currDate.weekday() >= 4 :
            currDate = currDate + timedelta(days=3) 
        else :
            currDate = currDate + timedelta(days=1) 
        print(currDate)
        days.append(currDate)

    daysDF = pd.DataFrame(days)
     
    results['Date'] = daysDF
    results = results.set_index('Date')


    # Make the prediciton chart
    print(results)
    plt.plot(results)
    plt.ylabel('Value')
    plt.xlabel('Simulated days')
    plt.show()


    print("\n")
    print("Data: ")
    print(data)
    print("\n =================================================== \n")
    print("Results: ")
    print(results)


# This is executed when run from the command line
if __name__ == "__main__":
    main()