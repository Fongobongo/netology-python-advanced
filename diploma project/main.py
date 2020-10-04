from parameters.constants import constant, today, weights
from search_engine.search_options import options, my_favorites, minimum_favorites
from search_engine import search
from my_exceptions import errors
from datetime import datetime, timedelta
from decimal import Decimal
import requests
import psycopg2
import time
import re


def get_response_without_error(url, params):

    repeat = True
    response = None
    retry = 5

    while repeat:

        try:
            response = requests.get(url, params=params).json()

            if 'error' in response and 'error_code' in response['error'] and response['error']['error_code'] == 6:
                print('Эта кобыла не может гнать так быстро, дадим ей передохнуть хотя бы пару секунд')
                time.sleep(2)
            else:
                repeat = False
        except requests.exceptions.ReadTimeout:
            if retry > 0:
                print(f'Сервер не отправил данные. Попробуем снова через 10 секунд. Осталось попыток: {retry}')
                retry -= 1
                time.sleep(10)
            else:
                raise errors.ServerErrorException

    return response


def get_main_user_vk_id():

    url = f'https://api.vk.com/method/users.get?PARAMETERS'

    params = {
        'access_token': constant['TOKEN'],
        'user_ids': constant['USERNAME'],
        'v': '5.122'
    }

    print(f"Запрашиваем VK ID у пользователя {constant['USERNAME']}")
    response = get_response_without_error(url, params)

    if 'error' in response and 'error_code' in response['error'] and response['error']['error_code'] == 113:
        print(f"Пользователь {constant['USERNAME']} не найден среди пользователей VK")
        return
    elif 'error' in response and 'error_code' in response['error'] and response['error']['error_code'] == 5:
        print(f"Неверный токен")
        return
    elif 'error' in response:
        print(f"При запросе VK ID {constant['USERNAME']} что-то пошло не так")
        return

    vk_id = response.get('response')[0].get('id')
    print(f"VK ID у пользователя {constant['USERNAME']} получен: {vk_id}")

    return vk_id


def get_city_id(name):

    url = 'https://api.vk.com/method/database.getCities?PARAMETERS'

    params = {
        'access_token': constant['TOKEN'],
        'country_id': 1,
        'q': name,
        'v': '5.110'
    }

    response = get_response_without_error(url, params)

    city_id = None

    if response.get('response') and response.get('response').get('count') >= 1:

        for city in response.get('response').get('items'):

            if city['title'] == options['city']:

                city_id = city['id']
                break

    if city_id is None:
        city_id = 1

    return city_id


class User:

    def __init__(self, vk_id, user_info=''):

        self.vk_id = vk_id
        self.groups = self.common_groups = None
        self.common_groups_count = self.rating = 0
        self.common_interests = dict()

        if user_info:
            self.user_info = user_info
        else:
            self.user_info = self.get_user_info()

    def get_user_info(self):

        url = f'https://api.vk.com/method/users.get?PARAMETERS'

        params = {
            'access_token': constant['TOKEN'],
            'user_id': self.vk_id,
            'fields': 'sex, bdate, city, movies, music, books, games, interests, last_seen',
            'v': '5.122'
        }

        response = get_response_without_error(url, params)
        self.user_info = response.get('response')[0]

        return self.user_info

    def count_age(self):

        birthday = self.user_info.get('bdate')
        user_bdate = datetime.strptime(birthday, '%m.%d.%Y')
        user_age = today.year - user_bdate.year - ((today.month, today.day) > (user_bdate.month, user_bdate.day))

        return user_age

    def get_friends_list(self):

        url = f'https://api.vk.com/method/friends.get?PARAMETERS'

        params = {
            'access_token': constant['TOKEN'],
            'user_id': self.vk_id,
            'v': '5.110'
        }

        response = get_response_without_error(url, params=params)

        if 'error' in response and 'error_code' in response['error'] and response['error']['error_code'] == 15:
            raise errors.PrivateUserException

        if 'error' in response and 'error_code' in response['error'] and response['error']['error_code'] == 18:
            raise errors.UserDeletedException

        friends_list = response.get('response').get('items')

        self.friends = friends_list

        return friends_list

    def get_groups_dict(self):
        url = f'https://api.vk.com/method/groups.get?PARAMETERS'

        params = {
            'access_token': constant['TOKEN'],
            'user_id': self.vk_id,
            'count': 1000,
            'extended': 1,
            'v': '5.124'
        }

        response = get_response_without_error(url, params)

        groups_dict = {}

        if response.get('response').get('count'):

            groups_list = response.get('response').get('items')

            for group in groups_list:
                groups_dict.update({group.get('id'): group.get('name')})

        self.groups = groups_dict

        return groups_dict


def search_for_couple(user):

    user_info = user.get_user_info()

    sex = options['sex']

    if not sex:
        user_sex = user_info.get('sex')

        if user_sex == 2:
            sex = 1

        elif user_sex == 1:
            sex = 2

        else:
            sex = 0

    age_from = options['age_from']
    age_to = options['age_to']

    user_age = main_user.count_age()

    if not age_from and user_age:
        age_from = user_age

    if not age_to and user_age:
        age_to = user_age

    age_delta = age_to - age_from

    if options['city']:
        city_id = get_city_id(options['city'])

    elif options['city'] is None and user_info.get('city'):
        city_id = user_info.get('city').get('id')

    else:
        city_id = 1
    url = f'https://api.vk.com/method/users.search?PARAMETERS'

    params = {
        'access_token': constant['TOKEN'],
        'count': 1000,
        'sort': 1,
        'has_photo': 1,
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to,
        'city': city_id,
        'fields': 'sex, bdate, city, movies, music, books, games, interests, last_seen, relation, common_count',
        'v': '5.110'
    }

    response = get_response_without_error(url, params)
    # if response.get('response'):
    #     count = response.get('response').get('count')
    #     if count > 1000:
    #
    #         ages_amount = age_delta + 1
    #         per_year_amount = count / ages_amount
    #
    #         print(f"Найдено человек: {count}, количество возрастов: {ages_amount}, человек за год: {per_year_amount}")
    #
    #         if per_year_amount > 0:
    #
    #             start_year = today.year - age_to - 1
    #             end_year = today.year - age_from
    #             month = '%02d' % today.month
    #
    #             print(f"Ищем по каждому месяцу всех возрастов: c {month}.{start_year} по {month}.{end_year}")
    #
    #             result = response.get('response').get('items')
    #
    #     else:
    #         result = response.get('response').get('items')

    # print(response)
    # repeat = True
    # response = None
    # retry = 3
    # bonus_time = 0
    #
    # while repeat:
    #
    #     # print(f"Ищем подходящую пару для пользователя {constant['USERNAME']}")
    #     response = get_response_without_error(url, params)
    #     print(response)
    #
    #     if response.get('response') and response['response'].get('count') == 0 and retry > 0:
    #         print(f"Эта кобыла не может гнать так быстро, дадим ей передохнуть {60 + bonus_time} секунд")
    #         time.sleep(60 + bonus_time)
    #         retry -= 1
    #         bonus_time += 30
    #     else:
    #         repeat = False
    #         continue
    #
    # result = response.get('response').get('items')
    # # result_count = len(result)
    # # print(f"Найдено {result_count} результатов")

    result = response.get('response').get('items')
    print(f"Найдено {len(result)} результатов")

    return result


def write_results_to_db(search_results):
    pass


def filter_search_results(search_results):

    results_count = len(search_results)

    filtered_results = []

    for item in search_results:

        # Убираем из результатов поиска скрытые профили
        if item.get('is_closed') and item.get('can_access_closed') is False:
            # print(f'{item} закрытый профиль')
            continue

        # Фильтруем пользователей, которые не появлялись онлайн более options['last_seen'] (по умолчанию: 30 дней)
        if item.get('last_seen'):
            timestamp = item.get('last_seen').get('time')
            last_seen = datetime.fromtimestamp(timestamp).date()
            timedelta = (today - last_seen).days
        else:
            # print(f'{item} не содержит информации о последнем входе')
            continue

        if timedelta > options['last_seen']:
            # print(f'{item} был в сети {timedelta} дней назад')
            continue

        # Удаляем ключи с пустыми значениями
        new_item = dict((k, v) for k, v in item.items() if v)

        # Если у пользователя не заполнен ни один интерес из списка, не включаем его в итоговый результат
        if new_item.keys() & {'movies', 'music', 'books', 'games', 'interests'}:
            filtered_results.append(new_item)

    filtered_result_count = len(filtered_results)
    print(f"Отфильтровано {results_count - filtered_result_count} пользователей, осталось {filtered_result_count}")

    return filtered_results


def create_users_dict(search_results):

    users_dict = {}

    for user in search_results:
        new_user = {user.get('id'): User(user.get('id'), user)}
        users_dict.update(new_user)
    return users_dict


def get_25_vk_ids_for_execute(users_dict):

    users_list = list(users_dict.keys())

    users_amount = len(users_list)

    current_user = 0

    vk_ids_for_execute = []

    while current_user < users_amount:
        vk_ids_25 = []

        for user in users_list[current_user:current_user + 25]:
            vk_ids_25.append(user)

        vk_ids_for_execute.append(vk_ids_25)

        current_user += 25

    return vk_ids_for_execute


def get_groups(vk_ids_in_25_per_pack, users_dict):
    amount_of_executes = len(vk_ids_in_25_per_pack)

    iteration = 0

    result = []

    while iteration < amount_of_executes:
        for pack in vk_ids_in_25_per_pack:
            pack_length = len(pack)
            execute_code = """var groups = [];
                            var index = 0;
                            var end = %s;
                            var pack = %s;
                            while (index < end) {
                            var user_id = pack[index];
                            var result = API.groups.get({"user_id":user_id});
                            result = {"user_id": user_id} + result;
                            groups = groups + [result];
                            index = index + 1;
                            };
                            return groups;""" % (pack_length, pack)

            response = get_response_without_error('https://api.vk.com/method/execute?PARAMETERS', dict(code=execute_code, v='5.110', access_token=constant['TOKEN']))

            result += response.get('response')

            iteration += 1

            if iteration % 3 == 0:
                time.sleep(1)

    for user in result:
        if isinstance(user, dict) and user.get('user_id'):
            id = user.get('user_id')
            users_dict.get(id).groups = set(user.get('items'))

    return result


def find_common_groups(user, users):

    main_user_groups = set(user.groups.keys())

    for current_user in users.values():
        common_groups = main_user_groups.intersection(current_user.groups)
        if common_groups:
            current_user.common_groups = common_groups
            current_user.common_groups_count = len(common_groups)


def count_rating(user, users):

    count = 0

    pattern = re.compile('[^\w\d\s.,]')

    main_user_favorites = my_favorites

    for key, value in my_favorites.copy().items():

        if user.user_info.get(key):
            if value:
                criteria_value = value + ", " + user.user_info.get(key)
                main_user_favorites.update({key: criteria_value})
            else:
                main_user_favorites.update({key: user.user_info.get(key)})

        if main_user_favorites.get(key):
            count += 1
            filtered_string = re.sub(pattern, '', main_user_favorites.get(key)).replace(", ", ",")
            criteria_value = set(x.lower().strip() for x in filtered_string.split(","))
            main_user_favorites.update({key: criteria_value})
        else:
            main_user_favorites.pop(key)

    if count < minimum_favorites:
        raise errors.NotEnoughFavorites(count)

    for current_user in users.values():
        current_user_favorites = dict()
        for key in main_user_favorites.keys():
            if current_user.user_info.get(key):
                filtered_string = re.sub(pattern, '', current_user.user_info.get(key)).replace(", ", ",")
                current_user_favorites[key] = set(x.lower().strip() for x in filtered_string.split(","))
                common_interest = main_user_favorites.get(key).intersection(current_user_favorites.get(key))
                if common_interest:
                    current_user.common_interests.update({key: common_interest})
                    current_user.rating += len(common_interest) * weights.get(key, 1)

        current_user.rating += current_user.user_info.get('common_count', 0) * weights.get('friends', 1)
        current_user.rating += current_user.common_groups_count * weights.get('groups')


def get_top_users(users):

    users_rating = dict()

    for user in users.values():
        users_rating.update({user.vk_id: user.rating})

    users_rating = {k: v for k, v in sorted(users_rating.items(), key=lambda item: item[1], reverse=True)}

    print("Рейтинг пользователей: ", users_rating)

    return users_rating


def write_users_to_db(users):
    with psycopg2.connect("dbname=vk_users user=test password=1234") as connection:
        with connection.cursor() as cursor:
            cursor.execute("""create table if not exists users(
    		id serial primary key not null,
    		vk_id numeric(10),
    		rating numeric(10,2),
    		user_info varchar(65534),  
    		time timestamp with time zone);
            """)

    now = datetime.now()

    for user in users.items():

        vk_id = vars(user[1]).get('vk_id')
        rating = vars(user[1]).get('rating')
        user_info = str(vars(user[1]))

        with psycopg2.connect("dbname=vk_users user=test password=1234") as connection:
            with connection.cursor() as cursor:
                cursor.execute("insert into users (vk_id, rating, user_info, time) values (%s, %s, %s, %s)",
                (vk_id, rating, user_info, now))


def read_from_db():

    users_dict_from_db = {}

    with psycopg2.connect("dbname=vk_users user=test password=1234") as connection:
        with connection.cursor() as cursor:
            cursor.execute("select vk_id, user_info from users")
            response = cursor.fetchone()

            if isinstance(response[0], tuple):
                for user in response:
                    users_dict_from_db.update({int(user[0]): User(int(user[0]), user[1])})
            elif isinstance(response[0], Decimal):
                users_dict_from_db.update({int(response[0]): User(int(response[0]), response[1])})

    return users_dict_from_db


if __name__ == '__main__':
    try:

        main_user_vk_id = get_main_user_vk_id()
        main_user = User(main_user_vk_id)

        results = search_for_couple(main_user)

        write_results_to_db(results)

        # Фильтруем пользователей со скрытыми профилями, не заходивших более 30 дней и с незаполненными интересами
        filtered_results = filter_search_results(results)

        users_dict = create_users_dict(filtered_results)

        vk_ids_for_execute = get_25_vk_ids_for_execute(users_dict)

        if main_user.get_groups_dict():
            get_groups(vk_ids_for_execute, users_dict)
            find_common_groups(main_user, users_dict)

        count_rating(main_user, users_dict)

        get_top_users(users_dict)

        write_users_to_db(users_dict)

        read_from_db()

    except errors.ServerErrorException:
        print('Не удалось получить ответ. Сервер недоступен')
    except errors.NotEnoughFavorites as e:
        print(f"Указано мало интересов - {e.count}, требуется указать еще минимум {minimum_favorites-e.count}")
#     except PrivateUserException:
#         print('Нет доступа к профилю этого пользователя')
#     except UserDeletedException:
#         print('Такого пользователя не существует, либо он был забанен')
