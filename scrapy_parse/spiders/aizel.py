import scrapy
from scrapy_parse.items import AizelClothItem


class AizelClothSpider(scrapy.Spider):
    name = "aizel"

    # xpath to find last paginated_page: x('//ul[@class="pagination"]/li[last()]')