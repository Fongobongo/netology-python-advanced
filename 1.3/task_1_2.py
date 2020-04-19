class Contact:
    def __init__(self, name, surname, phone, favorite=False, *args, **kwargs):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.favorite = favorite
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        name = f'Имя: {self.name}\n'
        surname = f'Фамилия: {self.surname}\n'
        phone = f'Телефон: {self.phone}\n'
        favorite = 'В избранных: да' if self.favorite else 'В избранных: нет'
        args = '\n\t\t' + '\n\t\t'.join(self.args) if self.args else ''
        kwargs = ''
        for key, value in self.kwargs.items():
            kwargs += f'\n\t\t{key}: ' + ''.join(str(item) for item in value)
        additional_info = f'\nДополнительная информация:\t\t{args}{kwargs}' if args or kwargs else ''
        contact = name + surname + phone + favorite + additional_info
        return contact


class PhoneBook:
    def __init__(self, title):
        self.title = title
        self.contacts = {}

    def add_contact(self, instance_name):
        self.contacts[instance_name] = Contact
        print(f'Контакт {instance_name.name} {instance_name.surname} добавлен\n')

    def print_contacts(self):
        print('Список всех контактов:\n')
        for contact in self.contacts:
            print(contact, '\n')

    def find_favorite(self):
        favorite = []
        for contact in self.contacts:
            if contact.favorite:
                favorite.append(f'{contact.name} {contact.surname} с номером {contact.phone}')
        print(f'Избранные контакты: {", ".join(favorite)}\n') if favorite else print('Избранные контакты не найдены\n')

    def find_contact(self, name, surname):
        for contact in self.contacts:
            if name == contact.name and surname == contact.surname:
                return print(f'Контакт {name} {surname} найден:\n\n{contact}\n')
        else:
            return print(f'Контакт {name} {surname} не найден', '\n')

    def delete_by_phone(self, phone):
        contacts = list(self.contacts.keys())
        for contact in contacts:
            if phone == contact.phone:
                self.contacts.pop(contact)
                print(f'Контакт {contact.name} {contact.surname} удалён из телефонной книги\n')
        if len(contacts) == len(self.contacts.keys()):
            print(f'Контакт с номером {phone} не найден в телефонной книге\n')


# Контакты
jhon = Contact('Jhon', 'Smith', '+71234567809', True, 'миллионер', 'филантроп', telegram='@jhony', email='jhony@abc.ru')
lily = Contact('Lily', 'Adams', '+79872355253', email='lily_@zzz.ru')
sam = Contact('Sam', 'Raine', '+7396264756', True)

# Название телефонной книги
new_book = PhoneBook('Коллеги')

# Добавление нового контакта
print('--------------------------------------------------------------------')
print("Добавление нового контакта")
print('--------------------------------------------------------------------\n')

new_book.add_contact(jhon)
new_book.add_contact(lily)
new_book.add_contact(sam)

# Вывод контактов из телефонной книги
print('--------------------------------------------------------------------')
print('Вывод контактов из телефонной книги')
print('--------------------------------------------------------------------\n')

new_book.print_contacts()

# Удаление контакта по номеру телефона
print('--------------------------------------------------------------------')
print('Удаление контакта по номеру телефона')
print('--------------------------------------------------------------------\n')

new_book.delete_by_phone('+71234567809')
new_book.delete_by_phone('+99999999999')

# Поиск всех избранных номеров
print('--------------------------------------------------------------------')
print('Поиск всех избранных номеров')
print('--------------------------------------------------------------------\n')

new_book.find_favorite()

# Поиск контакта по имени и фамилии
print('--------------------------------------------------------------------')
print('Поиск контакта по имени и фамилии')
print('--------------------------------------------------------------------\n')

new_book.find_contact('Lily', 'Adams')
new_book.find_contact('Ann', 'May')
