import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
	rows = csv.reader(f, delimiter=",")
	contacts_list = list(rows)

columns = len(contacts_list[0])
new_contacts_list = []
phone_pattern = re.compile(r"(\+7|8)(\s*\(?\d{3}\)?)(\s*\d*-?\d*-?\d*)(\s?\(?\w*\.?\s*\d*\)?)")


def search_for_unique_person(dup_list, unique_list):
	new_list = []
	if dup_list[0] == unique_list[0] and dup_list[1] == unique_list[1] \
		and (dup_list[2] == unique_list[2] or dup_list[2] == '' or unique_list[2] == ''):
		new_list = [''] * columns
		new_list[0:2] = dup_list[0:2]
		# Почему-то на 5 строке исходного csv-файла на 1 запятую больше, чем нужно
		if len(dup_list) == 8:
			dup_list.pop()
		for i, column in enumerate(dup_list[2:], 2):
			if dup_list[i] != unique_list[i]:
				new_list[i] = dup_list[i] + unique_list[i]
			else:
				new_list[i] = dup_list[i]
	return new_list


for row in contacts_list:

	name = ' '.join(row[0:3]).split()
	for index, item in enumerate(name):
		row[index] = item

	if row[5] and row[5] != 'phone':
		phone = phone_pattern.split(row[5])
		phone.pop(0)
		phone.pop()
		phone = list(map(str.strip, phone))
		if phone[0] == '8':
			phone[0] = '+7'
		if len(phone[1]) == 3:
			phone[1] = f'({phone[1]})'
		phone[2] = phone[2].replace('-', '')
		phone[2] = f'{phone[2][:3]}-{phone[2][3:5]}-{phone[2][5:]}'
		if phone[3]:
			phone[3] = re.search(r'\d+', phone[3]).group()
			phone[3] = ' доб.' + phone[3]
		phone = ''.join(phone)

	for row_number, new_row in enumerate(new_contacts_list.copy()):
		no_dup_row = search_for_unique_person(row, new_row)
		if no_dup_row:
			new_contacts_list.pop(row_number)
			row = no_dup_row

	new_contacts_list.append(row)

for line in new_contacts_list:
	print(', '.join(line))

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
	datawriter = csv.writer(f, delimiter=',')
	datawriter.writerows(new_contacts_list)
