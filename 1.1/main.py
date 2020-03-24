from application.db.people import get_employees
from application.salary import calculate_salary
from datetime import datetime as dt

if __name__ == '__main__':
    print(f"Текущая дата: {dt.now().date()}")
    get_employees()
    calculate_salary()
