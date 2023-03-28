import scrapy

from kazdream.items import ShoppingItem

class ShopScrapper(scrapy.Spider):
    name = 'shopkz'

    start_urls = [
        'https://shop.kz/catalog/'
    ]
    categories = set()

    def parse(self, response):
        for product in response.css('.bx_catalog_tile_title a::attr("href")').getall():
            yield response.follow(product, callback=self.parse_page_or_categories)

    def parse_page_or_categories(self, response):
        if response.url in self.categories:
            return

        if response.css('.bx_catalog_tile_title a'):
            for product in response.css('.bx_catalog_tile_title a::attr(href)').getall():
                yield response.follow(product, callback=self.parse_page_or_categories)

        if response.css('.bx_catalog_item_title'):
            self.categories.add(response.url)

            for product_link in response.css('.bx_catalog_item_title a::attr(href)').getall():
                yield response.follow(product_link, callback=self.parse_product_data)

            next_page = response.css('.bx_blue+ .bx-blue .bx-pag-next a::attr(href)')

            if next_page:
                yield response.follow(next_page.get(), callback=self.parse_page_or_categories)

    def parse_product_data(self, response):
        product = ShoppingItem()
        product['name'] = response.css('#pagetitle::text').get().strip()   # Use .strip() to remove any characters or whitespaces from the name.
        product['articul'] = response.css('.bx-card-mark li:nth-child(1)::text').get().split()[1]

        price = response.css('.item_current_price::text').get()
        if price:
            product['price'] = price.strip().replace(' ₸', '').replace(' ', '')
        else:
            product['price'] = ''

        product['category'] = response.css('#bx_breadcrumb_1 span::text').get().strip()
        product['description'] = ''.join(response.css('.bx_item_description::text').getall()).replace('\r\n', '').strip()
        photo_urls = []
        for style in response.css('.cnt_item::attr(style)').getall():
            image_url = 'https:' + style.replace("background-image:url('", '').replace("');", '')
            image_url = image_url.replace('/100_100_1', '').replace('/resize_cache', '')
            photo_urls.append(image_url)

        product['photo_urls'] = photo_urls

        yield product
