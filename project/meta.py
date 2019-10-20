import configparser  # 1
from oandapyV20 import API
from oandapyV20.exceptions import V20Error, StreamTerminated
from oandapyV20.endpoints.instruments import InstrumentsCandles
import logging
import time
from a import sell
from test import main

user = main()

config = configparser.ConfigParser()  # 3
config.read('oanda.cfg')  # 4

access_token = config['oanda']['access_token']
accountID = config['oanda']['account_id']

api = API(access_token=access_token,
          environment="practice")

logging.basicConfig(
    filename="log.out",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
)

def Ema(instrument):
    global api
    r = InstrumentsCandles(instrument=instrument, params={"granularity": "H1"})
    api.request(r)
    q = r.response["candles"][-20:]
    Prices = []
    for i in q:
        Prices.append(float(i["mid"]["c"]))
    Ema5 = [Prices[-5]]
    Ema20 = [Prices[0]]
    for i in Prices[1:]:
        e = Ema20[-1] + ((2 / (len(Ema20) + 2)) * (i - Ema20[-1]))
        Ema20.append(e)
    for i in Prices[-4:]:
        e = Ema5[-1] + ((2 / (len(Ema5) + 2)) * (i - Ema5[-1]))
        Ema5.append(e)
    if Ema5[-2] < Ema20[-2] and Ema5[-1] > Ema20[-1]:
        sell(1)
    elif Ema5[-2] > Ema20[-2] and Ema5[-1] < Ema20[-1]:
        sell(-1)

timing = time.asctime().split()[3]
while timing[2:] != ":00:00":
    continue
print(timing)
instruments = user["instruments"]
while True:
    try:
        for instrument in instruments:
            Ema(instrument)
        timing = time.asctime().split()[3]
        while timing[2:] != ":00:00":
            continue
        print(timing)
    except V20Error as e:
        # catch API related errors that may occur
        with open("LOG", "a") as LOG:
            LOG.write("V20Error: {}\n".format(e))
        break
    except ConnectionError as e:
        with open("LOG", "a") as LOG:
            LOG.write("Error: {}\n".format(e))
    except StreamTerminated as e:
        with open("LOG", "a") as LOG:
            LOG.write("Stopping: {}\n".format(e))
        break
    except Exception as e:
        with open("LOG", "a") as LOG:
            LOG.write("??? : {}\n".format(e))
        break