import scrapy
from scrapy_parse.items import AizelClothItem
from scrapy_redis.spiders import RedisSpider


class AizelClothSpider(RedisSpider):
    name = "aizel"
    # start_urls = ("https://aizel.ru/ua-ru/odezhda/bryuki/", )

    # def make_request_from_data(self, data):
    size_base_url = 'https://aizel.ru/products/sizes/?id='

    def field_format(self):
        pass

    def get_color(self, response):
        """
        Checks if a field parsed successfully
        :return: Field value, if parsed, Nothing if parsing failed
        """
        return response.xpath('//div[@class="details__row"]/'
                              'span[contains(text(), "Цвеgт")]/../text()').get()

    def parse(self, response):
        link = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').get()
        last_page = response.xpath('//ul[@class="pagination"]/li[last()]/a/text()').get()
        url_list = [
            response.urljoin(link[:-2] + str(x+1)) for x in range(int(last_page))
        ]
        # for link in url_list:
        #     yield scrapy.Request(link, self.parse_cloth_list)
        print(url_list[5:7])
        for index, link in enumerate(url_list[5:7]):
            yield scrapy.Request(url_list[index], self.parse_cloth_list)

    def parse_cloth_list(self, response):
        cloth_link_list = response.xpath('//ul[contains(@class, "product__list")]/'
                                         'li[contains(@class, "product__item")]//'
                                         'a[contains(@class, "product__desc__name")]/'
                                         '@href').getall()
        # for link in cloth_link_list:
        #     yield scrapy.Request(response.urljoin(link), self.parse_cloth_item)
        for index, link in enumerate(cloth_link_list[1:3]):
            item_id = link.split('-')[-1].strip('/')
            yield scrapy.Request(response.urljoin(link), self.parse_cloth_fields, meta={'item_id': item_id})

    def parse_cloth_fields(self, response):
        meta_dict = dict()
        meta_dict['brand'] = response.xpath('//h1[@itemprop="name"]/a/text()').get()
        meta_dict['title'] = response.xpath('//h1[@itemprop="name"]/span/text()').get()
        meta_dict['image'] = response.xpath('//img[@itemprop="image"]/@src').get()
        meta_dict['price'] = response.xpath('//span[contains(@itemprop, "price")]/text()').get()
        meta_dict['descr'] = response.xpath('//p[contains(@itemprop, "description")]/text()').get()
        # meta_dict['color'] = self.get_color(response)

        meta_dict['color'] = response.xpath('//div[@class="deta2ils__row"]/'
                                            'span[contains(text(), "Цвеgт")]/../text()').get()

        size_request_url = self.size_base_url + response.meta['item_id'] + '/'
        return scrapy.Request(size_request_url, self.parse_cloth_item_with_size, meta=meta_dict)

    def parse_cloth_item_with_size(self, response):

        fields_item = AizelClothItem()
        fields_item['brand'] = response.meta['brand']
        fields_item['title'] = response.meta['title']
        fields_item['image'] = response.urljoin(response.meta['image'])
        fields_item['price'] = response.meta['price']
        fields_item['size'] = response.xpath('//ul[contains(@class, "size__list")]//'
                                             'span[@class="product-size-title"]/text()').getall()
        fields_item['descr'] = response.meta['descr']
        fields_item['color'] = response.meta['color']
        print(fields_item)
