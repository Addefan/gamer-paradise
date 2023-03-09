import locale


def date(dt, fmt, loc=''):
    locale.setlocale(category=locale.LC_ALL, locale=loc)
    cods = 'aAwdbBmyYHIpMSfzZjUWcxX%GuV'
    convert = {sym: f'%#{sym}' for sym in cods}
    convert = fmt.maketrans(convert)
    fmt = fmt.translate(convert)
    months = {'Январь': 'января', 'Февраль': 'февраля', 'Март': 'марта', 'Апрель': 'апреля',
              'Май': 'мая', 'Июнь': 'июня', 'Август': 'августа', 'Декабрь': 'декабря',
              'Сентябрь': 'сентября', 'Октябрь': 'октября', 'Ноябрь': 'ноября', 'Июль': 'июля'}
    result = dt.strftime(fmt)
    for month in months:
        result = result.replace(month, months[month])
    return result


def cart_amount(games):
    return sum(game['price'] * game['quantity'] for game in games)


def difference(first, second):
    return list(set(first) - set(second))
