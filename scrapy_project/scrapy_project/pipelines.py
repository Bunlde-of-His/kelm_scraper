# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter

import os
import json


class JsonWriterPipeline:
    def open_spider(self, spider):
        domain = spider.start_urls[0].split('/')[2]
        directory = f"Germany/{domain}/Rental Object"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.file = open(f"{directory}/items.json", 'w', encoding='utf-8')
        self.file.write('[\n')

    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 2, 0)
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + ",\n"
        self.file.write(line)
        return item
