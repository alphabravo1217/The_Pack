# The_Pack

so, my Code:
1) Calculates the asia range (19:30 - 20:30, but can do any range really) high and low.
2) it then calculates the high and low from 20:30 - 16:00 the next day (again can be changed to whatever "session" you want)
3) it then finds the first candle that crosses either the asia range high or asia range low.
   a) Special note: The Cross Time and Cross Price are based on a candle fully closing above/below the asia range.  No wick or candle body within the range.
   b) this difers a little from Quantum's strat of just any first candle close above/below the range

Things I am working on are the calculations:  MAE (max drawdown), total range distance, and columns for trade entry (opposite of whatever Condition is)

The code can also resample the data to whatever timeframe you want.  My data is on the 1 minute, but can be changed to 5minute, 15, 18, 1 hour, 1 hour 16 minute (you get the idea)



I ask that people just random check an asset for a day/date and double check my results are accurate from the data.


Thanks Pack
We All Win Together
