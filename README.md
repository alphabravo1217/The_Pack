# The_Pack

so, my Code:
1) Calculates the asia range (19:30 - 20:30, but can do any range really) high and low.
2) it then calculates the high and low from 20:30 - 16:00 the next day (again can be changed to whatever "session" you want)
3) After the "open session" and 'daily' Highs and Lows are found, the code finds
    a) the first candle that closes above or below the Open Session high/low
    b) the first candle above/below the high/low FULLY Outside the range (no part of the wick/body is within the open session range
4) Calculates the max MAE (Draw Down) from those candles in #3 to the daily high/low from #2.
5) Finally finds the first candle that crosses the opposite side of the range.
6) Calculates the summary of whatever asset, as well as the MAE scatter plot.




Thanks Pack
We All Win Together

AlphaBravo
