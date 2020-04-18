import json
import requests


class CountriesIterator:

    def __init__(self, path):
        self.path = path
        with open(path, encoding='utf-8') as json_file:
            self.json_countries = json.load(json_file)
        self.start = -1
        self.end = len(self.json_countries)
        self.session = requests.Session()

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start == self.end:
            raise StopIteration
        country_name = self.json_countries[self.start].get('name').get('common')
        params = {
                "action": "opensearch",
                "format": "json",
                "limit": 500,
                "search": country_name,
        }
        response = self.session.get('https://en.wikipedia.org/w/api.php', params=params).json()
        link = response[3][0]
        pair = f'{country_name} - {link}'
        with open(f'{self.path[:-5]}.txt', 'a', encoding='utf-8') as links_file:
            links_file.write(f'{pair}\n')
        return pair


if __name__ == '__main__':
    for country in CountriesIterator('countries.json'):
        print(country)
