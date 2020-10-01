def search_all_in_once():
	return result


def search_by_month():
	return result


def search_by_calendar(url, params):
	# 'birth_day': birth_day,
	# 'birth_month': birth_month,
	all_filtered_users = []

	daterange = pd.date_range('01.01.2020', '31.12.2020')

	for everyday in daterange:
		day = everyday.day
		month = everyday.month
		print(day, month)
		search_result = search_for_couple(main_user, day, month)
		all_filtered_users += search_result

	repeat = True
	response = None
	retry = 3
	bonus_time = 0

	while repeat:

		# print(f"Ищем подходящую пару для пользователя {constant['USERNAME']}")
		response = get_response_without_error(url, params)
		print(response)

		if response.get('response') and response['response'].get('count') == 0 and retry > 0:
			print(f"Эта кобыла не может гнать так быстро, дадим ей передохнуть {60 + bonus_time} секунд")
			time.sleep(60 + bonus_time)
			retry -= 1
			bonus_time += 30
		else:
			repeat = False
			continue

	result = response.get('response').get('items')

	return result
