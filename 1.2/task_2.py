import hashlib


def hash_generator(path):
    with open(path, encoding='utf-8') as some_file:
        for line in some_file:
            md5_hash = hashlib.md5(line.strip().encode('utf-8')).hexdigest()
            yield md5_hash


if __name__ == '__main__':
    for each_line in hash_generator('countries.txt'):
        print(each_line)
