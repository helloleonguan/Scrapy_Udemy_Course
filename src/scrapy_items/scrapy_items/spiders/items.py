# -*- coding: utf-8 -*-
import scrapy
from scrapy_items.items import ScrapyItemsItem


class ItemsSpider(scrapy.Spider):
    name = 'items'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        authors = response.xpath("//*[@itemprop='author']/text()").extract()

        item = ScrapyItemsItem()
        item['authors'] = authors

        return item
