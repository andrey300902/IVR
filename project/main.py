from GUI import *
from functions import main, set_list, delete_list, reporting, change
import sys
import oandapyV20.endpoints.orders as orders
import json
import configparser  # 1
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.instruments import InstrumentsCandles
import logging
import time
import oandapyV20.endpoints.accounts as accounts

login = main()
Data = open('data.json')
Data = json.load(Data)['users']
f = False
for i in Data:
    for k in i:
        if k == login:
            user = i[login]
            f = True
    if f:
        break

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

statistic = []

def Ema(instrument):
    global api, instruments
    flag = instruments[instrument]
    r = InstrumentsCandles(instrument=instrument, params={"granularity": "H1"})
    api.request(r)
    q = r.response["candles"][-8:]
    Prices = []
    for i in q:
        Prices.append(float(i["mid"]["c"]))
    Ema3 = [Prices[-3]]
    Ema5 = [Prices[-5]]
    Ema8 = [Prices[0]]
    for i in Prices[1:]:
        e = Ema8[-1] + ((2 / (len(Ema8) + 2)) * (i - Ema8[-1]))
        Ema8.append(e)
    for i in Prices[-4:]:
        e = Ema5[-1] + ((2 / (len(Ema5) + 2)) * (i - Ema5[-1]))
        Ema5.append(e)
    for i in Prices[-2:]:
        e = Ema3[-1] + ((2 / (len(Ema3) + 2)) * (i - Ema3[-1]))
        Ema3.append(e)

    if flag == 0 and Ema3[-1] > Ema5[-1] > Ema8[-1]:
        if sell(instrument, 1):
            instruments[instrument] = -1
    elif flag == 0 and Ema3[-1] < Ema5[-1] < Ema8[-1]:
        if sell(instrument, -1):
            instruments[instrument] = 1
    elif flag != 0 and ((Ema3[-2] > Ema5[-2] and Ema3[-1] < Ema5[-1]) or (Ema3[-2] < Ema5[-2] and Ema3[-1] > Ema5[-1])):
        if sell(instrument, flag):
            instruments[instrument] = 0

def sell(instrument, k):
    global access_token, accountID
    logging.basicConfig(
        filename="log.out",
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
    )
    unit = str(k * 100)

    orderConf = [
           {
             "order": {
                "units": unit,
                "instrument": instrument,
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT",
            }
        }
    ]

# client
    api = API(access_token=access_token)

# create and process order requests
    for O in orderConf:
        r = orders.OrderCreate(accountID=accountID, data=O)
        print("processing : {}".format(r))
        print("===============================")
        print(r.data)
        try:
            response = api.request(r)
        except V20Error as e:
            print("V20Error: {}".format(e))
        else:
            print("Response: {}\n{}".format(r.status_code,
                                            json.dumps(response, indent=2)))

    global statistic
    if k == -1:
        statistic.append([time.time(), instrument, "Продажа", 100])
    else:
        statistic.append([time.time(), instrument, "Купля", 100])


Surface = pygame.display.set_mode((550, 350))
report = Button((145, 170, 100, 50), "Отчет")
delete = Button((145, 100, 270, 50), "Удалить акции")
add = Button((145, 30, 270, 50), "Добавить акции")
settings = Button((145, 250, 180, 50), "Настройки")
instruments = user["instruments"]
print(instruments)
while True:
    time1 = time.asctime().split()
    timing = time1[3]
    if timing[2:] == ":00:00":
        if timing[0:2] == '00':
            data = open('statistic.json')
            data = json.load(data)
            data['balance'].append([time1, api.request(accounts.AccountDetails(accountID))['account']['balance']])
            with open("statistic.json", 'w') as file:
                file.write(data)
            if user['mode'] == 3:
                for i in instruments:
                    sell(i, instruments[i])
            elif time1[0] == 'Sat' and user['mode'] == 2:
                for i in instruments:
                    sell(i, instruments[i])
        for instrument in instruments:
            try:
                Ema(instrument)
            except:
                continue
        user["instruments"] = instruments
        for i in range(len(Data)):
            for k in Data[i]:
                if k == login:
                    Data[i][login] = user
        jData = json.dumps({"users": Data})
        with open("data.json", 'w') as file:
            file.write(jData)
        data = open('statistic.json')
        data = json.load(data)
        for i in statistic:
            data['deals'].append(i)
        data = json.dumps(data)
        with open("statistic.json", 'w') as file:
            file.write(data)
        statistic = []
    Surface.fill(pygame.Color('yellow'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if add.get_event(event):
            add_list = set_list()
            for i in add_list:
                if i not in instruments:
                    instruments[i] = 0
            user["instruments"] = instruments
            for i in range(len(Data)):
                for k in Data[i]:
                    if k == login:
                        Data[i][login] = user
            jData = json.dumps({"users": Data})
            with open("data.json", 'w') as file:
                file.write(jData)

        if delete.get_event(event):
            del_list = delete_list(instruments)
            for i in del_list:
                sell(i, instruments[i])
            for i in del_list:
                del instruments[i]
            user["instruments"] = instruments
            for i in range(len(Data)):
                for k in Data[i]:
                    if k == login:
                        Data[i][login] = user
            jData = json.dumps({"users": Data})
            with open("data.json", 'w') as file:
                file.write(jData)

        if report.get_event(event):
            reporting()

        if settings.get_event(event):
            d = change(login, user)
            f = False
            for i in range(len(Data)):
                for k in Data[i]:
                    if k == login:
                        del Data[i]
                        f = True
                if f:
                    break
            Data.append(d)
            jData = json.dumps({"users": Data})
            with open("data.json", 'w') as file:
                file.write(jData)


    delete.render(Surface)
    add.render(Surface)
    settings.render(Surface)
    report.render(Surface)
    pygame.display.update()