import csv
import pickle

# Определяет типы данных для заголовков таблицы на основе значений в первом ряду данных.
def start_type_header(table):
    header = table[0]
    values = table[1]
    for i in range(len(values)):
        if values[i].count('.') >= 2:
            table[0][i] = header[i] + '_datatime'  
        elif values[i].count('.') == 1 and all([alpha.isdigit() for alpha in values[i].split('.')]):
            table[0][i] = header[i] + '_float'
        else:
            if values[i].isdigit():
                table[0][i] = header[i] + '_int'  
            elif 'True' == values[i] or "False" == values[i]:
                table[0][i] = header[i] + '_bool'  
            else:
                table[0][i] = header[i] + '_str'
    return table

# Разделяет таблицу на две части по указанной строке.
def split_table(name_table, row):
    correct_row = row - 1
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = [line for line in reader]
        header = table[0]
    
    first_table = [table[i] for i in range(len(table)) if i <= correct_row]
    second_table = [header]
    for i in range(len(table)):
        if i > correct_row:
            second_table.append(table[i])
    
    save_table(first_table, f'{name_table}_first')
    save_table(second_table, f'{name_table}_second')

# Объединяет несколько таблиц в одну, проверяя совпадение заголовков.
def contact(name_table):
    big_table = []
    big_table_all = []
    for table in name_table.split(','):
        with open(f'{table}.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            now_table = [line for line in reader]
            header = now_table[0]
            if big_table:
                if big_table[0] != now_table[0]:
                    print('Данные файлы не являются одной "таблицей"')
                    break
            
            for line in now_table:
                big_table.append(line)
    
    big_table_all.append(header)
    for line in big_table:
        if line != header:
            big_table_all.append(line)

    save_table(big_table_all, table + '_contact')

# Перезаписывает таблицу в файл с расширением '.dump' в бинарном формате через pickle.
def rewrite_picle(name_table):
    with open(f'{name_table}.csv', 'r', encoding='utf-8')as f:
        reader = csv.reader(f)
        table = [line for line in reader]
    with open(f'{name_table}.dump', 'wb') as file:
        pickle.Pickler(file).dump(table)

# Добавляет значения в колонку таблицы по указанному столбцу.
def set_values(name_table, list_values, colum):
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = [line for line in reader]
        header = table[0]
        correct_colum = colum - 1
        extra_table = table
        for j in range(len(list_values)):
            now_extra_line = [' ' * len(header[0])] * len(header)
            extra_table.append(now_extra_line)
        i = -1
        j = 0
        for line in extra_table:
            i += 1
            if line[correct_colum] == ' ' * len(header[0]) and j < len(list_values):
                extra_table[i][correct_colum] = list_values[j] 
                j += 1
        comon = [' ' * len(header[0])] * len(header)
        i_table = [1 for line in extra_table if line != comon]
        extra = [extra_table[i] for i in range(len(extra_table)) if i <= (sum(i_table) - 1)]
        
        with open(f'{name_table}.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for line in extra:
                writer.writerow(line)
    rewrite_picle(name_table)

# Возвращает значения из указанного столбца.
def get_values(name_table, colum):
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        col = []
        for line in reader:
            col.append(line[colum - 1])
        return col

# Устанавливает типы данных для указанных столбцов на основе словаря.
def set_colum_types(name_table, dict_types):
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = [line for line in reader]
        for colum, typee in dict_types.items():
            now_colum = colum - 1
            if typee not in table[0][now_colum][-5:]:
                table[0][now_colum] = table[0][now_colum][:table[0][now_colum].rfind('_')] + '_' + typee
                for line in table[1:]:
                    if typee == 'str': line[now_colum] = str(line[now_colum])
                    elif typee == 'int': line[now_colum] = int(line[now_colum])
                    elif typee == 'float': line[now_colum] = float(line[now_colum])
                    elif typee == 'bool': line[now_colum] = bool(line[now_colum])

    with open(f'{name_table}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for line in table:
            writer.writerow(line)
    
    rewrite_picle(name_table)

# Возвращает типы данных столбцов в виде словаря.
def get_column_types(name_table, by_number):
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = [line for line in reader]
        header = table[0]
        dict_types = {}
        if by_number == 'True':
            for num, el_type in enumerate(header):
                dict_types[num] = el_type[el_type.rfind('_'):]
        else:
            for el_type in (header):
                dict_types[el_type] = el_type[el_type.rfind('_'):]
    return dict_types

# Возвращает строки, чьи индексы совпадают с заданными.
def get_rows_by_index(name_table, first_colum):
    first_colum = first_colum.split(', ')
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        new_table = []
        for line in reader:
            for el in first_colum:
                if line[0] == el:
                    new_table.append(line)
        return new_table

# Возвращает строки, чьи номера совпадают с заданными.
def get_rows_by_number(name_table, number_start_row, number_end_row, copy_table, if_new_table):
    number_start_row = int(number_start_row)
    number_end_row = int(number_end_row)
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        counter_row = 0
        if copy_table == 'True':
            with open(f'{if_new_table}.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for line in reader:
                    counter_row += 1
                    if number_start_row <= counter_row <= number_end_row:
                        writer.writerow(line)
            return ''
        else:
            new_writer_table = []
            for line in reader:
                counter_row += 1
                if number_start_row <= counter_row <= number_end_row:
                    new_writer_table.append(line)
            return new_writer_table
            
# Функция для вывода таблицы
def print_table(name_table):
    print('-_-_-_-_-_-_-_-_-_-_-_-_-')
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        a = list(reader)
        for line in a:
            print(*line)
    print('-_-_-_-_-_-_-_-_-_-_-_-_-') 

# Функция для загрузки таблицы из репозитория, в котором находится программа.
def load_table(name_table):
    with open(f'{name_table}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        while True:
            my_request = input('Набор команд:quit - выйти с таблицы, print - вывести таблицу, get on stroke - получание по строкам, get types - получить типы, set types - задать типы, get on index - получить по индексам, add values - дабавить значения, join - обьединить таблицы, split - разбить на две\n').lower()
            if my_request == 'quit': break
            
            if my_request == 'print':
                print_table(name_table)
            
            elif my_request == 'get on stroke':
                new_request = input('Введите номер строки начала, номер строки конца(вкл.), хотите создать новую таблицу(True\False), и если хотите новую табличу, то нозвание ее, инача просто напишите в этом параметре 0\n').split()
                tb = get_rows_by_number(name_table, new_request[0], new_request[1], new_request[2], new_request[3])# хз что делать с табличой в переменной
                print(tb)
            
            elif my_request == 'get types':
                new_request = input('Хотите вы получить пронумерованный список или нет(True\False)\n')
                print(get_column_types(name_table, new_request))
            
            elif my_request == 'set types':
                new_request = dict(input('Введите ключ(номер столбца) и значение через пробел по одному\n').split(' ') for _ in range(2))
                set_colum_types(name_table, new_request)
            
            elif my_request == 'get on index':
                new_request = input('Введите через пробел значения по первым столбцам, через запятую\n')
                print(get_rows_by_index(name_table, new_request))
            
            elif my_request == 'get column':
                new_request = int(input('Введите номер колонки(начиная с единицы)\n'))
                print(get_values(name_table, new_request))
                
            elif my_request == 'add value':
                new_request = int(input('Введите колонку(1, 2, 3...)'))
                list_val = [el for el in input('Введите список значений через пробел').split()]
                set_values(name_table, list_val, new_request)
            
            elif my_request == 'join':
                contact(input('Напишите названия таблиц через ","\n'))
            
            elif my_request == 'split':
                name, row = input('Введите название таблицы, а затем строку через ","').split(',')
                row = int(row)
                split_table(name, row)

# Функция для сохранения данных в файл таблицы.
def save_table(table, name_table):
    with open(f'{name_table}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        table = start_type_header(table)
        for line in table:
            writer.writerow(line)
            
    with open(f'{name_table}.dump', 'wb') as file:
        pickle.Pickler(file).dump(table)

# Основной цикл программы ожидает команды от пользователя и выполняет их.
while True:
    my_request = input(
        'Hапишите, что собираетесь делать с файлом (save, download) или же shutdown для выхода из системы.\n'
    ).lower()
    
    # Команда для скачивания и обработки файла
    if my_request == 'download':
        name_table = input(
            'Напишите имя файла, который вы хотите загрузить (если несколько файлов, запишите их черз ",")\n'
        )
        flag = True
        if ',' in name_table:
            big_table = []
            big_table_all = []
            for table in name_table.split(','):
                with open(f'{table}.csv', 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    now_table = [line for line in reader]
                    header = now_table[0]
                    
                    if big_table:
                        # Проверка, что таблицы совпадают по структуре
                        if big_table[0] != now_table[0]:
                            print('Данные файлы не являются одной "таблицей"')
                            flag = False
                            break
                    
                    # Добавляем строки таблицы
                    for line in now_table:
                        big_table.append(line)
            
            # Сохраняем объединённую таблицу, если всё корректно
            if flag:
                big_table_all.append(header)
                for line in big_table:
                    if line != header:
                        big_table_all.append(line)
                
                with open(f'{table}_big.csv', 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    for line in big_table_all:
                        writer.writerow(line)
                       
                load_table(table + '_big')  # Загружаем таблицу
    
        elif flag:  # Для одного файла
            load_table(name_table)

    # Команда для сохранения данных в файле
    elif my_request == 'save':
        flag = True
        name_table = input(
            'Напишите, как будет назваться ваш файл (если хотите сохранить как разбитую на файлы, то напишите название файлов через ",")\n'
        )
        
        # Сохранение нескольких файлов
        if ',' in name_table:
            big_table = []
            big_table_all = []
            for table in name_table.split(','):
                with open(f'{table}.csv', 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    now_table = [line for line in reader]
                    header = now_table[0]
                    
                    if big_table:
                        if big_table[0] != now_table[0]:
                            print('Данные файлы не являются одной "таблицей"')
                            flag = False
                            break
            
                    for line in now_table:
                        big_table.append(line)
    
            if flag:
                big_table_all.append(header)
                for line in big_table:
                    if line != header:
                        big_table_all.append(line)
                save_table(big_table_all, table + '_big')  # Сохраняем объединённую таблицу
        
        # Сохранение одного файла
        elif flag:
            table = input(
                'Введите таблицу с разграничителями между строк "," и "!" (например: sword,cost!Exskalibur,1000)\n'
            )
            normal_table = [
                [x[1:] if x[0] == ' ' else x for x in el.split(',')]
                for el in table.split('!')
            ]
            save_table(normal_table, name_table)  # Сохраняем таблицу
    
    # Завершение программы
    elif my_request == 'shutdown':
        break
    
    else:
        print('Не обнаружено такой команды в системе(')
        continue
