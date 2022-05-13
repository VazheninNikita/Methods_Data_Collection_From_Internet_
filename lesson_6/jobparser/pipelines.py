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
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_hhru(item['salary'])
            # del item['salary']
        else:
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_sjru(item['salary'])
            # del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def process_salary_hhru(self, salary):
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

    def process_salary_sjru(self, salary):
        min_salary_l = None
        max_salary_l = None
        currency_l = None

        if 'от' in salary:
            min_salary_l = salary[2].replace('\xa0руб.', '')
            max_salary_l = None
            currency_l = 'руб.'
        if 'до' in salary:
            min_salary_l = None
            max_salary_l = salary[2].replace('\xa0руб.', '')
            currency_l = 'руб.'
        if '—' in salary:
            min_salary_l = salary[0]
            max_salary_l = salary[4]
            currency_l = salary[6]
        if 'от' not in salary and 'до' not in salary and '—' not in salary and 'По договорённости' not in salary:
            min_salary_l = salary[0].replace('\xa0руб.', '')
            max_salary_l = salary[0].replace('\xa0руб.', '')
            currency_l = salary[2]
        return min_salary_l, max_salary_l, currency_l
