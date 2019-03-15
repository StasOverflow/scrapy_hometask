import scrapy
from scrapy_parse.items import AizelClothItem


class AizelClothSpider(scrapy.Spider):
    name = "aizel"

    # xpath to find last paginated_page: x('//ul[@class="pagination"]/li[last()]')

    # start_urls = ("https://aizel.ru/ua-ru/odezhda/bryuki/", )
    start_urls = ("https://aizel.ru/ua-ru/alexanderwangt/serye-bryuki-dzhoggery-s-printom-113697/", )

    def parse(self, response):
        brand = response.xpath('//h1[@itemprop="name"]/a/text()').get()
        title = response.xpath('//h1[@itemprop="name"]/span/text()').get()
        image = response.xpath('//img[@itemprop="image"]/@src').get()
        price = response.xpath('//span[contains(@class, "price")]/text()').get()
        sizes = response.xpath('//li[contains(@class, "size")]/span[@class="product-size-title"]/text()').get()
        descr = response.xpath('//p[contains(@itemprop, "description")]/text()').get()
        color = response.xpath('//div[@class="details__row"]/text()')[-1].extract()

        fields_item = AizelClothItem()
        fields_item['brand'] = brand
        fields_item['title'] = title
        fields_item['image'] = image
        fields_item['price'] = price
        fields_item['sizes'] = sizes
        fields_item['descr'] = descr
        fields_item['color'] = color

        print(fields_item)

