
def col(text, colour):
    text = str(text)
    if colour == 'red': r = '\33[31m' + text
    elif colour == 'green': r = '\33[32m' + text
    elif colour == 'yellow': r = '\33[33m' + text
    else: r = '\33[0m' + text
    return r + '\33[0m'


def colour_status_code(status):
    if isinstance(status, int):
        if 100 <= status <= 199: return col(status, 'white')
        elif 200 <= status <= 299: return col(status, 'green')
        elif 300 <= status <= 399: return col(status, 'yellow')
        else: return col(status, 'red')
    elif isinstance(status, str):
        if status == 'BAD': return col(status, 'red')
        elif status == 'OK': return col(status, 'green')
        else: return col(status, 'yellow')
