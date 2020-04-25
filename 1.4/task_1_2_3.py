from datetime import datetime as dt


# Декоратор
def log_to_path(path):
    def log_decorator(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)

            if args:
                arg_params = 'с неименованными аргументами: '
                for item in args:
                    arg_params += f'"{item}"' + ', '
            else:
                arg_params = 'без неименованных аргументов, '

            if kwargs:
                kwarg_params = 'с именованными аргументами: '
                for key, value in kwargs.items():
                    kwarg_params += f'"{key}: {value}", '
            else:
                kwarg_params = 'без именованных аргументов,'

            params = arg_params + kwarg_params

            current_moment = dt.now()

            log = f'Функция "{old_function.__name__}" запустилась {current_moment.date()} в {current_moment.time()}' \
                  f' {params.strip()} вернула "{result}"\n'

            with open(path, 'a', encoding='utf-8') as f:
                f.write(log)

            return result
        return new_function
    return log_decorator


# Функция продвинутый print из задания № 3 к Лекции 1.3
@log_to_path('./log.txt')
def adv_print(*args, **kwargs):
    if kwargs.get('sep') is None:
        kwargs['sep'] = ' '
    if kwargs.get('end') is None:
        kwargs['end'] = ''
    output = kwargs.get('sep').join(args) + kwargs.get('end')
    kwargs.pop('end')
    if kwargs.get('start'):
        output = kwargs.get('start') + output
        kwargs.pop('start')
    else:
        output = '\n' + output
    if kwargs.get('max_line'):
        limited_output = ''
        for i in range(0, len(output), kwargs.get('max_line')):
            limited_output += output[i:i+kwargs.get('max_line')] + '\n'
        output = limited_output.strip()
        kwargs.pop('max_line')
    if kwargs.get('in_file'):
        with open(kwargs.get('in_file'), 'a', encoding='utf-8') as f:
            f.write(output)
            f.write('\n')
        kwargs.pop('in_file')
    print(output, **kwargs)


if __name__ == '__main__':
    adv_print('AAAAAAAAA', 'BBBBBBBBB', max_line=4, start='~~~', in_file='somefile.txt', end='------>', sep='******')
    adv_print('Hello')
    adv_print(end='_______________________')
    adv_print()