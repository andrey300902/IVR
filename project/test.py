import sys
from GUI import *
import json
import time

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
    b_start.bgcolor = pygame.Color("orange")
    b_reg = Button([230, 280, 205, 50], "Регистрация")
    b_reg.bgcolor = pygame.Color("orange")
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
                    continue
                if i == text:
                    l.text = "Логин уже занят"
                    f = False

        if f:
            l.font_color = pygame.Color("green")
            l.text = "Хороший логин"
            l.render(Surface)
            pygame.display.update()
            global new_user
            new_user = {text: {}}
            pygame.time.wait(2000)
            return True

    Surface = pygame.display.set_mode((650, 650))
    gui.add_element(Label([10, 10, 150, 30], "Придумайте логин:"))
    gui.add_element(Label([10, 50, 150, 30], "Логин должен сосотоять из 8 - 30 символов"))
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

    Surface = pygame.display.set_mode((650, 650))
    gui.add_element(Label([10, 10, 150, 30], "Придумайте пароль:"))
    gui.add_element(Label([10, 50, 150, 30], "Пароль должен сосотоять из 8 - 20 символов"))
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

    Surface = pygame.display.set_mode((650, 650))
    gui.add_element(Label([10, 10, 150, 30], "Войдите в свой аккаунт на oanda.com"))
    gui.add_element(Label([10, 50, 150, 30], 'Перейдите в раздел "Управление API доступом"'))
    gui.add_element(Label([10, 90, 150, 30], 'Нажмите кнопку "Generate"'))
    gui.add_element(Label([10, 130, 150, 30], "Скопирйте свой Token и вставьте в форму ниже"))
    gui.add_element(TextBox([10, 170, 300, 30], "", False))

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
    l = Label([100, 60, 100, 40], "Нажимайт любое поле")
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
                    if gui.elements[1].pressed1 or gui.elements[1].pressed2:
                        instruments.add(gui.elements[1].text)
                    del gui.elements[1]
                return instruments

        gui.render(Surface)
        l.render(Surface)
        button.render(Surface)
        pygame.display.update()


def set_list():
    gui = GUI()
    Surface = pygame.display.set_mode((650, 450))
    gui.add_element(Label([100, 20, 100, 40], "Выберите инструменты"))
    l = Label([20, 70, 100, 40], "Правое поле - ожидание, левое поле - избранное")
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
                    gui.add_element(CheckBox([170, y, 150, 30], i))
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
        for user in Data['users']:
            for Login in user:
                if Login == login:
                    if user[Login]['password'] == password:
                        l.font_color = pygame.Color("green")
                        l.text = "Добро пожаловать"
                        l.render(Surface)
                        pygame.display.update()
                        return user[Login]
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
                    if check(gui.elements[1].text, gui.elements[3].text2):
                        check(gui.elements[1].text, gui.elements[3].text2)
            gui.get_event(event)

        gui.render(Surface)
        pygame.display.update()
        gui.update()


def main():
    if start():
        global new_user
        new_user = {}
        set_login()
        set_password()
        set_token()
        new_user['mode'] = set_mode()
        new_user['instruments'] = set_list()
        global Data
        Data.append(new_user)
        jData = json.dumps(Data)
        with open("data.json", 'w') as file:
            file.write(jData)
        return new_user
    else:
        return login()


main()