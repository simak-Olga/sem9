import telebot
from random import *
from telebot import types


API_TOKEN = '5753495962:AAFSuOIzlc7zBmoCgv9ls4YVdrLFi39xeWI'
bot = telebot.TeleBot(API_TOKEN)

field = []
players = {}
hod = True
finish = False


def new_field():
    field = [['_' for j in range(3)] for i in range(3)]
    return field


def print_field(field):
    text = ''
    for i in range(len(field)):
        text += '\n'+' | '.join(field[i])
    return text

# определяем игрока и чем ходит


def set_players(human):
    hod = choice([True, False])  # определили рандомно 1го игрока
    # буду считать по ходу программы, что True - это бот, False - человек
    dic = {}
    dic[hod] = ['x']  # и добавили это значение в словарь
    dic[not hod] = ['0']
    if hod == True:
        dic[hod].append('bot')
        dic[not hod].append(human)
    else:
        dic[hod].append(human)
        dic[not hod].append('bot')

    print(dic)
    return (dic, dic[hod][1], hod)


def ch_input(text):
    # убираем команду, остается 0й один элемент после разделителя пробела- это как раз строка с номером строки/столбца
    # через запятую
    text = text.split()[1:]
    try:
        pos = list(map(int, text))
        if pos[0] > 3 or pos[1] > 3 or pos[0] < 1 or pos[1] < 1:
            pos = 'Значения могут быть только от 1 до 3\nПовторите команду'
            print('Значения могут быть только от 1 до 3')
    except:
        pos = 'Некорректный ввод, повторите команду'
        print('Некорректный ввод')
    return pos


def check_win(field, elem_go):
    # проверяем по строкам через число вхождений
    for el in field:
        if el.count(elem_go) == 3:
            return True
    col_in_row = [[field[j][i]
                   for j in range(len(field))] for i in range(len(field[0]))]
# проверяем по столбцаи
    for el in col_in_row:
        if el.count(elem_go) == 3:
            return True
# проверяем главную диагональ
    find_el = 0
    for i in range(3):
        if field[i][i] == elem_go:
            find_el += 1
    if find_el == 3:
        return True
# проверяем диагональ
    if field[2][0] == elem_go and field[1][1] == elem_go and field[0][2] == elem_go:
        return True

# проверяем возможность хода в принципе
def none_hod(field):
    none_hod = False
    _pos = [(index1,index2) for index1,value1 in enumerate(field) for index2,value2 in enumerate(value1) if value2=='_']
    if _pos == None:
        none_hod = True

    return none_hod        


def ch_field(field):
    _pos = [(index1, index2) for index1, value1 in enumerate(field)
            for index2, value2 in enumerate(value1) if value2 == '_']
    print(_pos)
    pl = choice(_pos)
    return pl


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, f"Привет, {message.from_user.first_name}!\nПоиграем в крестики-нолики?!\nЖми /game")



@bot.message_handler(commands=['game'])
def game_message(message):
    global field, players, hod, finish
    finish = False
    field = new_field()
    text = print_field(field)
    bot.send_message(message.chat.id, f"Игровое поле:\n{text}")
    players, first_step, hod = set_players(message.from_user.first_name)
    bot.send_message(
        message.chat.id, f"\nЖребий выпал. Первым ходит:\n{first_step}")
    if first_step == 'bot':
        pl = ch_field(field)
        print(pl)
        bot.send_message(
            message.chat.id, f"\nbot ходит:\n{players[hod][0]} на {pl[0]+1}, {pl[1]+1}")
        field[pl[0]][pl[1]] = players[hod][0]
        text = print_field(field)
        bot.send_message(message.chat.id, f"Игровое поле:\n{text}")
        bot.send_message(message.chat.id, f'''Играйте! Вы ходите -{players[False][0]}-\nЧтобы сделать ход - введите команду: 
        '/go' №строки №столбца через пробел
        Например: "/go 2 2" - чтобы сходить в центр''')
    else:
        bot.send_message(message.chat.id, f'''Играйте! Вы ходите -{players[False][0]}-\nЧтобы сделать ход - введите команду: 
        '/go' №строки №столбца через пробел
        Например: "/go 2 2" - чтобы сходить в центр''')



@bot.message_handler(commands=['go'])
def game_message(message):
    global field, finish
    # если еще есть незанятые ячейки
    if not none_hod(field) and not finish:
        pl = ch_input(message.text)
        print(pl)
        if not isinstance(pl, list):  # если ошибка ввода - вернулась строка ошибки
            bot.send_message(message.chat.id, pl)
        else:
            if field[pl[0]-1][pl[1]-1] == '_':
                field[pl[0]-1][pl[1]-1] = players[False][0]
                text = print_field(field)
                bot.send_message(message.chat.id, f"Игровое поле:\n{text}")
                if check_win(field, players[False][0]):
                    bot.send_message(
                        message.chat.id, f"Поздравляю с выигрышем!\n-{players[False][0]}-ки победили")
                    print('Поздравляю с выигрышем!')
                    finish = True
                # после успешного хода человека всегда ходит бот и передает ход человеку, предлагая команду
                if not none_hod(field) and not finish:
                    pl = ch_field(field)

                    print(pl)
                    bot.send_message(
                        message.chat.id, f"\nbot ходит:\n{players[True][0]} на {pl[0]+1}, {pl[1]+1}")
                    field[pl[0]][pl[1]] = players[True][0]
                    text = print_field(field)
                    bot.send_message(message.chat.id, f"Игровое поле:\n{text}")
                    if check_win(field, players[True][0]):
                        bot.send_message(
                            message.chat.id, f"Bot выиграл!\n-{players[True][0]}-ки победили")
                        print('Bot выиграл!')
                        finish = True

                    if not none_hod(field) and not finish:
                        bot.send_message(message.chat.id, f'''Играйте! Вы ходите -{players[False][0]}-\nЧтобы сделать ход - введите команду: 
                        '/go' №строки №столбца через пробел
                        Например: "/go 2 2" - чтобы сходить в центр''')
                    else:
                        bot.send_message(
                            message.chat.id, f"Игра завершена\nИгровое поле:\n{text}\nНачните новую /game")
                else:
                    bot.send_message(
                        message.chat.id, f"Игра завершена\nИгровое поле:\n{text}\nНачните новую /game")

            else:
                bot.send_message(
                    message.chat.id, f'Место {pl} занято, повторите команду')
                text = print_field(field)
                bot.send_message(message.chat.id, f"Игровое поле:\n{text}")
    else:
        text = print_field(field)
        bot.send_message(
            message.chat.id, f"Игра завершена\nИгровое поле:\n{text}\nНачните новую /game")


@bot.message_handler(commands=['stop'])
def stop_message(message):
    global finish
    bot.send_message(message.chat.id, f"Ок - прекращаю игру..")
    finish = True
    bot.send_message(message.chat.id, f"Для начала новой игры выберите\n/game")


@bot.message_handler(content_types='text')
def message_reply(message):
    bot.send_message(message.chat.id, f'''{message.from_user.first_name}, пожалуйста, воспользуйтесь командами:
    /game - чтобы начать новую игру
    /go - чтобы совершить свой ход в текущей игре
    /stop - остановить игру
    ''')


bot.polling()
