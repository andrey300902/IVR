import sys
from GUI import *
import json
import time
import matplotlib
import matplotlib.backends.backend_agg as agg
import pylab
import os

FPS = 30
pygame.init()
Data = open('data.json')
Data = json.load(Data)['users']

index = {
    "Форекс": ['EUR_USD', "USD_JPY", 'GBP_USD', 'AUD_USD', 'USD_CHF', "USD_CAD", "EUR_JPY", "EUR_GBP"],
    "Товары": ["BRENT", "NATURAL GAS", "WEST TEXAS OIL", "SOYBEANS", "SUGAR", "CORN"],
    "Индексы": ["UK 100", "US WALL ST 30", "GERMANY 30", "AUSTRALIA 200", "US SPX 500", "SWISS 20", "EUROPE 50"],
    "Облигации": ["UK 10Y GILT", "BUND", "US 2Y T-NOTE", "US 5Y T-NOTE", "US 10Y T-NOTE", "US T-BOND"],
    "Металлы": ["GOLD", "SILVER", "GOLD/SILVER", "PLATINUM", "PALLADIUM"]
}


def start():
    gui = GUI()
    Surface = pygame.display.set_mode((650, 450))
    Hello = Label([250, 150, 150, 60], "Baranoff")
    b_start = Button([275, 220, 100, 50], "Войти")
    b_reg = Button([230, 280, 205, 50], "Регистрация")
    while True:
        Surface.fill(pygame.Color("yellow"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            b_start.get_event(event)
            b_reg.get_event(event)
            if b_reg.pressed:
                return True
            if b_start.pressed:
                return False
        Hello.render(Surface)
        b_start.render(Surface)
        b_reg.render(Surface)
        pygame.display.update()


def set_login():
    gui = GUI()
    l = Label([10, 230, 150, 30], "")
    def check(text):
        f = True
        l.font_color = pygame.Color("red")
        if len(text) < 8:
            l.text = "Логин слишком короткий"
            f = False
        elif len(text) > 30:
            l.text = "Логин слишком длинный"
            f = False
        else:
            for char in text:
                if 48 <= ord(char) <= 57 or 97 <= ord(char) <= 122 or 65 <= ord(char) <= 90 or ord(char) == 45 or ord(char) == 95:
                    continue
                else:
                    l.text = "Недопустимые символы"
                    f = False
                    break
            for user in Data:
                for i in user:
                    if i == text:
                        l.text = "Логин уже занят"
                        f = False
                        break
                if f:
                    break

        if f:
            l.font_color = pygame.Color("green")
            l.text = "Хороший логин"
            l.render(Surface)
            pygame.display.update()
            global new_user
            new_user = {text: {}}
            pygame.time.wait(2000)
            return True

    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([10, 10, 150, 30], "Придумайте логин:"))
    gui.add_element(Label([10, 50, 150, 30], "Логин должен состоять из 8 - 30 символов"))
    gui.add_element(Label([10, 90, 150, 30], "Может содержать строчные и заглавные буквы"))
    gui.add_element(Label([10, 130, 150, 30], "а также цифры и символы _ и -"))
    gui.add_element(TextBox([10, 170, 300, 30], ""))

    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            res = gui.get_event(event)
            if res != None:
                if check(res):
                    return

        gui.render(Surface)
        l.render(Surface)
        pygame.display.update()
        gui.update()

def set_password():
    gui = GUI()
    l = Label([10, 230, 150, 30], "")
    def check(text):
        f = True
        l.font_color = pygame.Color("red")
        if len(text) < 8:
            l.text = "Пароль слишком короткий"
            f = False
        elif len(text) > 30:
            l.text = "Пароль слишком длинный"
            f = False
        else:
            for char in text:
                if 48 <= ord(char) <= 57 or 97 <= ord(char) <= 122 or 65 <= ord(char) <= 90 or ord(char) == 45 or ord(
                        char) == 95:
                    continue
                else:
                    l.text = "Недопустимые символы"
                    f = False
                    break

        if f:
            l.font_color = pygame.Color("green")
            l.text = "Хороший пароль"
            l.render(Surface)
            pygame.display.update()
            global new_user
            for i in new_user:
                new_user[i] = {"password": text}
            pygame.time.wait(2000)
            return True

    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([10, 10, 150, 30], "Придумайте пароль:"))
    gui.add_element(Label([10, 50, 150, 30], "Пароль должен состоять из 8 - 20 символов"))
    gui.add_element(Label([10, 90, 150, 30], "Может содержать строчные и заглавные буквы"))
    gui.add_element(Label([10, 130, 150, 30], "а также цифры и символы _ и -"))
    gui.add_element(TextBox([10, 170, 300, 30], "", True))

    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            res = gui.get_event(event)
            if res != None:
                if check(res):
                    return

        gui.render(Surface)
        l.render(Surface)
        pygame.display.update()
        gui.update()


def set_token():
    gui = GUI()
    l = Label([10, 230, 150, 30], "")

    def check(text):
            global new_user
            for i in new_user:
                new_user[i]["token"] = text
            pygame.time.wait(2000)
            return True

    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([10, 10, 150, 30], "Войдите в свой аккаунт на oanda.com"))
    gui.add_element(Label([10, 50, 150, 30], 'Перейдите в раздел "Управление API доступом"'))
    gui.add_element(Label([10, 90, 150, 30], 'Нажмите кнопку "Generate"'))
    gui.add_element(Label([10, 130, 150, 30], "Скопирйте свой Token и вставьте в форму ниже"))
    gui.add_element(TextBox([10, 170, 550, 30], "", False))

    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            res = gui.get_event(event)
            if res != None:
                if check(res):
                    return

        gui.render(Surface)
        pygame.display.update()
        gui.update()


def favour(instrument):
    gui = GUI()
    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([100, 20, 100, 40], "Список ожидания"))
    button = Button([500, 400, 140, 30], "Продолжить")
    instruments = set()
    y = 100
    for i in instrument:
        gui.add_element(CheckBox([70, y, 150, 30], i))
        y += 40
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            gui.get_event(event)
            button.get_event(event)
            if button.pressed:
                while len(gui.elements) > 1:
                    if gui.elements[1].pressed:
                        instruments.add(gui.elements[1].text)
                    del gui.elements[1]
                return instruments

        gui.render(Surface)
        button.render(Surface)
        pygame.display.update()


def set_list():
    gui = GUI()
    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([100, 20, 100, 40], "Выберите инструменты"))
    l = Label([20, 70, 100, 40], "Левое поле - избранное, правое поле - ожидание")
    button = Button([500, 400, 140, 30], "Продолжить")
    global index
    y = 120
    for i in index:
        gui.add_element(Flash([20, y, 140, 40], i))
        y += 50
    active = ''
    instruments = set()
    favourite = set()
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            gui.get_event(event)
            button.get_event(event)
            if button.pressed:
                while len(gui.elements) > 6:
                    if gui.elements[6].pressed1:
                        instruments.add(gui.elements[6].text)
                        try:
                            favourite.remove(gui.elements[6].text)
                        except:
                            pass
                    if gui.elements[6].pressed2:
                        favourite.add(gui.elements[6].text)
                    del gui.elements[6]
                if len(favourite):
                    a = favour(favourite)
                    instruments = instruments.union(a)
                return instruments
        for elem in gui.elements[1:6]:
            if elem.active and elem != active:
                active = elem
                text = index[elem.text]
                y = 120
                while len(gui.elements) > 6:
                    if gui.elements[6].pressed1:
                        instruments.add(gui.elements[6].text)
                        try:
                            favourite.remove(gui.elements[6].text)
                        except:
                            pass
                    if gui.elements[6].pressed2:
                        favourite.add(gui.elements[6].text)
                    del gui.elements[6]
                for i in text:
                    gui.add_element(CheckBox2([170, y, 150, 30], i))
                    y += 40

        gui.render(Surface)
        l.render(Surface)
        button.render(Surface)
        pygame.display.update()
        gui.update()


def table():
    Surface = pygame.display.set_mode((650, 450))
    gui = GUI()
    gui.add_element(Label([80, 20, 100, 30], "Данные приведены за месяц тестирования бота"))
    gui.add_element(Label([80, 60, 100, 30], "Тест проводился по 5 позициям"))
    gui.add_element(Label([60, 100, 150, 40], "Без закрытия"))
    gui.add_element(Label([240, 100, 150, 40], "На выходные"))
    gui.add_element(Label([440, 100, 150, 40], "На ночь"))
    gui.add_element(Label([70, 150, 10, 40], "8937$"))
    gui.add_element(Label([250, 150, 10, 40], "8896$"))
    gui.add_element(Label([450, 150, 10, 40], "8813$"))

    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.draw.line(Surface, (0, 0, 0), [227, 100], [227, 400], 2)
        pygame.draw.line(Surface, (0, 0, 0), [420, 100], [420, 400], 2)
        pygame.draw.line(Surface, (0, 0, 0), [40, 150], [600, 150], 2)
        gui.render(Surface)
        pygame.display.update()


def compared():
    gui = GUI()
    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([80, 20, 100, 30], "За перенос позиции через ночь биржа берет комиссию"))
    gui.add_element(Label([80, 60, 100, 30], "В выходные дни биржа не торгуется, но комиссия снимается"))
    gui.add_element(Label([60, 100, 150, 40], "Без закрытия"))
    gui.add_element(Label([240, 100, 150, 40], "На выходные"))
    gui.add_element(Label([440, 100, 150, 40], "На ночь"))
    gui.add_element(Label([50, 150, 150, 30], "Комиссия снимается"))
    gui.add_element(Label([50, 180, 150, 30], "каждую ночь"))
    gui.add_element(Label([229, 150, 150, 30], "Комиссия снимается за"))
    gui.add_element(Label([235, 180, 150, 30], "ночи между буднями"))
    gui.add_element(Label([430, 150, 150, 30], "Комиссия не снимается"))
    gui.add_element(Label([235, 220, 150, 30], "Есть риск пропустить"))
    gui.add_element(Label([235, 250, 150, 30], "выгодную сделку"))
    gui.add_element(Label([235, 280, 150, 30], "в понедельник"))
    gui.add_element(Label([430, 220, 150, 30], "Есть риск пропустить"))
    gui.add_element(Label([430, 250, 150, 30], "выгодную сделку"))
    gui.add_element(Label([430, 280, 150, 30], "утром"))
    button = Button([30, 400, 85, 40], "Назад")
    static = Button([450, 400, 150, 40], "Статистика")
    pygame.draw.line(Surface, (0, 0, 0), [200, 100], [200, 400])
    while True:
        Surface.fill(pygame.Color('yellow'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button.get_event(event):
                return

            if static.get_event(event):
                table()

        pygame.draw.line(Surface, (0, 0, 0), [227, 100], [227, 400], 2)
        pygame.draw.line(Surface, (0, 0, 0), [420, 100], [420, 400], 2)
        pygame.draw.line(Surface, (0, 0, 0), [40, 210], [600, 210], 2)
        static.render(Surface)
        button.render(Surface)
        gui.render(Surface)
        pygame.display.update()


def set_mode():
    gui = GUI()
    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([100, 20, 100, 40], "Выберите инструменты"))
    compare = Button([50, 400, 130, 40], "Сравнить")
    var1 = Button([100, 100, 500, 45], "Не закрывать позиции")
    var2 = Button([100, 200, 500, 45], "Закрывать позиции на выходные")
    var3 = Button([100, 300, 500, 45], "Закрывать позиции на ночь")

    while True:
        Surface.fill(pygame.Color('yellow'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if var1.get_event(event):
                    return 1
                elif var2.get_event(event):
                    return 2
                elif var3.get_event(event):
                    return 3
                elif compare.get_event(event):
                    compared()

        gui.render(Surface)
        var1.render(Surface)
        var2.render(Surface)
        var3.render(Surface)
        compare.render(Surface)
        pygame.display.update()
        gui.update()


def login():
    gui = GUI()
    l = Label([10, 230, 150, 30], "")
    def check(login, password):
        global Data
        for user in Data:
            for Login in user:
                if Login == login:
                    if user[Login]['password'] == password:
                        l.font_color = pygame.Color("green")
                        l.text = "Добро пожаловать"
                        l.render(Surface)
                        pygame.display.update()
                        return Login
            l.font_color = pygame.Color("red")
            l.text = "Неверный логин или пароль"
            l.render(Surface)
            pygame.display.update()
            time.sleep(2)


    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([100, 100, 100, 40], "Логин:"))
    gui.add_element(TextBox([100, 150, 200, 40], ""))
    gui.add_element(Label([100, 200, 100, 40], "Пароль:"))
    gui.add_element(TextBox([100, 250, 200, 40], "", secret=True))
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if gui.elements[1].text != "" and gui.elements[3].text2 != "":
                    res = check(gui.elements[1].text, gui.elements[3].text2)
                    if res:
                        return res
            gui.get_event(event)

        gui.render(Surface)
        pygame.display.update()
        gui.update()



def delete_list(instruments):
    gui = GUI()
    Surface = pygame.display.set_mode((650, 450))
    #gui.add_element(Label([100, 20, 100, 40], "Выберите инструменты"))
    l = Label([20, 70, 100, 30], "Если вы подтверждаете удаление, акция будет продана по нынешней цене")
    l.font_color = pygame.Color("red")
    button = Button([500, 400, 140, 30], "Удалить")
    delete = set()
    y = 120
    inst = list(instruments.keys())
    for i in range(0, len(inst), +2):
        gui.add_element(CheckBox([50, y, 100, 30], inst[i]))
        y += 35
    y = 120
    for i in range(1, len(inst), +2):
        gui.add_element(CheckBox([200, y, 100, 30], inst[i]))
        y += 35
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            gui.get_event(event)
            button.get_event(event)
            if button.pressed:
                while len(gui.elements) > 1:
                    if gui.elements[1].pressed:
                        delete.add(gui.elements[1].text)
                    del gui.elements[1]
                return delete

        gui.render(Surface)
        l.render(Surface)
        button.render(Surface)
        pygame.display.update()
        gui.update()


def change(new_login, user):
    Surface = pygame.display.set_mode((650, 450))
    token = Button([120, 260, 320, 60], "Изменить token")
    work = Button([120, 190, 470, 60], "Изменить режим работы")
    password = Button([120, 120, 330, 60], "Изменить пароль")
    log = Button([120, 50, 320, 60], "Изменить логин")
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {new_login: user}
                pygame.quit()
                sys.exit()

            if token.get_event(event):
               user["token"] = set_token()

            if work.get_event(event):
                user["mode"] = set_mode()

            if password.get_event(event):
                user["password"] = set_password()

            if log.get_event(event):
                new_login = set_login()

        token.render(Surface)
        work.render(Surface)
        password.render(Surface)
        log.render(Surface)
        pygame.display.update()

new_user = {}
def main():
    if start():
        global new_user
        set_login()
        set_password()
        set_token()
        for i in new_user:
            new_user[i]['mode'] = set_mode()
        a = list(set_list())
        k = {}
        for i in a:
            k[i] = 0
        for i in new_user:
            new_user[i]['instruments'] = k
        global Data
        Data.append(new_user)
        jData = json.dumps({"users": Data})
        with open("data.json", 'w') as file:
            file.write(jData)
        for Login in new_user:
            return Login
    else:
        return login()


def get_interval():
    Surface = pygame.display.set_mode((550, 450))
    day = Button([100, 100, 400, 70], "По дням")
    week = Button([100, 200, 400, 70], "По неделям")
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if day.get_event(event):
                return 1

            if week.get_event(event):
                return 2

        day.render(Surface)
        week.render(Surface)
        pygame.display.update()



def get_period():
    Surface = pygame.display.set_mode((550, 450))
    week = Button([100, 100, 400, 50], "За неделю")
    month = Button([100, 200, 400, 50], "За месяц")
    all_time = Button([100, 300, 400, 50], "За всё время")
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if week.get_event(event):
                return [1, get_interval()]

            if month.get_event(event):
                return [2, get_interval()]

            if all_time.get_event(event):
                return [3, get_interval()]

        week.render(Surface)
        month.render(Surface)
        all_time.render(Surface)
        pygame.display.update()


def reporting():
    Surface = pygame.display.set_mode((550, 450))
    balance = Button([100, 100, 300, 70], "Баланс")
    deal = Button([100, 200, 300, 70], "Сделки")
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if balance.get_event(event):
                show_balance(get_period())

            if deal.get_event(event):
                show_deal()


        balance.render(Surface)
        deal.render(Surface)
        pygame.display.update()

def get_per():
    Surface = pygame.display.set_mode((550, 450))
    day = Button([100, 100, 500, 50], "За день")
    week = Button([100, 200, 500, 50], "За неделю")
    month = Button([100, 300, 500, 50], "За месяц")
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if day.get_event(event):
                return 1

            if week.get_event(event):
                return 2

            if month.get_event(event):
                return 3

        week.render(Surface)
        month.render(Surface)
        day.render(Surface)
        pygame.display.update()

def show_deal():
    Surface = pygame.display.set_mode((550, 450))
    gui = GUI()
    gui.add_element(Label([100, 50, 100, 40], "Введите адрес, куда сохранить файл"))
    adress = TextBox([100, 150, 200, 40], "")
    flag = True
    while flag:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if adress.text != "":
                    res = adress.text
                    if res:
                        flag = False
                        break
            adress.get_event(event)

        adress.render(Surface)
        gui.render(Surface)
        pygame.display.update()
    adress = res + "\\deal.txt"
    with open(adress, 'w') as file:
        period = get_per()
        period = get_per()
        period = get_per()
        data = open('statistic.json')
        data = json.load(data)['deals']
        if period == 1:
            res = [data[-1]]
            i = -2
            while  res[-1][0] - data[i][0] < 86400:
                res.insert(0, data[i])
                i -= 1

        elif period == 2:
            res = [data[-1]]
            i = -2
            while res[-1][0] - data[i][0] < 604800:
                res.insert(0, data[i])
                i -= 1
        elif period == 3:
            res = [data[-1]]
            i = -2
            while res[-1][0] - data[i][0] < 2592000:
                res.insert(0, data[i])
                i -= 1
        s = ""
        for i in range(len(res)):
            s += time.ctime(res[0]) + '\t'
            s += '\t'.join(res[1:i]) + '\n'
        file.write(s)
    return

def show_balance(params):
    Surface = pygame.display.set_mode((550, 450))
    graph = Button([100, 100, 350, 60], "График")
    text = Button([100, 200, 350, 60], "Текст")
    while True:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if graph.get_event(event):
                show_graph(params)

            if text.get_event(event):
                show_text(params)

        graph.render(Surface)
        text.render(Surface)
        pygame.display.update()

def show_text(params):
    Surface = pygame.display.set_mode((550, 450))
    gui = GUI()
    gui.add_element(Label([100, 50, 100, 40], "Введите адрес, куда сохранить файл"))
    adress = TextBox([100, 150, 200, 40], "")
    flag = True
    while flag:
        Surface.fill(pygame.Color('yellow'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if adress.text != "":
                    res = adress.text
                    if res:
                        flag = False
                        break
            adress.get_event(event)

        adress.render(Surface)
        gui.render(Surface)
        pygame.display.update()
    adress = res + "\\balance.txt"
    with open(adress, 'w') as file:
        period, interval = params
        data = open('statistic.json')
        data = json.load(data)['balance']
        if period == 1:
            data = data[-7:]
        elif period == 2:
            data = data[-30:]
        if interval == 2:
            data = data[::7]
        x = [i[0] for i in data]
        y = [i[1] for i in data]
        s = ""
        for i in range(len(data)):
            s += x[i] + '    ' + str(y[i]) + '\n'
        file.write(s)
    return


def show_graph(params):
    period, interval = params
    data = open('statistic.json')
    data = json.load(data)['balance']
    start1 = time.time()
    x = [time.ctime(i) for i in range(int(time.time()) - 86400 * 30, int(time.time()), 86400)]
    if period == 1:
        data = data[-7:]
        x = [time.ctime(i) for i in range(int(time.time())-86400*7, int(time.time()), 86400)]
    elif period == 2:
        data = data[-30:]
        x = [time.ctime(i) for i in range(int(time.time())-86400*30, int(time.time()), 86400)]
    if interval == 2:
        data = data[::7]
        x = x[::+7]
    #x = [i[0] for i in data]
    y = [i for i in data]
    #x = [time.ctime(i) for i in range(time.time(), time.time(), 86400)]
    #y = [i for i in data]
    if (len(x) > len(y)):
        if len(y):
            x = x[-len(y)::]
        else:
            x = []

    matplotlib.use("Agg")
    fig = pylab.figure(figsize=[4, 4],  # Inches
                       dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                       )
    ax = fig.gca()
    ax.plot(x, y)
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    window = pygame.display.set_mode((550, 450))
    screen = pygame.display.get_surface()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
