import yfinance as yf
import pandas as pd
import numpy as np
import sys
import os

from scipy import signal
# import matplotlib.dates as mdates
from pandas_datareader import data as pdr

yf.pdr_override()


# use "period" instead of start/end
# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# (optional, default is '1mo')

# fetch data by interval (including intraday if period < 60 days)
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# (optional, default is '1d')
argv = sys.argv
tckr = "BBCA"
if 1 < len(argv):
    tckr = argv[1]

prd = "3mo"
if 2 < len(argv):
    prd = argv[2]

itv = "1d"
if 3 < len(argv):
    itv = argv[3]

upd = False
if 4 < len(argv):
    upd = argv[4] == "update"

csvfile = "{}-{}-{}.csv".format(tckr.lower(), prd, itv)
tickers = "{}.JK".format(tckr)

fexists = os.path.isfile(csvfile)
if not fexists | upd:
    pdr.get_data_yahoo(tickers, period=prd, interval=itv, auto_adjust=True).to_csv(csvfile)

df = pd.read_csv(csvfile)

# df['SMA5'] = df.Close.rolling(window=9).mean()
# prevclose = df.Close.shift(1)
# prevh = df.High.shift(1)
# prevl = df.Low.shift(1)
# prevsma5 = df.SMA5.shift(1)

# dikatakan bersilangan emas apabila nilai tutup sebelumnya lebih kecil dari nilai sma5
# gc = np.where((prevsma5 >= prevclose) & (df.SMA5 <= df.Close), "GC", "-")
# df['Crossing'] = np.where((prevsma5 <= prevclose) & (df.SMA5 >= df.Close), "DC", gc)

# df['buy'] = np.where(df.Crossing == 'GC', df.Close, '-')
# df['sell'] = np.where(df.Crossing == 'DC', df.Close, '-')

xp1 = df.Close.ewm(span=12, adjust=False).mean()
xp2 = df.Close.ewm(span=26, adjust=False).mean()

# df['MACD'] = xp1 - xp2
# df['SIGN'] = df.MACD.ewm(span=9, adjust=False).mean()

# prevm = df.MACD.shift(1)
# prevs = df.SIGN.shift(1)
# gc = np.where((prevs >= prevm) & (df.SIGN <= df.MACD), "GC", "-")
# df['Crossing'] = np.where((prevs <= prevm) & (df.SIGN >= df.MACD), "DC", gc)
currzz = 'valley'
lastpeak = {}
lastvalley = {}

h3 = (df.High.shift(3) + ((df.High.shift(3) * 1.5)/100))
h2 = (df.High.shift(2) + ((df.High.shift(2) * 1.5)/100))
h1 = (df.High.shift(1) + ((df.High.shift(1) * 1.5)/100))

l1 = (df.Low.shift(1) - ((df.Low.shift(1) * 1.5)/100))
l2 = (df.Low.shift(2) - ((df.Low.shift(2) * 1.5)/100))
l3 = (df.Low.shift(3) - ((df.Low.shift(3) * 1.5)/100))

_isu2d3 = np.where(df.Close.shift(3) <= df.Open.shift(3), -1, 1)
_isu2d2 = np.where(df.Close.shift(2) <= df.Open.shift(2), -1, 1)
_isu2d1 = np.where(df.Close.shift(1) <= df.Open.shift(1), -1, 1)
_isu2d = np.where(df.Close <= df.Open, -1, 1)

_bdir32 = np.where((_isu2d3 == 1) & (_isu2d2 == -1), -1, 1)
_bdir21 = np.where((_isu2d2 == 1) & (_isu2d1 == -1), -1, _bdir32)
_bdir10 = np.where((_isu2d == 1) & (_isu2d == -1), -1, _bdir21)

_bdir1 = np.where((_isu2d1 == 1) & (_isu2d == -1) & (_bdir10 == 1), 'peak', '-')
_bdir0 = np.where((_isu2d1 == -1) & (_isu2d == 1) & (_bdir10 == -1), 'valley', '-')

_bdirection = np.where(_bdir1 != '-', _bdir1, '-')
_direction = np.where(_bdir0 != '-', _bdir0, _bdirection)

# currentzz = np.where(_bdir1 == _bdir0, '-', _direction)
# findzz = np.where((currentzz != currzz) & (currentzz != '-'), currzz, currentzz)

df['zigzag'] = np.where(_bdir1 == _bdir0, '-', _direction)

# df['ud'] = np.where(df.Open <= df.Close, -1, 1)
# df['dir'] = df.ud.shift(1)


# ppeak = np.where((h3 < df.High) & (h2 < df.High) & (h1 < df.High), 'down', '-')
# df['fractal'] = np.where((l3 > df.Low) & (l1 > df.Low) & (l1 > df.Low), 'up', ppeak)
# df['buy'] = np.where((df.fractal == 'up') | (df.Crossing.shift(2) == 'DC'), df.Low + 5, '-')
# df['sell'] = np.where((df.fractal == 'down') | (df.Crossing.shift(2) == 'GC'), df.High - 5, '-')
df['buy'] = np.where(df.zigzag == 'valley', df.Low, '-')
df['sell'] = np.where(df.zigzag == 'peak', df.High, '-')

# print(df)
df.to_csv('result.csv')
# print(df.loc[df.zz != 'nzz'])
# print(df.loc[df['fractal'].isin(['down','up'])])
print(df.loc[df['zigzag'].isin(['peak', 'valley'])])