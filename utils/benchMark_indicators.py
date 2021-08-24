"""
https://github.com/twopirllc/pandas-ta/issues/367

Script to benchmark indicator generation time.

"""


import pandas as pd
import pandas_ta as ta

df = pd.read_parquet("df_file.txt")
print(df.shape)

def performance(df:pd.DataFrame, excluded:list, other:list, top:int = None, sortby:str = "secs", ascending:bool = False, places:int = 5):
    if df.empty: return
    top = int(top) if isinstance(top, int) and top > 0 else None

    data = []
    df = df.copy()
    indicators = df.ta.indicators(as_list=True, exclude=excluded)
    
    header = "Quickest" if ascending else "Slowest"
    header = f"{header} {top} Indicators" if top is not None else f"{header} Indicators"

    if len(indicators):
        for indicator in indicators:
            result = df.ta(indicator, timed=True)
            ms = float(result.timed.split(" ")[0].split(" ")[0])
            data.append({"indicator": indicator, "secs": round(0.001 * ms, places), "ms": ms})

    if len(other) > 0:
        for indicator in other:
            result = df.ta(indicator, timed=True)
            ms = float(result.timed.split(" ")[0].split(" ")[0])
            data.append({"indicator": indicator, "secs": round(0.001 * ms, places), "ms": ms})
        
    pdf = pd.DataFrame.from_dict(data)
    pdf.set_index("indicator", inplace=True)
    pdf.sort_values(by=sortby, ascending=ascending, inplace=True)

    print(f"\n{header}\n{len(header) * '='}")

    if top is not None:
        return pdf.head(top)
    return pdf


excluded = ["above", "above_value", "below", "below_value", "cross", "cross_value", "long_run", "short_run", "td_seq", "tsignals", "vp", "xsignals", "ichimoku"]
other = ["long_run", "short_run", "vp", "td_seq"]
pr = performance(df, excluded, other, top=10, ascending=False, places=6)
pr.style.background_gradient("autumn_r")