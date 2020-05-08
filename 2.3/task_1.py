import psycopg2


def create_db():
	with psycopg2.connect("dbname=test_db user=test password=1234") as connection:
		with connection.cursor() as cursor:
			cursor.execute("""create table if not exists Student(
			id serial primary key not null,
			name varchar(100) not null,
			gpa numeric(10,2),
			birth timestamp with time zone);
			
			create table if not exists Course(
			id serial primary key not null,
			name varchar(100) not null);
			
			insert into course (name) values ('DevOps'), ('Java'), ('Python');
			
			create table if not exists student_course(
			id serial primary key not null,
			student_id integer references Student(id),
			course_id integer references Course(id));
			""")
	print('Таблицы Student, Course, student_course созданы.')


def add_student(student):
	name = student.get('name')
	if name is None:
		print("У студента должно быть указано имя")
		return
	gpa = student.get('gpa')
	birth = student.get('birth')
	with psycopg2.connect("dbname=test_db user=test password=1234") as connection:
		with connection.cursor() as cursor:
			cursor.execute("insert into student (name, gpa, birth) values (%s, %s, %s)", (name, gpa, birth))
	print(f'Студент {name} добавлен в базу.')


def add_students(course_id, students):
	with psycopg2.connect("dbname=test_db user=test password=1234") as connection:
		with connection.cursor() as cursor:
			for student in students:
				name = student.get('name')
				if name is None:
					name = 'Аноним'
				gpa = student.get('gpa')
				birth = student.get('birth')

				cursor.execute("""insert into student (name, gpa, birth)
				values (%s, %s, %s) returning id""", (name, gpa, birth))

				student_id = cursor.fetchone()[0]

				cursor.execute("""insert into student_course (student_id, course_id) 
				values (%s, %s)""", (student_id, course_id))

				print(f'Студент {name} добавлен в базу c id {student_id} и записан на курс с id {course_id}.')


def get_student(student_id):
	with psycopg2.connect("dbname=test_db user=test password=1234") as connection:
		with connection.cursor() as cursor:
			cursor.execute("select * from Student where id=(%s)", (student_id, ))
			response = cursor.fetchone()
			if response is not None:
				return response
			else:
				print(f'Студент с id {student_id} в базе не найден.')
				return


def get_students(course_id):
	with psycopg2.connect("dbname=test_db user=test password=1234") as connection:
		with connection.cursor() as cursor:
			cursor.execute("select name from course where id=(%s)", (course_id,))
			course_name = cursor.fetchone()[0]
			cursor.execute("select student_id from student_course where course_id=(%s)", (course_id, ))
			response = cursor.fetchall()
			students = []
			for student in response:
				student_id = student[0]
				student_name = get_student(student_id)[1]
				students.append([student_name, student_id])
	print(f'Студенты [имя, id] на курсе {course_name} (id {course_id}): {students}.')
	return course_name, students


create_db()
add_student({'gpa': '8', 'name': 'Vasya Pupkin', 'birth': '1997-01-31 09:26:56.66 +02:00'})
add_students('2', [{'name': 'Anatoly Vasserman'}, {'name': 'Georgy Pobedonocec'}])
get_student('1')
get_students('2')
