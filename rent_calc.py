import pandas as pd


price_table = pd.read_csv('D:/code/telegram_bot/locate_price_2023.csv', index_col=0)


apart_N = 'N'
year = '2023'
sep = '-'
mistakes_list = [['29', '02'],
                 ['30', '02'],
                 ['31', '02'],
                 ['31', '04'],
                 ['31', '06'],
                 ['31', '09'],
                 ['31', '11']]


def guest_arrival(date_in):
    result = ''
    date_list = date_in.split('.')

    try: 
        if date_list in mistakes_list:
            result ='Несуществующая дата!'
        elif 1 <= int(date_list[0]) <= 31 and 1 <= int(date_list[1]) <= 12:
            result = 'ok'
        else:
            result = "Ошибка! Введите дату корректно!"
    except ValueError:
        result = "Несуществующая дата!"
    except IndexError:
        result = "Ошибка! Введите дату корректно!"

    return result


def guest_departure(date_in):
    result = ''
    date_list = date_in.split('.')

    try: 
        if date_list in mistakes_list:
            result ='Несуществующая дата!'
        elif 1 <= int(date_list[0]) <= 31 and 1 <= int(date_list[1]) <= 12:
            result = 'ok'
        else:
            result = "Ошибка! Введите дату корректно!"
    except ValueError:
        result = "Несуществующая дата!"
    except IndexError:
        result = "Ошибка! Введите дату корректно!"

    return result

def appart_number(number_in):
    result = ''

    try:
        if int(number_in) in range(1,9):
            result = 'ok'
        else:    
            raise ValueError
    except ValueError:
        print('выберите номер от 1 до 8')
    
    return result

def discount(number_in):
    result = ''
    
    try:
        if 0 <= int(number_in) <=100:
            result = "ok"
    except ValueError:
        result = 'Введите число от 0 до 100'

    return result

def calculate(arriv, dep, apart, discount):
    
    arrival = year + sep + arriv[1] + sep + arriv[0]
    departure = year + sep + dep[1] + sep + dep[0]
    apartment = apart_N + apart
    period = price_table[apartment].loc[arrival: departure]
    period = period[:-1]
    price = period.sum()*(1-discount/100)

    result = (f"Стоимоть проживания: {price} RUB, скидка {discount} %: {period.sum()-price} RUB    ",
              f"Расчёт стоимости проживания в апартаментах № {apart} посуточно:",
              period*(1-discount/100)) 

    return result