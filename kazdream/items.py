import scrapy


class ShoppingItem(scrapy.Item):
    name = scrapy.Field()
    articul = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    photo_urls = scrapy.Field()
