import os
import requests
import time
from datetime import datetime
#import schedule

key = os.getenv("ALPHAVANTAGEKEY")


#creates a function that prints EMA and notifies if there is a signal
def emacross() -> str:
    try:

        #doing API calls and saving them
        spyurl = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=SPY&interval=1min&apikey={key}'
        spy5emaurl = f"https://www.alphavantage.co/query?function=EMA&symbol=SPY&interval=1min&time_period=5&series_type=close&apikey={key}"
        spy9emaurl = f"https://www.alphavantage.co/query?function=EMA&symbol=SPY&interval=1min&time_period=9&series_type=close&apikey={key}"
        spy20emaurl = f"https://www.alphavantage.co/query?function=EMA&symbol=SPY&interval=1min&time_period=20&series_type=close&apikey={key}"

        r = requests.get(spyurl)
        spydata = r.json()
        r = requests.get(spy5emaurl)
        spy5ema = r.json()
        r = requests.get(spy9emaurl)
        spy9ema = r.json()
        r = requests.get(spy20emaurl)
        spy20ema = r.json()

        #finding the last time API updated
        lastupdate = next(iter(spydata["Time Series (1min)"]))

        #saving all price levels
        spyprice = str((spydata["Time Series (1min)"][lastupdate]["4. close"]))
        spy5ema = spy5ema["Technical Analysis: EMA"][lastupdate[0:(len(lastupdate)-3)]]["EMA"]
        spy9ema = spy9ema["Technical Analysis: EMA"][lastupdate[0:(len(lastupdate)-3)]]["EMA"]
        spy20ema = spy20ema["Technical Analysis: EMA"][lastupdate[0:(len(lastupdate)-3)]]["EMA"]


        print("SPY Price: " + spyprice)
        print("SPY 5 EMA: " + spy5ema)
        print("SPY 9 EMA: " + spy9ema)
        print("SPY 20 EMA: " + spy20ema)
        data = [spyprice,spy5ema,spy9ema,spy20ema]

        if (spy9ema>spy20ema and spy5ema>spy9ema):
            print("SPY CALL CROSS!")
            data.append("call")
            return (data)

        elif (spy9ema<spy5ema and spy20ema>spy9ema):
            print("SPY PUT CROSS")
            data.append("put")
            return(data)

        else:
            print("NO ACTION")
            data.append("none")
            return(data)

    #except block if i went over API limit
    except:
        print("Out of API calls")


#creating a recursive loop that starts and ends the program during market hours
def startProgram():
    print("starting loop")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if (now.strftime("%H:%M") == "6:30"):
            break

    print("market open")
    print("starting program")

    while (True):
        print(emacross())
        time.sleep(60)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if (now.strftime("%H:%M") == "13:01"):
            print("market close")
            print("stopping program")
            break

    startProgram()



startProgram()
