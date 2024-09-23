# Asher_Custom_Functions.py>

import pandas as pd
from datetime import datetime, time, timedelta


######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
# Function to resample the 1 minute timeframe data to new timeframe
def resample_data(data, timeframe):
    
    resampled_data = data.resample(timeframe).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    }).dropna()
    
    return resampled_data

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
# Find the High and Low of a range
def Range_HighLow(df, starttime, endtime):
    # Convert starttime and endtime to datetime.time objects
    starttime = pd.to_datetime(starttime).time()
    endtime = pd.to_datetime(endtime).time()
    
    # Handle cases where the time range crosses midnight
    if starttime < endtime:
        # Time range within the same day
        df_filtered = df[(df.index.time >= starttime) & (df.index.time <= endtime)]
    else:
        # Time range crosses midnight
        df_filtered = df[(df.index.time >= starttime) | (df.index.time <= endtime)]

    # Create a dataframe to hold the results
    results = []

    # Group by 'Day_of_Week' and calculate the highest high, lowest low, and their timestamps
    for day, group in df_filtered.groupby('TRADE DAY'):
        # Find highest high and its timestamp
        highest_high = group['High'].max()
        high_time = group[group['High'] == highest_high].index[0]

        # Find lowest low and its timestamp
        lowest_low = group['Low'].min()
        low_time = group[group['Low'] == lowest_low].index[0]

        # Append the results
        results.append({
            'Date': day,
            'Day_of_Week': group['Day_of_Week'].iloc[0],
            'Highest High': highest_high,
            'Highest High Time': high_time,
            'Lowest Low': lowest_low,
            'Lowest Low Time': low_time
        })

    # Create a new dataframe with the results
    result_df = pd.DataFrame(results)
    
    return result_df

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
def First_Close(df, Session_start, Session_end, summary_df):
    # Create an empty list to store results
    results = []
    
    # Iterate through each row in summary_df
    for i, row in summary_df.iterrows():
        day_of_week = row['Day of the Week']
        trade_day = row['Date']
        open_high = row['Open Session High']
        open_low = row['Open Session Low']
    
        # Filter df for the corresponding trade day
        df_filtered = df[df['TRADE DAY'] == trade_day]
        df_filtered_after_session = df_filtered.between_time(Session_end, '16:00')

        # Finds first candle close after end of opening session
        first_match = df_filtered_after_session[(df_filtered_after_session['Close'] > open_high) | 
                                                (df_filtered_after_session['Close'] < open_low)].head(1)

        # Finds first candle close after end of opening session with no part of the candle inside the opening range
        first_full_outside_match = df_filtered_after_session[(df_filtered_after_session['Low'] > open_high) | 
                                                             (df_filtered_after_session['High'] < open_low)].head(1)
        
        # Check if there is a match for the first close outside the range
        if not first_match.empty:
            first_close_price = first_match['Close'].values[0]
            first_close_time = first_match.index[0]
            
            # Determine condition based on whether the close is above or below the range
            if first_close_price > open_high:
                condition = 'Above Open Session High'
            elif first_close_price < open_low:
                condition = 'Below Open Session Low'
            else:
                condition = 'Does Not Cross'
        else:
            first_close_price = 'Does Not Cross'
            first_close_time = 'Does Not Cross'
            condition = 'Does Not Cross'
        
        # Check if there is a match for the fully outside close
        if not first_full_outside_match.empty:
            first_full_price = first_full_outside_match['Close'].values[0]
            first_full_time = first_full_outside_match.index[0]
            
            if first_full_price > open_high:
                condition2 = 'Above Open Session High'
            elif first_full_price < open_low:
                condition2 = 'Below Open Session Low'
            else:
                condition2 = 'Does Not Fully Cross'
        else:
            first_full_price = 'Does Not Fully Cross'
            first_full_time = 'Does Not Fully Cross'
            condition2 = 'Does Not Fully Cross'
        
        # Append the result to the results list
        result = {
            'Date': trade_day,
            'Day of the Week': day_of_week,
            'First Close Time': first_close_time,
            'First Close Price': first_close_price,
            'First Candle Close Condition': condition,
            'First Fully Close Time': first_full_time,
            'First Fully Close Price': first_full_price,
            'First Candle Fully Close Condition': condition2
        }
        
        results.append(result)
        
    # Convert the results to a DataFrame
    return pd.DataFrame(results)


######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
# Find if a candle crosses the opposite side of the opening range
def opposite_cross(df, Session_start, Session_end, summary_df):
    # Create an empty list to store results
    results = []

    # Iterate through each row in summary_df
    for _, row in summary_df.iterrows():
        # Extract the date and the Opening Range High and Low
        first_condition = row['First Candle Close Condition']
        day_of_week = row['Day of the Week']
        trade_day = row['Date']
        open_high = row['Open Session High']
        open_low = row['Open Session Low']
    
        # Filter df for the corresponding trade day
        df_filtered = df[df['TRADE DAY'] == trade_day]
        df_filtered_after_session = df_filtered.between_time(Session_end, '16:00')
    
        # Determine the logic for finding the opposite side cross
        if first_condition == 'Below Open Session Low':
            # Find the first candle that crosses the Opening Range High
            first_cross_row = df_filtered_after_session[df_filtered_after_session['High'] >= row['Open Session High']].head(1)
            cross_condition = 'Crossed Above Open Session Hight'
        elif first_condition == 'Above Open Session High':
            # Find the first candle that crosses the Opening Range Low
            first_cross_row = df_filtered_after_session[df_filtered_after_session['Low'] <= row['Open Session Low']].head(1)
            cross_condition = 'Crossed Below Open Session Low'
        else:
            continue
            
    
    # Check if the first_cross_row is not empty before accessing values
        if not first_cross_row.empty:
            cross_price = first_cross_row.iloc[0]['High'] if first_condition == 'Below Open Session Low' else first_cross_row.iloc[0]['Low']
            cross_time = first_cross_row.index[0].time()
    
            result = {
                'Date': trade_day,
                'Day of the Week': day_of_week,
                'Opposite Side Cross Time': cross_time,
                'Opposite Side Cross Price': cross_price,
                'Opposite Side Cross Condition': cross_condition
            }
        else:
            result = {
                'Date': trade_day,
                'Day of the Week': day_of_week,
                'Opposite Side Cross Time': 'Does Not Cross',
                'Opposite Side Cross Price': 'Does Not Cross',
                'Opposite Side Cross Condition': 'Does Not Cross'
            }
    
        results.append(result)
    
    
    return pd.DataFrame(results)

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
# Calculate Distributions
def calculate_distributions(final_df, ticker):
    # Dictionaries containing tick sizes and tick profit for each asset
    Profit_per_Tick = {
        "MES=F" :  1.25,    "MYM=F" :  0.50,    "NG=F"  : 10.00,    "MNQ=F" :  0.50,
        "ES=F"  : 12.50,    "NQ=F"  :  5.00,    "YM=F"  :  5.00,    "CL=F"  : 10.00,
        "MCL=F" :  1.00,    "GC=F"  : 10.00,    "MGC=F" :  1.00,    "RTY=F" :  5.00,
        "M2K=F" :  0.50,    "SI=F"  : 25.00,    "PL=F"  :  5.00,    "HG=F"  : 12.50,
        "SIL=F" : 10.00
    }

    TickSize = {
        "MES=F" :   0.2500,   "MYM=F" :   1.0000,   "NG=F"  :   0.0010,   "MNQ=F" :   0.2500,
        "ES=F"  :   0.2500,   "NQ=F"  :   0.2500,   "YM=F"  :   1.0000,   "CL=F"  :   0.0100,
        "MCL=F" :   0.0100,   "GC=F"  :   0.1000,   "MGC=F" :   0.1000,   "RTY=F" :   0.1000,
        "M2K=F" :   0.1000,   "SI=F"  :   0.0050,   "PL=F"  :   0.1000,   "HG=F"  :   0.0005,
        "SIL=F" :   0.0100
    }

    # Calculate Ticks_per_Point
    Ticks_per_Point = {asset: 1 / ticksize for asset, ticksize in TickSize.items()}

    # Ensure columns involved in arithmetic operations are numeric
    columns_to_convert = [
        'First Close Price', 'Trade Session High', 'Trade Session Low',
        'First Fully Close Price'
    ]
    final_df[columns_to_convert] = final_df[columns_to_convert].apply(pd.to_numeric, errors='coerce')

    # Set default values in the DataFrame
    final_df['Max Distribution/Drawdown (points)'] = None
    final_df['Max Distribution (%)'] = None
    final_df['Max Distribution/Drawdown (Fully Outside) (points)'] = None
    final_df['Max Distribution (Fully Outside) (%)'] = None

    # Calculations for 'Above Opening High' and 'Below Opening Low'
    final_df.loc[final_df['First Candle Close Condition'] == 'Above Open Session High', 'Max Distribution/Drawdown (points)'] = (
        final_df['Trade Session High'] - final_df['First Close Price']) / Ticks_per_Point[ticker]

    final_df.loc[final_df['First Candle Close Condition'] == 'Below Open Session Low', 'Max Distribution/Drawdown (points)'] = (
        final_df['First Close Price'] - final_df['Trade Session Low']) / Ticks_per_Point[ticker]

    final_df.loc[final_df['First Candle Close Condition'] == 'Above Open Session High', 'Max Distribution (%)'] = ((
        final_df['Trade Session High'] - final_df['First Close Price']) / final_df['Trade Session High']) * 100

    final_df.loc[final_df['First Candle Close Condition'] == 'Below Open Session Low', 'Max Distribution (%)'] = ((
        final_df['First Close Price'] - final_df['Trade Session Low']) / final_df['Trade Session Low']) * 100

    final_df.loc[final_df['First Candle Fully Close Condition'] == 'Above Open Session High',\
        'Max Distribution/Drawdown (Fully Outside) (points)'] = \
        (final_df['Trade Session High'] - final_df['First Fully Close Price']) / Ticks_per_Point[ticker]

    final_df.loc[final_df['First Candle Fully Close Condition'] == 'Below Open Session Low',\
        'Max Distribution/Drawdown (Fully Outside) (points)'] = \
        (final_df['First Fully Close Price'] - final_df['Trade Session Low']) / Ticks_per_Point[ticker]

    final_df.loc[final_df['First Candle Fully Close Condition'] == 'Above Open Session High', 'Max Distribution (Fully Outside) (%)'] = ((
        final_df['Trade Session High'] - final_df['First Fully Close Price']) / final_df['Trade Session High']) * 100

    final_df.loc[final_df['First Candle Fully Close Condition'] == 'Below Open Session Low', 'Max Distribution (Fully Outside) (%)'] = ((
        final_df['First Fully Close Price'] - final_df['Trade Session Low']) / final_df['Trade Session Low']) * 100

    # Win/Loss conditions
    final_df['Win/(Loss)'] = final_df['Opposite Side Cross Condition'].apply(lambda x: 'Loss' if x == 'Does Not Cross' else 'Win')

    return final_df


######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################



































