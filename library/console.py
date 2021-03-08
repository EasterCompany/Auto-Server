
def col(text, colour):
    if colour == 'red': r = '\33[31m' + text
    elif colour == 'green': r = '\33[32m' + text
    elif colour == 'yellow': r = '\33[33m' + text
    else: r = '\33[0m' + text
    return r + '\33[0m'

def colour_status_code(status):
    if status == 'BAD': return col(status, 'red')
    elif status == 'OK': return col(status, 'green')
    else: return col(status, 'yellow')
