# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    print()
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy1804

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary(item['salary'])
            # del item['salary']
        else:
            pass
        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        min_salary_l = None
        max_salary_l = None
        currency_l = None

        if 'от ' in salary and ' до ' not in salary:
            if 'руб.' in salary:
                min_salary_l = salary[1]
                max_salary_l = None
                currency_l = 'руб.'
            if 'USD' in salary:
                min_salary_l = salary[1]
                max_salary_l = None
                currency_l = 'USD'
            if 'EUR' in salary:
                min_salary_l = salary[1]
                max_salary_l = None
                currency_l = 'EUR'
        if 'до ' in salary and 'от ' not in salary:
            if 'руб.' in salary:
                min_salary_l = None
                max_salary_l = salary[1]
                currency_l = 'руб.'
            if 'USD' in salary:
                min_salary_l = None
                max_salary_l = salary[1]
                currency_l = 'USD'
            if 'EUR' in salary:
                min_salary_l = None
                max_salary_l = salary[1]
                currency_l = 'EUR'
        if 'от ' not in salary and ' до ' not in salary and 'до ' not in salary:
            if 'руб.' in salary:
                min_salary_l = salary[0]
                max_salary_l = salary[2]
                currency_l = 'руб.'
            if 'USD' in salary:
                min_salary_l = salary[0]
                max_salary_l = salary[2]
                currency_l = 'USD'
            if 'EUR' in salary:
                min_salary_l = salary[0]
                max_salary_l = salary[2]
                currency_l = 'EUR'
        if 'от ' in salary and ' до ' in salary:
            if 'руб.' in salary:
                min_salary_l = salary[1]
                max_salary_l = salary[3]
                currency_l = 'руб.'
            if 'USD' in salary:
                min_salary_l = salary[1]
                max_salary_l = salary[3]
                currency_l = 'USD'
            if 'EUR' in salary:
                min_salary_l = salary[1]
                max_salary_l = salary[3]
                currency_l = 'EUR'
        return min_salary_l, max_salary_l, currency_l
