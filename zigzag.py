import pandas as pd
import numpy as np

def zigzag(df, open='Open', close='Close', high='High', low='Low', date='Date', zz='zigzag', peak='peak', valley='valley', separator='-'):
    # tmpcols = ['date', 'zz', 'price']
    # first initial tmp zigzag
    # tmpz = pd.DataFrame(columns=tmpcols)
    # fnv = pd.DataFrame({ 'date': [df[date]], 'zz': ['peak'], 'price': [df[high]]})
    # tmpz = np.where(tmpz.empty, tmpz.append(fnv, ignore_index=True), tmpz)

    _isu2d3 = np.where(df[close].shift(3) <= df[open].shift(3), -1, 1)
    _isu2d2 = np.where(df[close].shift(2) <= df[open].shift(2), -1, 1)
    _isu2d1 = np.where(df[close].shift(1) <= df[open].shift(1), -1, 1)
    _isu2d = np.where(df[close] <= df[open], -1, 1)

    _bdir32 = np.where((_isu2d3 == 1) & (_isu2d2 == -1), -1, 1)
    _bdir21 = np.where((_isu2d2 == 1) & (_isu2d1 == -1), -1, _bdir32)
    _bdir10 = np.where((_isu2d == 1) & (_isu2d == -1), -1, _bdir21)

    _bdir1 = np.where((_isu2d1 == 1) & (_isu2d == -1) & (_bdir10 == 1), peak, separator)
    _bdir0 = np.where((_isu2d1 == -1) & (_isu2d == 1) & (_bdir10 == -1), valley, separator)

    _bdirection = np.where(_bdir1 != separator, _bdir1, separator)
    _direction = np.where(_bdir0 != separator, _bdir0, _bdirection)

    # last tmp zz
    # _lastmp = tmpz.loc[len(tmpz)]

    # _peakprice = np.where((_direction == peak) & (_lastmp['price'] < df[high]), df[high], _direction)
    # _valleyprice = np.where((_peakprice == valley) & (_lastmp['price'] > df[low]), df[low], _peakprice)
    # _savedprice = np.where(_valleyprice == separator, 0, _valleyprice)

    # _saveddirection = np.where((_lastmp['zz'] == _direction) & (_bdir1 == _bdir0), separator, _direction)

    # _bsave2tmp = pd.DataFrame({ 'date': df[date], 'zz': _saveddirection, 'price': _savedprice})
    # update = df.loc[date].
    # np.where(_saveddirection != separator, update, separator)
    # df[zz] = np.where(_saveddirection != separator, tmpz.append(_bsave2tmp, ignore_index=True), separator)

    # _ndirection = np.where(_bdir1 == _bdir0, separator, _direction)
    df[zz] = np.where(_bdir1 == _bdir0, separator, _direction)
    # df[zz] = np.where(df[zz].shift(1) != df[zz], _ndirection, separator)
    # df['lastzz'] = np.where(df[zz].shift(1) == df[zz], df[zz].shift(1), df[date])

    return df