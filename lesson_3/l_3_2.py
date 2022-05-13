from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['vacancies_db']

hh = db.hh

salary = int(input('Введите желаемую зарплату: '))


def get_vacancies(sal_input):
    req = {
        '$or': [{'vacancy_salary.min_salary': {'$gte': sal_input}}, {'vacancy_salary.max_salary': {'$gte': sal_input}}]}
    return hh.find(req)


for doc in get_vacancies(salary):
    pprint(doc)
