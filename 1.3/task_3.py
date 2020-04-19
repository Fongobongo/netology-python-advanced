def adv_print(*args, **kwargs):
    if kwargs.get('sep') is None:
        kwargs['sep'] = ' '
    if kwargs.get('end') is None:
        kwargs['end'] = '\n'
    output = kwargs.get('sep').join(args) + kwargs.get('end')
    kwargs.pop('end')
    if kwargs.get('start'):
        output = kwargs.get('start') + output
        kwargs.pop('start')
    else:
        output = '\n' + output
    if kwargs.get('max_line') is not None:
        limited_output = ''
        for i in range(0, len(output), kwargs.get('max_line')):
            limited_output += output[i:i+kwargs.get('max_line')] + '\n'
        output = limited_output.strip()
        kwargs.pop('max_line')
    if kwargs.get('in_file') is not None:
        with open(kwargs.get('in_file'), 'a', encoding='utf-8') as f:
            f.write(output)
            f.write('\n')
        kwargs.pop('in_file')
    print(output, **kwargs)


adv_print('AAAAAAAAAA', 'BBBBBBBBBB', 'CCCCCCCCCC', max_line=5, start='GOGOGO', in_file='somefile.txt', end='----->', sep='******')
print()
print('AAAAAAAAAA', 'BBBBBBBBBB', 'CCCCCCCCCC', end='----->', sep='******')
