import scrapy
from scrapy_parse.items import AizelClothItem
from scrapy_redis.spiders import RedisSpider


class AizelClothSpider(RedisSpider):
    name = "aizel"
    # start_urls = ("https://aizel.ru/ua-ru/odezhda/bryuki/", )

    # def make_request_from_data(self, data):

    def parse(self, response):
        link = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').get()
        last_page = response.xpath('//ul[@class="pagination"]/li[last()]/a/text()').get()
        url_list = [
            response.urljoin(link[:-2] + str(x+1)) for x in range(int(last_page))
        ]
        # for link in url_list:
        #     yield scrapy.Request(link, self.parse_cloth_list)
        print(url_list[5:6])
        for index, link in enumerate(url_list[2:6]):
            yield scrapy.Request(url_list[index], self.parse_cloth_list)

    def parse_cloth_list(self, response):
        cloth_link_list = response.xpath('//ul[contains(@class, "product__list")]/'
                                         'li[contains(@class, "product__item")]//'
                                         'a[contains(@class, "product__desc__name")]/'
                                         '@href').getall()
        for link in cloth_link_list:
            yield scrapy.Request(response.urljoin(link), self.parse_cloth_item)

    def parse_cloth_item(self, response):
        brand = response.xpath('//h1[@itemprop="name"]/a/text()').get()
        title = response.xpath('//h1[@itemprop="name"]/span/text()').get()
        image = response.xpath('//img[@itemprop="image"]/@src').get()
        price = response.xpath('//span[contains(@itemprop, "price")]/text()').get()

        '''
            The following code snippet returns nothing, because its content is added to page via js
            
            sizes = response.xpath('//li[contains(@class, "size")]/span[@class="product-size-title"]/text()').get()
        '''
        # size = response.xpath('//div[@class="details__row"]/text()')[2].get().strip().split(' ')[-1:]

        descr = response.xpath('//p[contains(@itemprop, "description")]/text()').get()
        color = response.xpath('//div[@class="details__row"]/span[contains(text(), "Цвет")]/../text()').get()

        fields_item = AizelClothItem()
        fields_item['brand'] = brand
        fields_item['title'] = title
        fields_item['image'] = image
        fields_item['price'] = price
        # fields_item['size'] = size
        fields_item['descr'] = descr
        fields_item['color'] = color
        print(fields_item)
