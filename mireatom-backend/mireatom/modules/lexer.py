import json

var_dict = {}; clear_var_dict = {} # Словарь для хранения индексов и имен переменных
const_dict = {}; clear_const_dict = {} # Словарь для хранения индексов и значений констант
sep_words = ['+','-','*','/','^','(',')','{','}','[',']','\\','_',' ','&',','] # Спиок слов разделителей
# Список греческих символов в Latex нотации
greek_words = ['\\alpha','\\beta','\\Gamma','\\gamma','\\Delta','\\delta','\\epsilon','\\varepsilon','\\zeta','\\eta'
    ,'\\Theta','\\theta','\\vartheta','\\iota','\\kappa','\\varkappa','\\Lambda','\\lambda','\\mu','\\nu','\\Xi','\\xi'
    ,'\\Pi','\\pi','\\varpi','\\rho','\\varrho','\\Sigma','\\sigma','\\varsigma','\\tau','\\Upsilon','\\upsilon','\\Phi'
    ,'\\phi','\\varphi','\\chi','\\Psi','\\psi','\\Omega','\\omega']

def proc_greek_str(string):
    """
    Обрабатывает строку, заменяя все вхождения слов из списка greek_words на символ '#', и сохраняет их позиции в словарь var_dict.

    Параметры:
    -----------
    string : str
        Исходная строка, в которой будут заменены слова из списка greek_words.

    Возвращаемое значение:
    ----------------------
    str
        Обновленная строка, в которой все вхождения слов из greek_words заменены на '#'.

    Словарь:
    --------
    var_dict : dict
        Словарь, где ключами являются индексы в строке, а значениями — заменённые слова.
    """
    # Проход по всем словам в списке greek_words
    for word in greek_words:
        idx = string.find(word) # Находим вхождение word в строку
        while idx != -1:
            # Заменяем ключевое слово из greek_words на спец символ '#'
            string = string[:idx] + '#' + string[idx + len(word):]
            # Для каждого найденного слова сохраняем позицию в словарь var_dict
            var_dict[idx] = word
            # Находим повторное вхождение word в строку
            idx = string.find(word, idx + 1)

    return string

def proc_str(string):
    """
    Обрабатывает строку, выполняя несколько операций: заменяет буквы на '#', цифры на '@', 
    обрабатывает последовательности после обратных слэшей и удаляет повторяющиеся '@'. 
    Также выполняется замена греческих букв на специальные символы.

    Параметры:
    -----------
    string : str
        Исходная строка, которую необходимо обработать.

    Возвращаемое значение:
    ----------------------
    str
        Обработанная строка, с заменами символов и удалением повторяющихся '@'.

    Примечания:
    -----------
    - Все буквы заменяются на символ '#'.
    - Все цифры заменяются на символ '@'.
    - Последовательности после обратного слэша обрабатываются как ключевые слова.
    - Все повторяющиеся символы '@' заменяются на один символ '@'.
    - Применяется дополнительная обработка греческих букв через функцию `proc_greek_str`.
    """
    # Добавление пробела в конец строки для удобства обработки
    string += ' '
    # Инициализация обработанной строки
    proc_string = ""
    i = 0
    # Проход по строке
    while i < len(string):
        if string[i] == "\\":  # Если символ — обратный слэш
            proc_string += string[i]
            i += 1
            # Считываем последовательность после слэша до разделителя (выделяем ключевое слово)
            while i < len(string) and string[i] not in sep_words:
                proc_string += string[i]
                i += 1
            i -= 1  # Возвращаемся на 1 позицию, так как условие вышло на разделитель
        elif string[i] in sep_words or string[i] in {'f', 'd'}:  # Если символ — разделитель или 'f'/'d'
            proc_string += string[i]
        elif string[i].isalpha():  # Если символ — буква
            proc_string += '#'
        elif string[i].isdigit():  # Если символ — цифра
            proc_string += '@'
        else:  # Все остальные символы остаются без изменений
            proc_string += string[i]
        i += 1

    proc_string = proc_greek_str(proc_string).strip() # Замена греческих букв
    # Удаление повторяющихся @
    result = proc_string[0]
    for char in proc_string[1:]:
        if char != '@' or result[-1] != '@':
            result += char

    return result


def find_parts(str1, str2):
    """
    Находит все уникальные общие подстроки между двумя строками, сортирует их по длине,
    и возвращает список самых длинных подстрок, исключая подстроки, которые являются частью других.

    Параметры:
    -----------
    str1 : str
        Первая строка, в которой будут искать общие подстроки.

    str2 : str
        Вторая строка, с которой будет производиться сравнение для нахождения общих подстрок.

    Возвращаемое значение:
    ----------------------
    list
        Список уникальных самых длинных общих подстрок между строками `str1` и `str2`,
        отсортированных по длине в убывающем порядке, без подстрок, являющихся частью других.

    Примечания:
    -----------
    - Подстроки, содержащие символы из списка `key_words` (например, '#', '@'), считаются переменными и константами.
    - В процессе поиска подстроки, если одна является частью другой, то более короткая подстрока удаляется.
    - Возвращаются только уникальные подстроки, которые не являются частью других.
    """
    common_substrings = set()  # Используем set для уникальности подстрок
    # Нахождение всех схожих подстрок
    for i in range(len(str1)):
        for j in range(i + 1, len(str1) + 1):
            substring = str1[i:j]
            if substring in str2:
                common_substrings.add(substring)  # Добавляем подстроку в set
    # Сортируем список уникальных подстрок
    all_templates = sorted(common_substrings)
    
    templates = []
    max_len = 0
    # Проход по всем подстрокам для выбора самых длинных
    for i in range (len(all_templates)):
        if len(all_templates[i]) > max_len:
            # Если нашли подстроку большей длины, обновляем max_len
            max_len = len(all_templates[i])
        elif len(all_templates[i]) <= max_len:
            # Если длина подстроки равна или меньше max_len, добавляем предыдущее значение в список и обновляем max_len
            templates.append(all_templates[i - 1])
            max_len = len(all_templates[i])
    # Добавляем последний элемент, так как он не проверяется в цикле
    if len(all_templates) != 0:
        templates.append(all_templates[-1])

    templates = sorted(templates,key = len, reverse = True) # Сортируем список подстрок по длинне
    key_words = ['#','@'] # Символы, которые заменяют переменные и константы
    rm_temp = []
    # Находим строку, которая является подстокой для другой строки из списка
    # Не удаляем сразу т.к. из-за многопоточности пропускаются значения
    for el1 in templates:
        for el2 in templates:
            if (el1 != el2 and el2 in el1) or all(word not in el2 for word in key_words):
                rm_temp.append(el2)
    # Удаляем неуникальные подстроки
    for el1 in rm_temp:
        for el2 in templates:
            if el2 == el1:
                templates.remove(el2)

    return templates # Возвращаем список оставшихся строк

def make_dicts(string,str_temp):
    """
    Обрабатывает строку, создавая два словаря: один для переменных и один для констант.
    Также корректирует слова, соответствующие греческим символам, и объединяет соседние цифры в числа.

    Параметры:
    -----------
    string : str
        Входная строка, содержащая переменные, константы и другие символы.
        Строка будет обработана для создания двух словарей: для переменных и констант.

    str_temp : str
        Временная строка, которая используется для корректировки индексов переменных и констант
        и для обработки на основе символов `#` (для переменных) и `@` (для констант).

    Возвращаемое значение:
    ----------------------
    None
        Функция изменяет глобальные словари: `var_dict`, `const_dict`, `clear_var_dict`, `clear_const_dict`,
        и не возвращает значения.

    Примечания:
    -----------
    - Функция работает с глобальными словарями `var_dict`, `clear_var_dict`, `const_dict`, `clear_const_dict`.
    - Каждый символ строки обрабатывается для добавления в один из двух словарей:
        - Символы, представляющие переменные, добавляются в `var_dict`.
        - Символы, представляющие цифры, добавляются в `const_dict`.
    - После обработки строка корректируется путем объединения соседних цифр в одно число.
    - Греческие символы обрабатываются отдельно в функции `proc_greek_str`.
    """
    # Очищаем словари, для работы с разными строками
    var_dict.clear(); clear_var_dict.clear()
    const_dict.clear(); clear_const_dict.clear()
    
    string += ' '  # Добавляем пробел в конец для обработки последней переменной
    i = 0
    while i < len(string):
        if string[i] == "\\":
            # Пропускаем символы после обратного слэша
            i += 1
            while i < len(string) and string[i] not in sep_words:
                i += 1
        elif string[i] in sep_words or string[i] in {'f', 'd'}:
            # Просто пропускаем, если символ разделитель или 'f'/'d'
            i += 1
        elif string[i].isalpha():
            # Если символ буква, добавляем в var_dict
            var_dict[i] = string[i]
            i += 1
        elif string[i].isdigit():
            # Если символ цифра, добавляем в const_dict
            const_dict[i] = string[i]
            i += 1
        else:
            # Если символ не из этих категорий, пропускаем
            i += 1
    # Обработка греческих символов
    proc_greek_str(string)
    # Объединение констант в одно число, если они им являются 
    for key in sorted(const_dict, reverse=True):
        if key - 1 in const_dict:
            const_dict[key - 1] = const_dict[key - 1] + const_dict[key]
            del const_dict[key]
    # Корректировка словаря констант
    list_temp = list(str_temp) # Превращаем строку в список, удобнее в использовании
    for key in sorted(const_dict):
        for i in range (len(str_temp)):
            if list_temp[i] == '@':
                clear_const_dict[i] = const_dict[key] # Корректируем индекс
                list_temp[i] = '' # Убираем обработанный символ
                break
    # Корректировка словаря переменных
    for key in sorted(var_dict):
        for i in range (len(str_temp)):
            if list_temp[i] == '#':
                clear_var_dict[i] = var_dict[key] # Корректируем индекс
                list_temp[i] = '' # Убираем обработанный символ
                break
    
def replace_chars(template,str_temp):
    """
    Заменяет символы в шаблоне на значения переменных и констант, соответствующие их индексам в строке.

    Параметры:
    -----------
    template : str
        Шаблон, в котором будут заменены символы на соответствующие значения переменных и констант.
        Это строка, где каждый символ, попадающий в диапазон индексов переменных и констант, будет заменен.

    str_temp : str
        Строка, содержащая исходные данные, в которой будут найдены индексы вхождения шаблона.
        На основе этой строки будут выполнены замены переменных и констант в шаблоне.

    Возвращаемое значение:
    ----------------------
    str
        Строка, в которой символы шаблона были заменены на значения переменных и констант, соответствующие их индексам.

    Примечания:
    -----------
    - Функция использует глобальные словари `clear_var_dict` и `clear_const_dict`, которые содержат
      индексы и значения переменных и констант соответственно.
    - Если индекс из словаря переменных или констант попадает в диапазон подстроки шаблона, то соответствующий
      символ в шаблоне заменяется на значение из словаря.
    - Строка возвращается после всех замен, преобразованная обратно в строку из списка символов.
    """
    list_temp = list(template) # Превращаем строку в список, удобнее в использовании
    temp_idx = str_temp.find(template) # Находим индекс вхождения подстроки в строку
    temp_size = temp_idx + len(list_temp) # Находим индекс конца подстроки в строке
    # Работа с переменными
    for idx,var in clear_var_dict.items():
        if idx >= temp_idx and idx < temp_size: # Проверяем попадает ли индекс из словаря в подстроку
            list_temp[idx - temp_idx] = var # Вставляем имя переменной в список
    # Работа с константами
    for idx,const in clear_const_dict.items():
        if idx >= temp_idx and idx < temp_size: # Проверяем попадает ли индекс из словаря в подстроку
            list_temp[idx - temp_idx] = const # Вставляем значение константы в список
    
    return ''.join(list_temp) # Возвращаем список как строку

def fin_parts(string,str_temp,templates):
    """
    Обрабатывает список подстрок, заменяя символы переменных и констант на их значения, 
    используя словари с индексами переменных и констант.

    Параметры:
    -----------
    string : str
        Исходная строка, на основе которой будут созданы словари с переменными и константами.
        Эта строка используется для анализа переменных и констант в других строках.

    str_temp : str
        Строка, с уже заменёнными переменными, служит только для передачи в другую функцию

    templates : list
        Список подстрок, которые будут обработаны. Каждая подстрока будет заменена на строку, 
        где символы переменных и констант заменены на соответствующие значения из словаря.

    Возвращаемое значение:
    ----------------------
    list
        Обработанный список подстрок, в которых переменные и константы заменены на свои значения.

    Примечания:
    -----------
    - Функция использует глобальные словари `var_dict`, `const_dict`, `clear_var_dict`, и `clear_const_dict`,
      которые содержат индексы и значения переменных и констант.
    - Для каждой подстроки из списка `templates` вызывается функция `replace_chars`, которая заменяет символы
      переменных и констант на их значения.
    """
    # Формируем словари с константами и переменными и их индексами
    make_dicts(string,str_temp)
    for i in range (len(templates)):
        # Возвращаем в список подстроку, но уже с переменными и константами
        templates[i] = replace_chars(templates[i].strip(),str_temp) 
    return templates
    
def count_coef(string1,string2):
    """
    Вычисляет коэффициент схожести между двумя строками на основе общих подстрок. 
    Также возвращает информацию о позициях этих подстрок в обеих строках в формате JSON.

    Параметры:
    -----------
    string1 : str
        Первая строка для сравнения.

    string2 : str
        Вторая строка для сравнения.

    Возвращаемое значение:
    ----------------------
    str
        Строка в формате JSON, содержащая коэффициент схожести между строками и позиции общих подстрок в обеих строках.

    Примечания:
    -----------
    - Строки корректируются перед обработкой, чтобы учесть возможные специальные символы (например, `\a`, `\b` и т. д.).
    - Для вычисления коэффициента схожести используется длина общих подстрок, нормированная на длину каждой строки.
    - Функция использует другие вспомогательные функции:
      - `proc_str`: для обработки строк, замены переменных и констант.
      - `find_parts`: для нахождения общих подстрок между двумя строками.
      - `fin_parts`: для подстановки переменных и констант в общие подстроки.
    """
    replacements = {'\a':'\\a','\b':'\\b','\c':'\\c','\d':'\\d','\e':'\\e','\f':'\\f','\g':'\\g'
    ,'\h':'\\h','\i':'\\i','\j':'\\j','\k':'\\k','\l':'\\l','\m':'\\m','\n':'\\n','\p':'\\p'
    ,'\o':'\\o','\q':'\\q','\r':'\\r','\s':'\\s','\t':'\\t','\v':'\\v','\w':'\\w'
    ,'\y' : '\\y'}
    # Корректировка строк
    for old, new in replacements.items():
        string1 = string1.replace(old, new)
        string2 = string2.replace(old, new)
    # Обработка строк обезличиванием переменных
    str1, str2 = proc_str(string1).strip(),proc_str(string2).strip()
    # Нахождение общих подстрок
    templates = find_parts(str1 ,str2)
    templates_c = templates.copy()
    # Подстановка переменных и констант в подстроки
    same_parts_string1, same_parts_string2 = fin_parts(string1,str1,templates), fin_parts(string2,str2,templates_c)
    # Объявление переменных для подсчёта длинны всех подстрок
    string1_parts_len = 0; string2_parts_len = 0
    # Списки для хранения индексов подстрок в строке
    string1_list = []; string2_list = []
    # Проходимся по всем подстрокам
    for i in range (len(same_parts_string1)):
        # Заполняем переменные с длинной подстрок
        string1_parts_len += len(same_parts_string1[i].replace(" ",""))
        string2_parts_len += len(same_parts_string2[i].replace(" ",""))
        # Заполняем списки для хранения индексов
        string1_list.append(str(string1.find(same_parts_string1[i])) + ":" + str(string1.find(same_parts_string1[i]) + len(same_parts_string1[i])))
        string2_list.append(str(string2.find(same_parts_string2[i])) + ":" + str(string2.find(same_parts_string2[i]) + len(same_parts_string2[i])))
    # Вычисление коэфициента схожести
    coef = min(round(((string1_parts_len / len(string1.replace(" ","")) * 100) + (string2_parts_len / len(string2.replace(" ","")) * 100)) / 2,2),100)
    # Перевод данныъ в Json формат
    data = {
        "coefficient": coef,
        "indexes" : [{"original": first, "found" : second} for first, second in zip(string1_list,string2_list)]
    }

    json_data = json.dumps(data, indent = 4, ensure_ascii=False)
    return json_data

if __name__ == "__main__":
    # Место для формул
    latex1 = "\alpha + \beta = \gamma"
    latex2 = "\alpha + \beta + \delta = \gamma"
    
    latex1 = "\frac{\sin(x+2)}{x + 51} * 5a + \log_a{xy + 2} + \log{x + 2} + \sqrt{a}"
    latex2 = "\log{a + 2} + \sqrt{x} + \log_x{ab + 2} + 5c + \frac{\sin(a+2)}{a + 51}"

    b = count_coef(latex1,latex2)
    print(b)
    