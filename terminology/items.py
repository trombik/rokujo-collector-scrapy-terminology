# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TerminologyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GlossaryJbitsItem(scrapy.Item):
    term = scrapy.Field()
    translation = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    obtained_at = scrapy.Field()
