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
