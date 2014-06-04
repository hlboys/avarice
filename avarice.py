import threading

import genconfig
import indicators
import loggerdb
import okcoin
import simulator
import strategies
import trader

CandleSizeSeconds = genconfig.CandleSize * 60

def do_every (interval, worker_func, iterations = 0):
    ''' Basic support for configurable/iterable threading'''
    if iterations != 1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func,\
                    0 if iterations == 0 else iterations-1]
        ).start ();
    worker_func ();

def RunCommon():
    '''Do the following forever:
    - Configure DB
    - Make candles based on genconfig.CandleSize.
    - Make a candle price list
    - Run indicator specified on genconfig.Indicator'''

    loggerdb.PopulateRow()
    indicators.MakeCandlePriceList()

    for indicator in genconfig.IndicatorList:
        getattr(indicators, indicator)()

    strategies.Generic()

    if genconfig.SimulatorTrading:
        simulator.SimulateFromIndicator()
    else:
        trader.TradeFromIndicator()

# RunAll automatically if avarice is run directly
if __name__ == '__main__':
    # Sometimes we do not want to drop table for debugging.
    # This *should never* be used in standard runtime
    if not genconfig.Debug:
        loggerdb.ConfigureDatabase()

    do_every(CandleSizeSeconds, RunCommon)
