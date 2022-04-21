# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class CastoramaPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        db_name = 'castorama'
        self.mongo_base = client.get_database(db_name)


    def process_item(self, item, spider):
        item['specifications'] = self.parse_specifications(item['attribute_label'], item['attribute_value'])
        del(item['attribute_label'])
        del(item['attribute_value'])

        collection = self.mongo_base[item['category']]
        collection.insert_one(item)
        return item


    def parse_specifications(self, labels, values):
        specifications_dict = dict(zip(labels, values))
        return specifications_dict


class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)


    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        file_path = f"{item['category']}/{item['name']}/{image_guid}.jpg"
        return file_path
