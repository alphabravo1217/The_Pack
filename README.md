# The_Pack

so, my Code:
1) Calculates the asia range (19:30 - 20:30, but can do any range really) high and low.
2) it then calculates the high and low from 20:30 - 16:00 the next day (again can be changed to whatever "session" you want)
3) After the "open session" and 'daily' Highs and Lows are found, the code finds
    a) the first candle that closes above or below the Open Session high/low
    b) the first candle above/below the high/low FULLY Outside the range (no part of the wick/body is within the open session range
4) Calculates the max MAE (Draw Down) from those candles in #3 to the daily high/low from #2.
5) Finally finds the first candle that crosses the opposite side of the range.
6) I have provided a summary of the stats for the assets I have, as well as scatter plots for the Max MAE

Keep in mind, my data only goes back to March 2024, so the summary stats and scatter plots only cover that timeframe.

The code can also resample the data to whatever timeframe you want.  My data is on the 1 minute, but can be changed to 5minute, 15, 18, 1 hour, 1 hour 16 minute (you get the idea)

If anyone needs help understanding the code, please let me know in discord.

I ask that people just random check an asset for a day/date and double check my results are accurate from the data.


Thanks Pack
We All Win Together

AlphaBravo
