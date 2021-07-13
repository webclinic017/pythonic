# Bullish Divergence
for i in range(len(Data)):
    try:
        if Data.iloc[i].RSI < lower_barrier:
            for a in range(i + 1, i + width):
                if Data.iloc[a].RSI > lower_barrier:
                    for r in range(a + 1, a + width):
                        if Data.iloc[r].RSI < lower_barrier and Data.iloc[r].RSI > Data.iloc[i].RSI and Data.iloc[r].close < Data.iloc[i].close:
                            for s in range(r + 1, r + width): 
                                if Data.iloc[s].RSI > lower_barrier:
                                    Data.at[s + 1,'Bull'] = 1
                                    break
                                else:
                                    continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
    except IndexError:
        pass

# Bearish Divergence
for i in range(len(Data)):
    try:
        if Data.iloc[i].RSI > upper_barrier:
            for a in range(i + 1, i + width): 
                if Data.iloc[a].RSI < upper_barrier:
                    for r in range(a + 1, a + width):
                        if Data.iloc[r].RSI > upper_barrier and Data.iloc[r].RSI < Data.iloc[i].RSI and Data.iloc[r].close > Data.iloc[i].close:
                            for s in range(r + 1, r + width):
                                if Data.iloc[s].RSI < upper_barrier:
                                    Data.at[s + 1, 'Bear'] = -1
                                    break
                                else:
                                    continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
    except IndexError:
        pass


