import pandas as pd
from pytrends.request import TrendReq
import seaborn as sns
import matplotlib.pyplot as plt
from pandas_datareader import data
import requests
import yfinance as yf
from pandas import DataFrame

#input... can be array but need flask functionality
#stock_ticker = ["MSFT","AAPL","WORK","AMD"]

#nothing
#stock_name = []

#for x in stock_ticker:
#    tick = yf.Ticker(x)
#    stock_name.append(tick.info['shortName'])

def get_searches(key_word):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([key_word], cat=0, timeframe='2020-01-01 2021-01-15',  gprop='',geo='')
    df = pytrends.interest_over_time()

    print(df.head())

    sns.set()
    df['timestamp'] = pd.to_datetime(df.index)
    sns.lineplot(x=df['timestamp'], y=df[key_word])

    plt.title("Normalized Searches for {}".format(key_word))
    plt.ylabel("Number of Searches")
    plt.xlabel("Date")
    plt.savefig("template/static/images/search.png")
    plt.close()


def get_finance(key_word):
    df = yf.download(key_word, start='2020-01-01', end='2021-01-15')['Adj Close']
    pd.plotting.register_matplotlib_converters()
# Load the data

# Set the style to seaborn for plotting
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(12, 6))
# Plot the cumulative returns fot each symbol
    ax.plot(df)
    plt.title('Adjusted Close Price - {}'.format(key_word), fontsize=16)
# Define the labels for x-axis and y-axis
    plt.ylabel('Adjusted Close Price', fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.savefig('template/static/images/finance.png')
    plt.close()

def prediction(key_word):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([key_word], cat=0, timeframe='2021-01-01 2021-01-15',  gprop='',geo='')
    df = pytrends.interest_over_time()

    std = pd.DataFrame.from_dict(df)

    std['Moving Average'] = std[key_word].rolling(2).mean()
    std[[key_word,'Moving Average']].plot(figsize=(10,4))
    plt.grid(True)
    plt.title(key_word +" Google Trends" ' Moving Averages')
    plt.axis('tight')
    plt.ylabel('Searches')
    plt.savefig('template/static/images/prediction.png')
    plt.close()

def actual_prediction(key_word):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([key_word], cat=0, timeframe='2021-01-01 2021-01-15',  gprop='',geo='')
    df = pytrends.interest_over_time()
    std = pd.DataFrame.from_dict(df)

    std['Moving Average'] = std[key_word].rolling(2).mean()

    close = float(std.loc['2021-01-15','Moving Average'])
    l=[]
    l.append(float(std.loc['2021-01-15','Moving Average']))
    l.append(float(std.loc['2021-01-13','Moving Average']))
    l.append(float(std.loc['2021-01-14','Moving Average']))
    l.append(float(std.loc['2021-01-12','Moving Average']))
    l.append(float(std.loc['2021-01-11','Moving Average']))
    l.append(float(std.loc['2021-01-10','Moving Average']))
    l.append(float(std.loc['2021-01-09','Moving Average']))

    average =0
    count = 0
    for x in l:
        average = average + x
        count +=1

    average  = average /count

    ender = (float(std.loc['2021-01-15','Moving Average'])/average)
    print(ender)
    if ender >1.10:
        ender = ender*0.90
    elif ender >1.15:
        ender = ender *0.85
    elif ender <1.00:
        ender = ender *1.02

    df = yf.download(key_word, start='2021-01-01', end='2021-01-16')['Adj Close']
    eat = pd.DataFrame.from_dict(df)
    fire = float(eat.loc['2021-01-15','Adj Close'])
    print(fire)
    fire = fire*ender
    print(fire)
    df1 = pd.DataFrame({"a":["2021-01-04","2021-01-05","2021-01-06","2021-01-07",
                            "2021-01-08","2021-01-11","2021-01-12","2021-01-13",
                            "2021-01-14","2021-01-15","2021-01-22"],
                            "b":[float(eat.loc['2021-01-04','Adj Close']),float(eat.loc['2021-01-05','Adj Close']),
                            float(eat.loc['2021-01-06','Adj Close']),float(eat.loc['2021-01-07','Adj Close']),
                            float(eat.loc['2021-01-08','Adj Close']),float(eat.loc['2021-01-11','Adj Close']),
                            float(eat.loc['2021-01-12','Adj Close']),float(eat.loc['2021-01-13','Adj Close']),
                            float(eat.loc['2021-01-14','Adj Close']),float(eat.loc['2021-01-15','Adj Close']), fire]})

    sns.set()

    sns.lineplot(x=df1['a'], y=df1['b'])

    plt.title("Predicted Stock Price {}".format(key_word))
    plt.ylabel("Price")
    plt.xlabel("Date")
    plt.savefig('template/static/images/actual.png')
    plt.close()
